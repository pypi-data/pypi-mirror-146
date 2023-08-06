from __future__ import division, print_function, unicode_literals

import errno
import json
import os
import os.path
import random
import shlex
import signal
import subprocess
import sys
import traceback
import warnings
from collections import defaultdict
from copy import copy
from enum import Enum
from functools import partial
from itertools import chain
from pathlib import Path
from tempfile import NamedTemporaryFile
from time import sleep
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

import attr
import psutil
import requests
import six
from clearml import Task
from clearml_agent import backend_config
from clearml_agent.backend_api.services import auth as auth_api
from clearml_agent.backend_api.services import queues as queues_api
from clearml_agent.backend_api.services import tasks as tasks_api
from clearml_agent.backend_api.services import workers as workers_api
from clearml_agent.backend_api.session import CallResult
from clearml_agent.backend_api.session.defs import ENV_ENABLE_ENV_CONFIG_SECTION, ENV_ENABLE_FILES_CONFIG_SECTION
from clearml_agent.backend_config.defs import UptimeConf
from clearml_agent.backend_config.utils import apply_environment, apply_files
from clearml_agent.commands.base import ServiceCommandSection
from clearml_agent.commands.events import Events
from clearml_agent.definitions import (
    ENV_AGENT_AUTH_TOKEN,
    ENV_AGENT_GIT_PASS,
    ENV_AGENT_SECRET_KEY,
    ENV_AWS_SECRET_KEY,
    ENV_AZURE_ACCOUNT_KEY,
    ENV_DOCKER_HOST_MOUNT,
    ENV_EXTRA_DOCKER_ARGS,
    ENVIRONMENT_SDK_PARAMS,
    PIP_EXTRA_INDICES,
    PROGRAM_NAME,
)
from clearml_agent.errors import APIError, CommandFailedError, Sigterm
from clearml_agent.helper.base import (
    ExecutionInfo,
    HOCONEncoder,
    check_directory_path,
    error,
    is_conda,
    is_linux_platform,
    is_windows_platform,
)
from clearml_agent.helper.base import mkstemp as safe_mkstemp
from clearml_agent.helper.base import (
    print_table,
    return_list,
    safe_remove_file,
    safe_remove_tree,
    select_for_platform,
    warning,
)
from clearml_agent.helper.check_update import start_check_update_daemon
from clearml_agent.helper.console import decode_binary_lines, print_text
from clearml_agent.helper.os.daemonize import daemonize_process
from clearml_agent.helper.package.base import PackageManager
from clearml_agent.helper.package.conda_api import CondaAPI
from clearml_agent.helper.package.external_req import ExternalRequirements
from clearml_agent.helper.package.poetry_api import PoetryAPI, PoetryConfig
from clearml_agent.helper.package.post_req import PostRequirement
from clearml_agent.helper.package.priority_req import PackageCollectorRequirement, PriorityPackageRequirement
from clearml_agent.helper.package.pytorch import PytorchRequirement
from clearml_agent.helper.process import (
    COMMAND_SUCCESS,
    Argv,
    Executable,
    ExitStatus,
    WorkerParams,
    kill_all_child_processes,
    shutdown_docker_process,
    terminate_all_child_processes,
    terminate_process,
)
from clearml_agent.helper.resource_monitor import ResourceMonitor
from clearml_agent.helper.runtime_verification import check_runtime, print_uptime_properties
from clearml_agent.helper.singleton import Singleton
from clearml_agent.session import Session
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning

DOCKER_ROOT_CONF_FILE = "/root/clearml.conf"
DOCKER_DEFAULT_CONF_FILE = "/root/default_clearml.conf"


sys_random = random.SystemRandom()


CONCAT_CMD = select_for_platform(linux=" && ", windows=" & ")


class TaskNotFoundError(APIError):
    pass


class TaskStopReason(Enum):
    no_stop = 0
    stopped = 1
    reset = 2
    status_changed = 3
    exception = 4
    not_found = 5
    service_started = 6


def _send_request(
    self: Session,
    service: str,
    action: str,
    version: Optional[int] = None,
    method: str = "get",
    headers: Optional[Dict[str, str]] = None,
    auth: Optional[HTTPBasicAuth] = None,
    data: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
    refresh_token_if_unauthorized: bool = True,
) -> requests.models.Response:
    """ Internal implementation for making a raw API request.
        - Constructs the api endpoint name
        - Injects the worker id into the headers
        - Allows custom authorization using a requests auth object
        - Intercepts `Unauthorized` responses and automatically attempts to refresh the session token once in this
          case (only once). This is done since permissions are embedded in the token, and addresses a case where
          server-side permissions have changed but are not reflected in the current token. Refreshing the token will
          generate a token with the updated permissions.
    """
    host = self.host
    headers = headers.copy() if headers else {}
    for h in self._WORKER_HEADER:
        headers[h] = self.worker
    for h in self._CLIENT_HEADER:
        headers[h] = self.client

    token_refreshed_on_error = False
    url = ("{host}/v{version}/{service}.{action}" if version else "{host}/{service}.{action}").format(**locals())
    while True:
        if data and len(data) > self._write_session_data_size:
            timeout = self._write_session_timeout
        elif self._session_requests < 1:
            timeout = self._session_initial_timeout
        else:
            timeout = self._session_timeout
        res: requests.models.Response = self._Session__http_session.request(
            method, url, headers=headers, auth=auth, data=data, json=json, timeout=timeout, verify=False
        )

        if (
            refresh_token_if_unauthorized
            and res.status_code == requests.codes.unauthorized
            and not token_refreshed_on_error
        ):
            # it seems we're unauthorized, so we'll try to refresh our token once in case permissions changed since
            # the last time we got the token, and try again
            self.refresh_token()
            token_refreshed_on_error = True
            # try again
            continue
        if res.status_code == requests.codes.service_unavailable and self.config.get(
            "api.http.wait_on_maintenance_forever", True
        ):
            self._logger.warning("Service unavailable: {} is undergoing maintenance, retrying...".format(host))
            continue
        break
    self._session_requests += 1
    return res


Session.__base__._send_request = _send_request


warnings.filterwarnings("ignore", category=InsecureRequestWarning)


def get_task(session: Session, task_id: str, **kwargs: Any):  # type: ignore
    """
    Use manual api call so that we can pass 'search_hidden' param from api v2.14
    Returns: clearml_agent.backend_api.session.client.client.Task
    """

    # return session.api_client.tasks.get_all(id=[task_id], **kwargs)[0]
    res = session.send_request(
        service="tasks",
        action="get_all",
        version="2.14",
        json={"id": [task_id], "search_hidden": True, **kwargs},
        method="get",
        async_enable=False,
    )
    result = CallResult.from_result(
        res=res,
        request_cls=tasks_api.GetAllRequest,
        logger=session._logger,
        service="tasks",
        action="get_all",
        session=session,
    )
    if not result.ok():
        raise APIError(result)
    if not result.response:
        raise APIError(result, extra_info="Invalid response")
    if not result.response.tasks:
        raise TaskNotFoundError(result)
    return result.response.tasks[0]


def get_next_task(session: Session, queue: str, get_task_info: bool = False) -> Dict[str, Dict[str, str]]:
    """
    Returns dict that contains next task and its additional info (company, user)
    """
    request: Dict[str, Any] = {"queue": queue}
    if get_task_info:
        request["get_task_info"] = True
    result = session.send_request(
        service="queues", action="get_next_task", version="2.14", json=request, method="get", async_enable=False
    )
    if not result.ok:
        raise APIError(result)
    data: Optional[Dict[str, Dict[str, str]]] = result.json().get("data")
    if data is None:
        raise APIError(result, extra_info="Invalid response")
    return data


class TaskStopSignal(object):
    """
    Follow task status and signals when it should be stopped
    """

    _number_of_consecutive_reset_tests = 4
    statuses = tasks_api.TaskStatusEnum
    unexpected_statuses = [statuses.closed, statuses.stopped, statuses.failed, statuses.published, statuses.queued]
    default = TaskStopReason.no_stop
    stopping_message = "stopping"

    def __init__(self, command: "Worker", session: Session, events_service: Events, task_id: str):
        """
        :param command: workers command
        :param session: command session
        :param events_service: events service object
        :param task_id: followed task ID
        """
        self.command = command
        self.session = session
        self.events_service = events_service
        self.worker_id = command.worker_id
        self._task_reset_state_counter = 0
        self.task_id = task_id

    def test(self) -> TaskStopReason:
        """
        Returns whether task should stop and for what reason,
        returns TaskStopReason.no_stop if task shouldn't stop.
        Catches and logs exceptions.
        """
        try:
            return self._test()
        except TaskNotFoundError:
            return TaskStopReason.not_found
        except Exception as ex:
            self.command.log_traceback(ex)
            # make sure we break nothing
            return TaskStopSignal.default

    def _test(self) -> TaskStopReason:
        """
        "Unsafe" version of test()
        """
        task_info = get_task(self.session, self.task_id, only_fields=["status", "status_message"])
        status = task_info.status
        message = task_info.status_message

        if status == self.statuses.in_progress and self.stopping_message in message:
            self.command.log("task status_message has '%s', task will terminate", self.stopping_message)
            return TaskStopReason.stopped

        if status in self.unexpected_statuses:  # ## and "worker" not in message:
            self.command.log("unexpected status change, task will terminate")
            return TaskStopReason.status_changed

        if status == self.statuses.created:
            if self._task_reset_state_counter >= self._number_of_consecutive_reset_tests:
                self.command.log("task was reset, task will terminate")
                return TaskStopReason.reset
            self._task_reset_state_counter += 1
            warning_msg = "Warning: Task {} was reset! if state is consistent we shall terminate ({}/{}).".format(
                self.task_id, self._task_reset_state_counter, self._number_of_consecutive_reset_tests
            )
            if self.events_service:
                self.events_service.send_log_events(
                    self.worker_id, task_id=self.task_id, lines=[warning_msg], level="WARNING"
                )
            print(warning_msg)
        else:
            self._task_reset_state_counter = 0

        return TaskStopReason.no_stop


class Worker(ServiceCommandSection):
    _pip_extra_index_url = PIP_EXTRA_INDICES

    _requirement_substitutions = (
        PytorchRequirement,
        PriorityPackageRequirement,
        PostRequirement,
        ExternalRequirements,
        partial(PackageCollectorRequirement, collect_package=["trains"]),
        partial(PackageCollectorRequirement, collect_package=["clearml"]),
    )

    # poll queues every _polling_interval seconds
    _polling_interval = 5.0
    # machine status update intervals, seconds
    _machine_update_interval = 30.0

    # message printed before starting task logging,
    # it will be parsed by services_mode, to identify internal docker logging start
    _task_logging_start_message = "Running task '{}'"
    # last message before passing control to the actual task
    _task_logging_pass_control_message = "Running task id [{}]:"

    # label with worker id for worker agent docker in services mode
    _worker_label = "clearml-worker-id={}"
    # label with parent worker id for worker agent docker in services mode
    _parent_worker_label = "clearml-parent-worker-id={}"

    _run_as_user_home = "/clearml_agent_home"
    _docker_fixed_user_cache = "/clearml_agent_cache"
    _temp_cleanup_list: List[str] = []

    @property
    def service(self) -> str:
        """ Worker command service endpoint """
        return "workers"

    @property
    def _task_status_change_message(self) -> str:
        return "Changed by {} {}".format(PROGRAM_NAME, self.worker_id)

    @staticmethod
    def register_signal_handler() -> None:
        def handler(*_: Any) -> None:
            for f in Worker._temp_cleanup_list + [Singleton.get_pid_file()]:
                safe_remove_tree(f)
            raise Sigterm()

        signal.signal(signal.SIGTERM, handler)

    def __init__(self, *args: Any, **kwargs: Any):
        super(Worker, self).__init__(*args, **kwargs)
        self.monitor = None
        self.log = self._session.get_logger(__name__)
        self.register_signal_handler()
        self._worker_registered = False
        self.is_conda: bool = is_conda(self._session.config)
        # Add extra index url - system wide
        extra_url = None
        # noinspection PyBroadException
        try:
            if self._session.config.get("agent.package_manager.extra_index_url", None):
                extra_url = self._session.config.get("agent.package_manager.extra_index_url", [])
                if not isinstance(extra_url, (tuple, list)):
                    extra_url = [extra_url]
                # put external pip url before default ones, so we first look for packages there
                for e in reversed(extra_url):
                    self._pip_extra_index_url.insert(0, e)
        except Exception:
            self.log.warning("Failed adding extra-index-url to pip environment: {}".format(extra_url))
        # update pip install command
        pip_install_cmd = ["pip", "install"]
        if self._pip_extra_index_url:
            pip_install_cmd.extend(chain.from_iterable(("--extra-index-url", x) for x in self._pip_extra_index_url))
        self.pip_install_cmd = tuple(pip_install_cmd)
        self.worker_id = self._session.config["agent.worker_id"] or "{}:{}".format(
            self._session.config["agent.worker_name"], os.getpid()
        )

        self._last_report_timestamp = psutil.time.time()
        self.temp_config_path: Optional[str] = None
        self.queues: Sequence[str] = ()
        self.venv_folder: Optional[str] = None
        self.package_api: Optional[PackageManager] = None
        self.global_package_api = None

        self.is_venv_update = self._session.config.agent.venv_update.enabled
        self.poetry = PoetryConfig(self._session)
        self.docker_image_func = None
        self._docker_image = None
        self._docker_arguments = None
        PackageManager.set_pip_version(self._session.config.get("agent.package_manager.pip_version", None))
        self._extra_docker_arguments = ENV_EXTRA_DOCKER_ARGS.get() or self._session.config.get(
            "agent.extra_docker_arguments", None
        )
        self._extra_shell_script = self._session.config.get("agent.extra_docker_shell_script", None)
        self._docker_force_pull = self._session.config.get("agent.docker_force_pull", False)
        self._daemon_foreground: Optional[bool] = None
        self._standalone_mode: Optional[bool] = None
        self._services_mode: Optional[bool] = None
        self._impersonate_as_task_owner = False
        self._worker_tags = None
        self._dynamic_gpus: Optional[bool] = None
        self._force_current_version = None
        self._redirected_stdout_file_no = None
        self._uptime_config = self._session.config.get("agent.uptime", None)
        self._downtime_config = self._session.config.get("agent.downtime", None)
        self._suppress_cr = self._session.config.get("agent.suppress_carriage_return", True)
        self._host_ssh_cache = None
        self._truncate_task_output_files = bool(self._session.config.get("agent.truncate_task_output_files", False))

        # True - supported
        # None - not initialized
        # str - not supported, version string indicates last server version
        self._runtime_props_support: Optional[Union[bool, str]] = None

    @classmethod
    def _verify_command_states(cls, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Conform and enforce command argument
        This is where you can automatically turn on/off switches based on different states.
        :param kwargs:
        :return: kwargs
        """
        if kwargs.get("services_mode"):
            kwargs["cpu_only"] = True
            kwargs["gpus"] = None

        return kwargs

    def handle_user_abort(self, task_id: str, session: Optional[Session] = None) -> None:
        """
        Set task status to appropriate value on user abort.
        """
        session = session or self._session
        # noinspection PyBroadException
        try:
            task_status = session.send_api(tasks_api.GetByIdRequest(task_id)).task.status
            if task_status == tasks_api.TaskStatusEnum.in_progress:
                print("\nUser abort - stopping task {}".format(task_id))
                session.send_api(tasks_api.StoppedRequest(task_id))
        except Exception:
            pass

    def get_task_session(self, user: str, company: str) -> Optional[Session]:
        """
        Get task session for the user by cloning the agent session
        and replacing the session credentials with the task owner auth token
        In case the task is not from the user company proceed with another login
        to get the auth token for the tenant and return the session for it
        Requires that agent session credentials will allow impersonation as task user
        """

        def get_new_session(session: Session, headers: Dict[str, str]) -> Optional[Session]:
            result = session.send(auth_api.LoginRequest(), headers=headers)
            if not (result.ok() and result.response):
                return None
            new_session = copy(session)
            new_session.set_auth_token(result.response.token)
            return new_session

        task_session = get_new_session(self._session, headers={"X-Clearml-Impersonate-As": user})
        if not task_session:
            return None

        token = task_session.get_decoded_token(task_session.token)
        if token.get("tenant") == company:
            return task_session

        return get_new_session(task_session, headers={"X-Clearml-Tenant": company})

    def run_tasks_loop(
        self,
        queues: List[str],
        projects_paths: List[str],
        venv_names: List[str],
        worker_params: WorkerParams,
        priority_order: bool = True,
        gpu_indexes: Optional[List[int]] = None,
        gpu_queues: Optional[List[Tuple[str, Tuple[int, int]]]] = None,
    ) -> None:
        """
        :summary: Pull and run tasks from queues.
        :description: 1. Go through ``queues`` by order.
                      2. Try getting the next task for each and run the first one that returns.
                      3. Go to step 1
        :param list(str) queues: IDs of queues to pull tasks from
        :param worker_params worker_params: Worker command line arguments
        :param bool priority_order: If True pull order in priority manner. always from the first
            If False, pull from each queue once in a round robin manner
        :param list gpu_indexes: list of gpu_indexes. Needs special backend support
        :param list gpu_queues: list of pairs (queue_id, num_gpus). Needs special backend support
        :param str projects_paths:
        :param str venv_names:
        """

        if not self._daemon_foreground:
            print("Starting infinite task polling loop...")

        max_num_instances: Optional[int] = None
        if self._services_mode:
            try:
                max_num_instances = int(self._services_mode) if not isinstance(self._services_mode, bool) else -1
            except (ValueError, TypeError):
                max_num_instances = -1

        # store in runtime configuration,
        if max_num_instances and not self.set_runtime_properties(key="max_num_instances", value=max_num_instances):
            warning("Maximum number of service instance not supported, removing limit.")
            max_num_instances = -1

        # get current running instances
        available_gpus = None
        dynamic_gpus_worker_id = None

        _gpu_queues: Optional[Dict[str, Tuple[int, int]]] = None
        if gpu_indexes and gpu_queues:
            available_gpus, _gpu_queues = self._setup_dynamic_gpus(gpu_queues)
            # multi instance support
            self._services_mode = True

        # last 64 tasks
        list_task_gpus_ids = {}
        try:
            while True:
                queue_tags = None
                runtime_props = None

                if max_num_instances and max_num_instances > 0:
                    # make sure we do not have too many instances to run
                    if self.docker_image_func:
                        running_count = self._get_child_agents_count_for_worker()
                    else:
                        running_count = len(Singleton.get_running_pids())
                    if running_count >= max_num_instances:
                        if self._daemon_foreground or worker_params.debug:
                            print(
                                "Reached max number of services {}, sleeping for {:.1f} seconds".format(
                                    max_num_instances, self._polling_interval
                                )
                            )
                        sleep(self._polling_interval)
                        continue

                # update available gpus
                if _gpu_queues and gpu_indexes:
                    available_gpus = self._dynamic_gpu_get_available(gpu_indexes)
                    # if something went wrong or we have no free gpus
                    # start over from the highest priority queue
                    if not available_gpus:
                        if self._daemon_foreground or worker_params.debug:
                            print("All GPUs allocated, sleeping for {:.1f} seconds".format(self._polling_interval))
                        sleep(self._polling_interval)
                        continue

                # iterate over queues (priority style, queues[0] is highest)
                for queue, projects_path, venv_name in zip(queues, projects_paths, venv_names):

                    if queue_tags is None or runtime_props is None:
                        queue_tags, runtime_props = self.get_worker_properties(queues)

                    if runtime_props and not self.should_be_currently_active(queue_tags[queue], runtime_props):
                        continue

                    if _gpu_queues and available_gpus:
                        # peek into queue
                        # get next task in queue
                        # noinspection PyBroadException
                        try:
                            response = self._session.send_api(queues_api.GetByIdRequest(queue=queue))
                        except Exception:
                            # if something went wrong start over from the highest priority queue
                            break
                        if not len(response.queue.entries):
                            continue
                        # check if we do not have enough available gpus
                        if _gpu_queues[queue][0] > len(available_gpus):
                            # not enough available_gpus, we should sleep and start over
                            if self._daemon_foreground or worker_params.debug:
                                print(
                                    "Not enough free GPUs {}/{}, sleeping for {:.1f} seconds".format(
                                        len(available_gpus), _gpu_queues[queue][0], self._polling_interval
                                    )
                                )
                            sleep(self._polling_interval)
                            break

                    # get next task in queue
                    try:
                        response = get_next_task(
                            self._session, queue=queue, get_task_info=self._impersonate_as_task_owner
                        )
                    except Exception as e:
                        print("Warning: Could not access task queue [{}], error: {}".format(queue, e))
                        continue
                    else:
                        try:
                            task_id = response["entry"]["task"]
                        except (KeyError, TypeError, AttributeError):
                            if self._daemon_foreground or worker_params.debug:
                                print("No tasks in queue {}".format(queue))
                            continue

                        # clear output log if we start a new Task
                        if (
                            not worker_params.debug
                            and self._redirected_stdout_file_no is not None
                            and self._redirected_stdout_file_no > 2
                        ):
                            try:
                                os.lseek(self._redirected_stdout_file_no, 0, 0)
                                os.ftruncate(self._redirected_stdout_file_no, 0)
                            except Exception as ex:
                                print("Failed to clear output, exception occurred:", ex)

                        task_session = None
                        if self._impersonate_as_task_owner:
                            try:
                                task_user = response["task_info"]["user"]
                                task_company = response["task_info"]["company"]
                            except (KeyError, TypeError, AttributeError):
                                print("Error: cannot retrieve owner user for the task '{}', skipping".format(task_id))
                                continue

                            task_session = self.get_task_session(task_user, task_company)
                            if not task_session:
                                print(
                                    "Error: Could not login as the user '{}' for the task '{}', skipping".format(
                                        task_user, task_id
                                    )
                                )
                                continue

                        self.report_monitor(ResourceMonitor.StatusReport(queues=queues, queue=queue, task=task_id))

                        org_gpus = os.environ.get("NVIDIA_VISIBLE_DEVICES")
                        dynamic_gpus_worker_id = self.worker_id
                        # the following is only executed in dynamic gpus mode
                        if _gpu_queues and _gpu_queues.get(queue):
                            # pick the first available GPUs
                            # gpu_queues[queue] = (min_gpus, max_gpus)
                            # get as many gpus as possible with max_gpus as limit, the min is covered before
                            gpus = available_gpus[: _gpu_queues.get(queue)[1]]  # type: ignore
                            available_gpus = available_gpus[_gpu_queues.get(queue)[1] :]  # type: ignore
                            self.set_runtime_properties(
                                key="available_gpus", value=",".join(str(g) for g in available_gpus)
                            )
                            os.environ["CUDA_VISIBLE_DEVICES"] = os.environ["NVIDIA_VISIBLE_DEVICES"] = ",".join(
                                str(g) for g in gpus
                            )
                            list_task_gpus_ids.update({str(g): task_id for g in gpus})
                            self.worker_id = ":".join(
                                self.worker_id.split(":")[:-1] + ["gpu" + ",".join(str(g) for g in gpus)]
                            )

                        self.send_logs(
                            task_id=task_id,
                            lines=["task {} pulled from {} by worker {}\n".format(task_id, queue, self.worker_id)],
                            level="INFO",
                            session=task_session,
                        )

                        self.execute(
                            task_id=task_id,
                            log_level=worker_params.log_level,
                            projects_path=projects_path,
                            venv_name=venv_name,
                            standalone_mode=True,
                        )

                        if _gpu_queues:
                            self.worker_id = dynamic_gpus_worker_id
                            os.environ["CUDA_VISIBLE_DEVICES"] = org_gpus  # type: ignore
                            os.environ["NVIDIA_VISIBLE_DEVICES"] = org_gpus  # type: ignore

                        self.report_monitor(ResourceMonitor.StatusReport(queues=self.queues))

                        queue_tags = None
                        runtime_props = None

                        # if we are using priority start pulling from the first always,
                        # if we are doing round robin, pull from the next one
                        if priority_order:
                            break
                else:
                    # sleep and retry polling
                    if self._daemon_foreground or worker_params.debug:
                        print("No tasks in Queues, sleeping for {:.1f} seconds".format(self._polling_interval))
                    sleep(self._polling_interval)

                if self._session.config["agent.reload_config"]:
                    self.reload_config()
        finally:
            # if we are in dynamic gpus mode, shutdown all active runs
            if self.docker_image_func:
                for t_id in set(list_task_gpus_ids.values()):
                    if shutdown_docker_process(docker_cmd_contains="--id {}'\"".format(t_id)):
                        self.handle_task_termination(task_id=t_id, exit_code=0, stop_reason=TaskStopReason.stopped)
            else:
                # if we are in dynamic gpus / services mode,
                # we should send termination signal to all child processes
                if self._services_mode:
                    terminate_all_child_processes(timeout=20, include_parent=False)

                # if we are here, just kill all sub processes
                kill_all_child_processes()

            # unregister dynamic GPU worker, if we were terminated while setting up a Task
            if dynamic_gpus_worker_id:
                self.worker_id = dynamic_gpus_worker_id
                self._unregister()

    def _dynamic_gpu_get_available(self, gpu_indexes: List[int]) -> Optional[List[int]]:
        # noinspection PyBroadException
        try:
            response = self._session.send_api(workers_api.GetAllRequest(last_seen=600))
        except Exception:
            return None

        worker_name = self._session.config["agent.worker_name"] + ":gpu"
        our_workers = [w.id for w in response.workers if w.id.startswith(worker_name) and w.id != self.worker_id]
        gpus: List[int] = []
        for w in our_workers:
            gpus += [int(g) for g in w.split(":")[-1].lower().replace("gpu", "").split(",")]
        available_gpus = list(set(gpu_indexes) - set(gpus))

        return available_gpus

    def _setup_dynamic_gpus(
        self, gpu_queues: List[Tuple[str, Tuple[int, int]]]
    ) -> Tuple[List[int], Dict[str, Tuple[int, int]]]:
        _available_gpus = self.get_runtime_properties()
        if _available_gpus is None:
            raise ValueError("Dynamic GPU allocation is not supported by the ClearML-server")
        available_gpus = [prop["value"] for prop in _available_gpus if prop["key"] == "available_gpus"]
        if available_gpus:
            available_gpus = [int(g) for g in available_gpus[-1].split(",")]
        _gpu_queues = dict(gpu_queues) if not isinstance(gpu_queues, dict) else gpu_queues

        if not self.set_runtime_properties(key="available_gpus", value=",".join(str(g) for g in available_gpus)):
            raise ValueError("Dynamic GPU allocation is not supported by the ClearML-server")

        return available_gpus, _gpu_queues

    def get_worker_properties(
        self, queue_ids: List[str]
    ) -> Tuple[Dict[str, Dict[str, Any]], Optional[List[Dict[str, Any]]]]:
        queue_tags = {
            q.id: {"name": q.name, "tags": q.tags}
            for q in self._session.send_api(queues_api.GetAllRequest(id=queue_ids, only_fields=["id", "tags"])).queues
        }
        runtime_props = self.get_runtime_properties()
        return queue_tags, runtime_props

    def get_runtime_properties(self) -> Optional[List[Dict[str, Any]]]:
        if self._runtime_props_support is not True:
            # either not supported or never tested
            if self._runtime_props_support == self._session.api_version:
                # tested against latest api_version, not supported
                return None
            if not self._session.check_min_api_version(UptimeConf.min_api_version):
                # not supported due to insufficient api_version
                self._runtime_props_support = self._session.api_version
                return None
        try:
            res: List[Dict[str, Any]] = self.get("get_runtime_properties", worker=self.worker_id)["runtime_properties"]
            # definitely supported
            self._runtime_props_support = True
            return res
        except APIError:
            self._runtime_props_support = self._session.api_version
        return None

    def set_runtime_properties(self, key: str, value: Any) -> bool:
        if self._runtime_props_support is not True:
            # either not supported or never tested
            if self._runtime_props_support == self._session.api_version:
                # tested against latest api_version, not supported
                return False
            if not self._session.check_min_api_version(UptimeConf.min_api_version):
                # not supported due to insufficient api_version
                self._runtime_props_support = self._session.api_version
                return False

        try:
            self.post(
                "set_runtime_properties",
                json={"runtime_properties": [{"key": key, "value": str(value)}], "worker": self.worker_id},
            )
            # definitely supported
            self._runtime_props_support = True
            return True
        except APIError:
            self._runtime_props_support = self._session.api_version
        except Exception as ex:
            print("set_runtime_properties failed with exception:", ex)

        return False

    def should_be_currently_active(
        self, current_queue: Dict[str, Any], runtime_properties: List[Dict[str, Any]]
    ) -> bool:
        """
        Checks if a worker is active according to queue tags, worker's runtime properties and uptime schedule.
        """
        runtime_properties = runtime_properties or []
        if UptimeConf.queue_tag_off in current_queue["tags"]:
            self.log.debug(
                "Queue {} is tagged '{}', worker will not pull tasks".format(
                    current_queue["name"], UptimeConf.queue_tag_off
                )
            )
            return False
        if UptimeConf.queue_tag_on in current_queue["tags"]:
            self.log.debug(
                "Queue {} is tagged '{}', worker will pull tasks".format(
                    current_queue["name"], UptimeConf.queue_tag_on
                )
            )
            return True
        force_flag = next((prop for prop in runtime_properties if prop["key"] == UptimeConf.worker_key), None)
        if force_flag:
            if force_flag["value"].lower() in UptimeConf.worker_value_off:
                self.log.debug(
                    "worker has the following runtime property: '{}'. worker will not pull tasks".format(force_flag)
                )
                return False
            elif force_flag["value"].lower() in UptimeConf.worker_value_on:
                self.log.debug(
                    "worker has the following runtime property: '{}'. worker will pull tasks".format(force_flag)
                )
                return True
            else:
                print(
                    "Warning: invalid runtime_property '{}: {}' supported values are: '{}/{}', ignoring".format(
                        force_flag["key"], force_flag["value"], UptimeConf.worker_value_on, UptimeConf.worker_value_off
                    )
                )
        if self._uptime_config:
            self.log.debug("following uptime configurations")
            check: bool = check_runtime(self._uptime_config)
            return check
        if self._downtime_config:
            self.log.debug("following downtime configurations")
            check = check_runtime(self._downtime_config, is_uptime=False)
            return check
        return True

    def reload_config(self) -> None:
        try:
            reloaded = self._session.reload()
        except Exception as ex:
            self.log("Failed reloading config file")
            self.log_traceback(ex)
        else:
            if reloaded:
                self.log('Config file change detected, reloading and updating "{.temp_config_path}"'.format(self))
                self.dump_config(self.temp_config_path, clean_api_credentials=self._impersonate_as_task_owner)

    def check(self, **_: Any) -> None:
        try:
            check_directory_path(str(Path(".").resolve()), check_whitespace_in_path=False)
        except OSError as e:
            if e.errno == errno.ENOENT:
                raise CommandFailedError("current working directory does not exist")
            raise

        for key in "agent.venvs_dir", "sdk.storage.cache.default_base_dir":
            try:
                value = self._session.config.get(key, None)
                if value:
                    check_directory_path(value)
            except CommandFailedError as e:
                raise CommandFailedError('Invalid config key "{}": {.message}'.format(key, e))

        if is_windows_platform():
            # if not self.is_conda:
            #     self.warning("Worker on Windows without Conda are not supported")
            if self._session.config.agent.venv_update:
                # self.warning("venv-update is not supported on Windows")
                self.is_venv_update = False

        self._session.print_configuration()

    def daemon(
        self,
        queues: List[str],
        projects_paths: List[str],
        log_level: str,
        foreground: bool = False,
        detached: bool = False,
        order_fairness: bool = False,
        venv_names: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> Optional[int]:

        if venv_names is None:
            venv_names = ["venv" for _ in queues]

        self._worker_tags = kwargs.get("child_report_tags", None)
        self._impersonate_as_task_owner = kwargs.get("use_owner_token", False)
        if self._impersonate_as_task_owner:
            if not self._session.check_min_api_version("2.14"):
                raise ValueError("Server does not support --use-owner-token option (incompatible API version)")
            if self._session.feature_set == "basic":
                raise ValueError("Server does not support --use-owner-token option")
        self._standalone_mode = kwargs.get("standalone_mode", False)
        self._services_mode = kwargs.get("services_mode", False)
        # must have docker in services_mode
        if self._services_mode:
            kwargs = self._verify_command_states(kwargs)
        self._uptime_config = kwargs.get("uptime", None) or self._uptime_config
        self._downtime_config = kwargs.get("downtime", None) or self._downtime_config
        if self._uptime_config and self._downtime_config:
            self.log.error(
                "Both uptime and downtime were specified when only one of them could be used. Both will be ignored."
            )
            self._uptime_config = None
            self._downtime_config = None

        # support --dynamic-gpus
        dynamic_gpus, gpu_indexes, queues = self._parse_dynamic_gpus(kwargs, queues)

        if self._services_mode and dynamic_gpus:
            raise ValueError("Combining --dynamic-gpus and --services-mode is not supported")

        # We are not running a daemon we are killing one.
        # find the pid send termination signal and leave
        if kwargs.get("stop", False):
            return 1 if not self._kill_daemon(dynamic_gpus=bool(dynamic_gpus)) else 0

        # if we do not need to create queues, make sure they are valid
        # match previous behaviour when we validated queue names before everything else
        queues = self._resolve_queue_names(queues, create_if_missing=kwargs.get("create_queue", False))

        queues_info = [q.to_dict() for q in self._session.send_api(queues_api.GetAllRequest(id=queues)).queues]

        if kwargs.get("status", False):
            runtime_properties = self.get_runtime_properties()
            if self._downtime_config:
                print_uptime_properties(self._downtime_config, queues_info, runtime_properties, is_uptime=False)
            else:
                print_uptime_properties(self._uptime_config, queues_info, runtime_properties)
            return 1

        # make sure we only have a single instance,
        # also make sure we set worker_id properly and cache folders
        self._singleton(dynamic_gpus=bool(dynamic_gpus))

        if dynamic_gpus and gpu_indexes:
            self._register_dynamic_gpus(gpu_indexes)

        # check if we have the latest version
        start_check_update_daemon()

        self.check(**kwargs)
        self.log.debug("starting resource monitor thread")
        print('Worker "{}" - '.format(self.worker_id), end="")

        columns: Tuple[str, ...] = ("id", "name", "tags")
        print("Listening to queues:")
        if dynamic_gpus:
            columns = ("id", "name", "tags", "gpus")
            for q in queues_info:
                q["gpus"] = str(dict(dynamic_gpus).get(q["id"]) or "")
        print_table(queues_info, columns=columns, titles=columns)

        # register worker
        self._register(queues)

        # create temp config file with current configuration
        self.temp_config_path = NamedTemporaryFile(suffix=".cfg", prefix=".clearml_agent.", mode="w+t").name

        self.dump_config(self.temp_config_path, clean_api_credentials=self._impersonate_as_task_owner)
        # only in none docker we have to make sure we have CUDA setup

        # make sure we have CUDA set if we have --gpus
        if kwargs.get("gpus") and self._session.config.get("agent.cuda_version", None) in (None, 0, "0"):
            message = (
                "Running with GPUs but no CUDA version was detected!\n"
                "\tSet OS environment CUDA_VERSION & CUDNN_VERSION to the correct version\n"
                "\tExample: export CUDA_VERSION=10.1 or (Windows: set CUDA_VERSION=10.1)"
            )
            if is_conda(self._session.config):
                self._unregister(queues)
                safe_remove_file(self.temp_config_path)
                raise ValueError(message)
            else:
                warning(message + "\n")

        if self._services_mode:
            print("ClearML-Agent running in services mode")

        self._daemon_foreground = foreground
        if not foreground:
            out_file, name = safe_mkstemp(
                prefix=".clearml_agent_daemon_out",
                suffix=".txt",
                open_kwargs={"buffering": self._session.config.get("agent.log_files_buffering", 1)},
            )
            print("Running CLEARML-AGENT daemon in background mode, writing stdout/stderr to {}".format(name))

            if not self._session.debug_mode:
                self._temp_cleanup_list.append(name)

            # on widows we do nothing
            if detached and is_windows_platform():
                print("Detached not supported on Windows, ignoring --detached")
                detached = False

            if not detached:
                # redirect std out/err to new file
                sys.stdout = sys.stderr = out_file
            else:
                # in detached mode
                # fully detach stdin.stdout/stderr and leave main process, running in the background
                daemonize_process(out_file.fileno())
                self._redirected_stdout_file_no = out_file.fileno()
                # make sure we update the singleton lock file to the new pid
                Singleton.update_pid_file()
                # reprint headers to std file (we are now inside the daemon process)
                print('Worker "{}" :'.format(self.worker_id))
                self._session.print_configuration()
                print_table(queues_info, columns=columns, titles=columns)

        try:
            while True:
                # noinspection PyBroadException
                try:
                    self.new_monitor(ResourceMonitor.StatusReport(queues=queues))
                    self.run_tasks_loop(
                        queues,
                        projects_paths=projects_paths,
                        venv_names=venv_names,
                        worker_params=WorkerParams(
                            log_level=log_level,
                            config_file=self.temp_config_path,
                            debug=self._session.debug_mode,
                            trace=self._session.trace,
                        ),
                        priority_order=not order_fairness,
                        gpu_indexes=gpu_indexes,
                        gpu_queues=dynamic_gpus,
                    )
                except Exception:
                    tb = six.text_type(traceback.format_exc())
                    print("FATAL ERROR:")
                    print(tb)
                    crash_file, name = safe_mkstemp(prefix=".clearml_agent-crash", suffix=".log")
                    # noinspection PyBroadException
                    try:
                        with crash_file:
                            crash_file.write(tb)
                    except Exception:
                        print("Could not write crash log to {}\nException:\n{}".format(name, tb))
                    sleep(1)
        finally:
            self._unregister(queues)
            safe_remove_file(self.temp_config_path)

    def _parse_dynamic_gpus(
        self, kwargs: Dict[str, Any], queues: List[str]
    ) -> Tuple[Optional[List[Tuple[str, Tuple[int, int]]]], Optional[List[int]], List[str]]:
        dynamic_gpus: Optional[List[Tuple[str, Tuple[int, int]]]] = kwargs.get("dynamic_gpus", None)
        if not dynamic_gpus:
            return None, None, queues

        queue_names = [q for q in queues]
        if not all("=" in q for q in queue_names):
            raise ValueError(
                "using --dynamic-gpus, --queue [{}], "
                "queue must be in format <queue_name>=<num_gpus>".format(queue_names)
            )

        gpu_indexes = kwargs.get("gpus")

        # test gpus were passed correctly
        if not gpu_indexes or len(gpu_indexes.split("-")) > 2 or ("," in gpu_indexes and "-" in gpu_indexes):
            raise ValueError(
                "--gpus must be provided, in one of two ways: " "comma separated '0,1,2,3' or range '0-3'"
            )
        try:
            if "-" in gpu_indexes:
                gpu_indexes = list(range(int(gpu_indexes.split("-")[0]), 1 + int(gpu_indexes.split("-")[1])))
            else:
                gpu_indexes = [int(g) for g in gpu_indexes.split(",")]
        except Exception:
            raise ValueError(
                'Failed parsing --gpus "{}". '
                "--dynamic_gpus must be use with "
                'specific gpus for example "0-7" or "0,1,2,3"'.format(kwargs.get("gpus"))
            )

        dynamic_gpus = []
        for s in queue_names:
            s_p = s.split("=")
            name = s[: -1 - len(s_p[-1])]
            min_max_g = int(s_p[-1].split("-")[0] or 1), int(s_p[-1].split("-")[-1])
            if min(min_max_g) <= 0:
                raise ValueError('Parsing min/max number of gpus <= 0 is not allowed: "{}"'.format(s))
            dynamic_gpus.append((name, min_max_g))
        queue_names = [q for q, _ in dynamic_gpus]
        # resolve queue ids
        dynamic_gpus_q = self._resolve_queue_names(queue_names, create_if_missing=kwargs.get("create_queue", False))
        dynamic_gpus = list(zip(dynamic_gpus_q, [i for _, i in dynamic_gpus]))
        # maintain original priority order
        queues = [q for q, _ in dynamic_gpus]

        self._dynamic_gpus = True

        return dynamic_gpus, gpu_indexes, queues

    def _register_dynamic_gpus(self, gpu_indexes: List[int]) -> None:
        # test server support
        available_gpus = self._dynamic_gpu_get_available(gpu_indexes)
        if available_gpus and not self.set_runtime_properties(
            key="available_gpus", value=",".join(str(g) for g in available_gpus)
        ):
            raise ValueError("Dynamic GPU allocation is not supported by the ClearML-server")

    def report_monitor(self, report: ResourceMonitor.StatusReport) -> None:
        if not self.monitor:
            self.new_monitor(report=report)
        else:
            self.monitor.set_report(report)
        if self.monitor is not None:
            self.monitor.send_report()

    def stop_monitor(self) -> None:
        if self.monitor:
            self.monitor.stop()
            self.monitor = None

    def new_monitor(self, report: Optional[ResourceMonitor.StatusReport] = None) -> ResourceMonitor:
        self.stop_monitor()
        self.monitor = ResourceMonitor(
            session=self._session,
            worker_id=self.worker_id,
            first_report_sec=3.0,
            report_frequency_sec=self._machine_update_interval,
            worker_tags=None if self._services_mode else self._worker_tags,
        )
        if self.monitor is not None:
            self.monitor.set_report(report)
            self.monitor.start()
        return self.monitor

    def dump_config(
        self,
        filename: Optional[str],
        config: Optional[backend_config.config.Config] = None,
        clean_api_credentials: bool = False,
    ) -> bool:
        current_content: Optional[str] = None
        if filename is not None:
            # noinspection PyBroadException
            try:
                current_content = Path(filename).read_text()
            except Exception:
                pass
        # noinspection PyBroadException
        try:
            config_data = (
                self._session.config.as_plain_ordered_dict() if config is None else config.as_plain_ordered_dict()
            )
            if clean_api_credentials:
                api = config_data.get("api")
                if api:
                    api.pop("credentials", None)

            new_content = six.text_type(json.dumps(config_data, cls=HOCONEncoder, indent=4))
            # Overwrite file only if the content is different, because we are mounting the same file  into
            # multiple containers in services mode, and we don't want to change it if we do not have to.
            if filename is not None and new_content != current_content:
                Path(filename).write_text(new_content)
            else:
                return False
        except Exception:
            return False
        return True

    def _log_command_output(
        self,
        task_id: str,
        cmd: Executable,
        stdout_path: str,
        stderr_path: Optional[str] = None,
        daemon: bool = False,
        cwd: Optional[str] = None,
        stop_signal: Optional[TaskStopSignal] = None,
        session: Optional[Session] = None,
        **kwargs: Any,
    ) -> Tuple[Optional[int], Optional[TaskStopReason]]:
        def _print_file(file_path: str, prev_pos: int = 0) -> Union[Tuple[List[str], int], Tuple[List[bytes], int]]:
            with open(file_path, "ab+") as f:
                f.seek(prev_pos)
                binary_text = f.read()
                if not self._truncate_task_output_files:
                    # non-buffered behavior
                    pos = f.tell()
                else:
                    # buffered - read everything and truncate
                    f.truncate(0)
                    pos = 0
            # skip the previously printed lines,
            blines = binary_text.split(b"\n") if binary_text else []
            if not blines:
                return blines, pos
            return (
                decode_binary_lines(
                    blines if blines[-1] else blines[:-1],
                    replace_cr=not self._suppress_cr,
                    overwrite_cr=self._suppress_cr,
                ),
                pos,
            )

        stdout = open(stdout_path, "wt")
        stderr = open(stderr_path, "wt") if stderr_path else stdout
        stdout_line_count, stdout_pos_count = 0, 0
        stderr_line_count, stderr_pos_count = 0, 0
        lines_buffer: Dict[str, Union[List[str], List[bytes]]] = defaultdict(list)  # type: ignore

        def report_lines(lines: Union[List[str], List[bytes]], source: str) -> int:
            if not self._truncate_task_output_files:
                # non-buffered
                return self.send_logs(task_id, lines, session=session)

            buffer = lines_buffer[source]
            buffer += lines  # type: ignore

            sent = self.send_logs(task_id, buffer, session=session)
            if sent > 0:
                lines_buffer[source] = buffer[sent:]
            return sent

        service_mode_internal_agent_started = None
        stopping = False
        status = None
        process = None
        # noinspection PyBroadException
        try:
            stop_reason = None

            process = cmd.call_subprocess(
                subprocess.Popen, stdout=stdout, stderr=stderr, cwd=cwd and str(cwd), **kwargs
            )

            while status is None and not stopping:

                stop_reason = stop_signal.test() if stop_signal else TaskStopSignal.default
                if stop_reason != TaskStopSignal.default:
                    # mark quit loop
                    stopping = True
                    if daemon:
                        self.send_logs(
                            task_id=task_id,
                            lines=["User aborted: stopping task ({})\n".format(str(stop_reason))],
                            level="ERROR",
                            session=session,
                        )
                        kill_all_child_processes(process.pid)
                else:
                    sleep(self._polling_interval)
                    status = process.poll()
                # flush stdout and stderr buffers
                if stdout:
                    stdout.flush()
                if stderr:
                    stderr.flush()

                # get diff from previous poll
                printed_lines, stdout_pos_count = _print_file(stdout_path, stdout_pos_count)
                if self._services_mode and not stopping and status is None:
                    # if the internal agent started, we stop logging, it will take over logging.
                    # if the internal agent started running the task itself, it will return status==0,
                    # then we can quit the monitoring loop of this process
                    printed_lines, service_mode_internal_agent_started, status = self._check_if_internal_agent_started(
                        printed_lines, service_mode_internal_agent_started, task_id
                    )
                    if status is not None:
                        stop_reason = TaskStopReason.service_started

                stdout_line_count += report_lines(printed_lines, "stdout")

                if stderr_path:
                    printed_lines, stderr_pos_count = _print_file(stderr_path, stderr_pos_count)
                    stderr_line_count += report_lines(printed_lines, "stderr")

        except subprocess.CalledProcessError as ex:
            # non zero return code
            stop_reason = TaskStopReason.exception
            status = ex.returncode
        except KeyboardInterrupt:
            # so someone else will catch us
            if process:
                kill_all_child_processes(process.pid)
            raise
        except Exception:
            # we should not get here, but better safe than sorry
            printed_lines, stdout_pos_count = _print_file(stdout_path, stdout_pos_count)
            stdout_line_count += report_lines(printed_lines, "stdout")
            if stderr_path:
                printed_lines, stderr_pos_count = _print_file(stderr_path, stderr_pos_count)
                stderr_line_count += report_lines(printed_lines, "stderr")
            stop_reason = TaskStopReason.exception
            status = -1

        # if running in services mode, keep the file open
        # in case the docker was so quick it started and finished, check the stop reason
        if (
            self._services_mode
            and service_mode_internal_agent_started
            and stop_reason == TaskStopReason.service_started
        ):
            return None, None

        # full cleanup (just in case)
        if process and not self._services_mode:
            kill_all_child_processes(process.pid)

        stdout.close()
        if stderr_path:
            stderr.close()

        # Send last lines
        printed_lines, stdout_pos_count = _print_file(stdout_path, stdout_pos_count)
        stdout_line_count += report_lines(printed_lines, "stdout")
        if stderr_path:
            printed_lines, stderr_pos_count = _print_file(stderr_path, stderr_pos_count)
            stderr_line_count += report_lines(printed_lines, "stderr")

        return status, stop_reason

    def _check_if_internal_agent_started(
        self,
        printed_lines: Union[List[str], List[bytes]],
        service_mode_internal_agent_started: Optional[bool],
        task_id: str,
    ) -> Tuple[Union[List[str], List[bytes]], Optional[bool], Optional[int]]:
        log_start_msg = self._task_logging_start_message.format(task_id)
        log_control_end_msg = self._task_logging_pass_control_message.format(task_id)
        filter_lines = printed_lines if not service_mode_internal_agent_started else []  # type: ignore
        for i, line in enumerate(printed_lines):
            if not service_mode_internal_agent_started and line.startswith(log_start_msg):  # type: ignore
                service_mode_internal_agent_started = True
                filter_lines = printed_lines[: i + 1]
            elif line.startswith(log_control_end_msg):  # type: ignore
                return filter_lines, service_mode_internal_agent_started, 0

        return filter_lines, service_mode_internal_agent_started, None

    def send_logs(
        self,
        task_id: str,
        lines: Union[List[str], List[bytes]],
        level: str = "DEBUG",
        session: Optional[Session] = None,
    ) -> int:
        """Send output lines as log events to backend"""
        if not lines:
            return 0
        print_text("".join(str(line) for line in lines), newline=False)

        # remove backspaces from the text log, they look bad.
        for i, l in enumerate(lines):
            lines[i] = l.replace("\x08", "")

        events_service = self.get_service(Events)
        try:
            events_service.send_log_events(self.worker_id, task_id=task_id, lines=lines, level=level, session=session)
            return len(lines)
        except Exception as e:
            print("\n### Error sending log: %s ###\n" % e)
            # revert number of sent lines (we will try next time)
            return 0

    def _apply_extra_configuration(self) -> None:
        try:
            self._session.load_vaults()
        except Exception as ex:
            print("Error: failed applying extra configuration: {}".format(ex))

        config = self._session.config
        default = config.get("agent.apply_environment", False)
        if ENV_ENABLE_ENV_CONFIG_SECTION.get(default=default):
            try:
                keys = apply_environment(config)
                if keys:
                    print("Environment variables set from configuration: {}".format(keys))
            except Exception as ex:
                print("Error: failed applying environment from configuration: {}".format(ex))

        default = config.get("agent.apply_files", default=False)
        if ENV_ENABLE_FILES_CONFIG_SECTION.get(default=default):
            try:
                apply_files(config)
            except Exception as ex:
                print("Error: failed applying files from configuration: {}".format(ex))

    def execute(
        self,
        task_id: str,
        log_level: str = "INFO",
        disable_monitoring: bool = False,
        require_queue: bool = False,
        log_file: Optional[str] = None,
        standalone_mode: Optional[bool] = None,
        clone: bool = False,
        projects_path: str = ".",
        venv_name: str = "venv",
        **_: Any,
    ) -> int:
        self._standalone_mode = standalone_mode

        if not task_id:
            raise CommandFailedError("Worker execute must have valid task id")

        try:
            current_task = self._session.api_client.tasks.get_by_id(task_id)
            if not current_task.id:
                pass
        except AttributeError:
            raise ValueError(
                "Could not find task id={} (for host: {})".format(task_id, self._session.config.get("api.host", ""))
            )
        except Exception as ex:
            raise ValueError(
                "Could not find task id={} (for host: {})\nException: {}".format(
                    task_id, self._session.config.get("api.host", ""), ex
                )
            )

        if clone:
            try:
                print("Cloning task id={}".format(task_id))
                current_task = self._session.api_client.tasks.get_by_id(
                    self._session.send_api(
                        tasks_api.CloneRequest(
                            task=current_task.id, new_task_name="Clone of {}".format(current_task.name)
                        )
                    ).id
                )
                print("Task cloned, new task id={}".format(current_task.id))
            except Exception:
                raise CommandFailedError("Cloning failed")
        else:
            # make sure this task is not stuck in an execution queue, it shouldn't have been, but just in case.
            # noinspection PyBroadException
            try:
                res = self._session.api_client.tasks.dequeue(task=current_task.id)
                if require_queue and res.meta.result_code != 200:
                    raise ValueError(
                        "Execution required enqueued task, " "but task id={} is not queued.".format(current_task.id)
                    )
            except Exception:
                if require_queue:
                    raise

        clearml_task = Task.get_task(task_id)
        project_name = clearml_task.get_project_name()
        script_dir = os.path.join(projects_path, project_name)
        venv_path = os.path.join(venv_name, "bin", current_task.script.binary)

        args = chain.from_iterable(
            (f"--{parameter_name[5:]}", value)
            for parameter_name, value in clearml_task.get_parameters().items()
            if parameter_name.startswith("Args/")
        )

        self._apply_extra_configuration()

        self._session.print_configuration()

        # now mark the task as started
        self._session.api_client.tasks.started(
            task=current_task.id,
            status_reason="worker started execution",
            status_message=self._task_status_change_message,
            force=True,
        )

        if not disable_monitoring:
            self.log.debug("starting resource monitor")
            self.report_monitor(ResourceMonitor.StatusReport(task=current_task.id))

        execution = self.get_execution_info(current_task)

        print("\n")

        # run code
        # print("Running task id [%s]:" % current_task.id)
        print(self._task_logging_pass_control_message.format(current_task.id))

        command = Argv(venv_path, current_task.data.script.entry_point, *args)
        print("[{}]$ {}".format(execution.working_dir, command.pretty()))

        sdk_env = {
            # config_file updated in session.py
            "task_id": current_task.id,
            "log_level": log_level,
            "log_to_backend": "0",
            "config_file": self._session.config_file,  # The config file is the tmp file that clearml_agent created
        }
        os.environ.update(
            {sdk_key: str(value) for key, value in sdk_env.items() for sdk_key in ENVIRONMENT_SDK_PARAMS[key]}
        )

        use_execv = is_linux_platform() and not isinstance(self.package_api, (PoetryAPI, CondaAPI))

        self._session.api_client.tasks.started(
            task=current_task.id,
            status_reason="worker starting task execution",
            status_message=self._task_status_change_message,
            force=True,
        )

        # check if we need to add encoding to the subprocess
        if sys.getfilesystemencoding() == "ascii" and not os.environ.get("PYTHONIOENCODING"):
            os.environ["PYTHONIOENCODING"] = "utf-8"

        print("Starting Task Execution: {}\n".format(current_task.id))

        exit_code = -1
        try:
            if disable_monitoring:
                try:
                    sys.stdout.flush()
                    sys.stderr.flush()
                    os.chdir(script_dir)
                    if use_execv:
                        os.execv(command.argv[0].as_posix(), tuple([command.argv[0].as_posix()]) + command.argv[1:])
                    else:
                        exit_code = command.check_call(cwd=script_dir)
                        exit(exit_code)
                except subprocess.CalledProcessError as ex:
                    # non zero return code
                    exit_code = ex.returncode
                    if not use_execv:
                        exit(exit_code)
                except Exception as ex:
                    if not use_execv:
                        exit(-1)
                    raise ex
            else:
                # store stdout/stderr into file, and send to backend
                temp_stdout_fname = log_file or safe_mkstemp(
                    suffix=".txt", prefix=".clearml_agent_out.", name_only=True
                )
                print("Storing stdout and stderr log into [%s]" % temp_stdout_fname)
                exit_code, _ = self._log_command_output(  # type: ignore
                    task_id=current_task.id, cmd=command, stdout_path=temp_stdout_fname, cwd=script_dir
                )
        except KeyboardInterrupt:
            self.handle_user_abort(current_task.id)
            raise
        except Exception as e:
            self.log.warning(str(e))
            self.log_traceback(e)
            exit_code = -1

        # kill leftover processes
        kill_all_child_processes()

        # if we return ExitStatus.interrupted==2,
        # it means user aborted, KeyboardInterrupt should have caught it,
        # that cannot happen when running with disable monitoring
        exit_code = exit_code if exit_code != ExitStatus.interrupted else -1

        if not disable_monitoring:
            # we need to change task status according to exit code
            self.handle_task_termination(current_task.id, exit_code, TaskStopReason.no_stop)
            self.stop_monitor()
            # unregister the worker
            self._unregister()

        return 1 if exit_code is None else exit_code

    def get_execution_info(self, current_task) -> ExecutionInfo:  # type: ignore
        # current_task type: clearml_agent.backend_api.session.client.client.Task
        try:
            execution = ExecutionInfo.from_task(current_task)
        except Exception as e:
            self.error("Could not parse task execution info: {}".format(e.args[0]))
            current_task.failed(status_reason=e.args[0], status_message=self._task_status_change_message)
            self.exit(e.args[0])
        if "\\" in execution.working_dir:
            warning(
                'Working dir "{}" contains backslashes. '
                "All path separators must be forward slashes.".format(execution.working_dir)
            )

        print("Executing task id [%s]:" % current_task.id)
        sanitized_execution = attr.evolve(
            execution,
            docker_cmd=" ".join(  # type: ignore
                self._sanitize_docker_command(shlex.split(execution.docker_cmd or ""))
            ),
        )
        for pair in attr.asdict(sanitized_execution).items():
            print("{} = {}".format(*pair))
        print()
        return execution

    def handle_task_termination(
        self, task_id: str, exit_code: int, stop_reason: TaskStopReason, session: Session = None
    ) -> None:
        session = session or self._session
        try:
            if stop_reason == TaskStopReason.stopped:
                self.log("Stopping - tasks.stop was called for task")
                self.send_logs(task_id, ["Process aborted by user"], session=session)
                session.send_api(
                    tasks_api.StoppedRequest(
                        task=task_id,
                        status_reason="task was stopped by tasks.stop",
                        status_message=self._task_status_change_message,
                    )
                )

            elif stop_reason == TaskStopReason.status_changed:
                try:
                    task_status = get_task(session, task_id, only_fields=["status"]).status
                    self.log(
                        "Task status changed unexpectedly (status: {}), terminating task process.".format(task_status)
                    )
                except Exception as ex:
                    self.log(
                        "Task status changed unexpectedly. Was not able to obtain the current status: "
                        "{}: {}".format(type(ex), ex)
                    )
                    self.log_traceback(ex)

            elif stop_reason == TaskStopReason.reset:
                self.log("Task was reset unexpectedly")

            elif stop_reason == TaskStopReason.no_stop:
                self.handle_task_process_termination(task_id, exit_code, session=session)

            elif stop_reason == TaskStopReason.not_found:
                self.log("Task not found")

            else:
                self.log("INTERNAL ERROR: unidentified task stop reason: {}".format(stop_reason))

        except Exception as e:
            # task probably set its own status
            self.log("Warning: could not update task id '{}' status. Task exit code {}".format(task_id, exit_code))
            self.log_traceback(e)

    def handle_task_process_termination(self, task_id: str, exit_code: int, session: Session = None) -> None:
        session = session or self._session
        self.log("Task process terminated")

        if exit_code == COMMAND_SUCCESS:
            self.log("Task success: completing")
            self.send_logs(task_id, ["Process completed successfully"], session=session)
            session.send_api(
                tasks_api.CompletedRequest(
                    task=task_id,
                    status_reason="worker execution done",
                    status_message=self._task_status_change_message,
                )
            )
        elif exit_code in (ExitStatus.interrupted, 256 + ExitStatus.interrupted):
            self.log("Task interrupted: stopping")
            self.send_logs(task_id, ["Process terminated by user"], session=session)
            session.send_api(
                tasks_api.StoppedRequest(
                    task=task_id, status_reason="user abort", status_message=self._task_status_change_message
                )
            )
        else:
            self.log("Task failure: setting status to 'failed'")
            self.send_logs(task_id, ["Process failed, exit code {}".format(exit_code)], session=session)
            session.send_api(
                tasks_api.FailedRequest(
                    task=task_id,
                    status_reason="worker execution exit code {}".format(exit_code),
                    status_message=self._task_status_change_message,
                )
            )

    def _register(self, queues: Sequence[str] = ()) -> None:
        self.queues = queues
        try:
            self.get("register", worker=self.worker_id, queues=queues)
            # If we got here - we've registered
            self._worker_registered = True
        except Exception as e:
            self.log("Worker failed registering itself with backend service: {}".format(e))

    def _unregister(self, queues: Sequence[str] = ()) -> None:
        self.queues = ()
        try:
            self.get("unregister", worker=self.worker_id, queues=queues)
            self._worker_registered = False
        except Exception as e:
            self.log("Worker failed unregistering itself with backend service: {}".format(e))

    def log_traceback(self, err: Exception) -> None:
        if isinstance(err, APIError):
            tb = err.get_traceback()
            if tb:
                print("Server traceback:\n{}".format(tb))
        if self._session.debug_mode:
            self.log(traceback.format_exc())

    def _kill_daemon(self, dynamic_gpus: bool = False) -> bool:
        worker_id, worker_name = self._generate_worker_id_name(dynamic_gpus=dynamic_gpus)

        # Iterate over all running process
        for pid, uid, slot, file in sorted(Singleton.get_running_pids(), key=lambda x: x[1] or ""):
            if pid < 0 or uid is None:
                continue

            # if dynamic gpus kill all children
            if dynamic_gpus and uid == worker_id:
                print("Terminating clearml-agent worker_id={} pid={}".format(uid, pid))
                if not terminate_process(pid, timeout=120):
                    warning("Could not terminate process pid={}".format(pid))
                return True

            # either we have a match for the worker_id or we just pick the first one, and kill it.
            if (worker_id and uid == worker_id) or (not worker_id and uid.startswith("{}:".format(worker_name))):
                # this is us kill it
                print("Terminating clearml-agent worker_id={} pid={}".format(uid, pid))
                timeout = 120 if uid.startswith("{}:dgpu".format(worker_name)) else 10
                if not terminate_process(pid, timeout=timeout):
                    error("Could not terminate process pid={}".format(pid))
                return True

        print(
            "Could not find a running clearml-agent instance with worker_name={} worker_id={}".format(
                worker_name, worker_id
            )
        )
        return False

    def _singleton(self, dynamic_gpus: bool = False) -> None:
        # ensure singleton
        worker_id, worker_name = self._generate_worker_id_name(dynamic_gpus=dynamic_gpus)

        # if we are running in services mode, we allow double register since
        # docker-compose will kill instances before they cleanup
        self.worker_id, worker_slot = Singleton.register_instance(
            unique_worker_id=worker_id,
            worker_name=worker_name,
            api_client=self._session.api_client,
            allow_double=bool(ENV_DOCKER_HOST_MOUNT.get()),  # and bool(self._services_mode),
        )

        if self.worker_id is None:
            error("Instance with the same WORKER_ID [{}] is already running".format(worker_id))
            exit(1)
        # update folders based on free slot
        self._session.create_cache_folders(slot_index=worker_slot)

    def _generate_worker_id_name(self, dynamic_gpus: bool = False) -> Tuple[str, str]:
        worker_id = self._session.config["agent.worker_id"]
        worker_name = self._session.config["agent.worker_name"]
        if not worker_id and os.environ.get("NVIDIA_VISIBLE_DEVICES") is not None:
            nvidia_visible_devices = os.environ.get("NVIDIA_VISIBLE_DEVICES")
            if nvidia_visible_devices and nvidia_visible_devices.lower() != "none":
                worker_id = "{}:{}gpu{}".format(worker_name, "d" if dynamic_gpus else "", nvidia_visible_devices)
            elif nvidia_visible_devices == "":
                pass
            else:
                worker_name = "{}:cpu".format(worker_name)
        return worker_id, worker_name

    def _resolve_queue_names(self, queues: List[str], create_if_missing: bool = False) -> List[str]:
        if not queues:
            # try to look for queues with "default" tag
            try:
                default_queue = self._session.send_api(queues_api.GetDefaultRequest())
                return [default_queue.id]
            except APIError:
                # if we cannot find one with "default" tag, look for a queue named "default"
                queues = ["default"]

        queues = return_list(queues)
        if not create_if_missing:
            return [self._resolve_name(q, "queues") for q in queues]

        queue_ids = []
        for q in queues:
            try:
                q_id = self._resolve_name(q, "queues")
            except Exception as ex:
                print("que name resolving failed with exception:", ex, "\ntrying again...")
                self._session.send_api(queues_api.CreateRequest(name=q))
                q_id = self._resolve_name(q, "queues")
                print("que name resolving done!")
            queue_ids.append(q_id)
        return queue_ids

    def _sanitize_docker_command(self, docker_command: List[str]) -> List[str]:
        if not docker_command:
            return docker_command
        if not self._session.config.get("agent.hide_docker_command_env_vars.enabled", False):
            return docker_command

        keys = set(self._session.config.get("agent.hide_docker_command_env_vars.extra_keys", []))
        keys.update(
            ENV_AGENT_GIT_PASS.vars,
            ENV_AGENT_SECRET_KEY.vars,
            ENV_AWS_SECRET_KEY.vars,
            ENV_AZURE_ACCOUNT_KEY.vars,
            ENV_AGENT_AUTH_TOKEN.vars,
        )

        result = docker_command[:]
        for i, item in enumerate(docker_command):
            try:
                if item not in ("-e", "--env"):
                    continue
                key, sep, _ = result[i + 1].partition("=")
                if key not in keys or not sep:
                    continue
                result[i + 1] = "{}={}".format(key, "********")
            except KeyError:
                pass

        return result


if __name__ == "__main__":
    pass
