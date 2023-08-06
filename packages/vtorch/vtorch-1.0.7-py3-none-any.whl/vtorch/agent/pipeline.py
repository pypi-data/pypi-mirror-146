import os
from typing import Dict, List

from clearml import Task
from clearml.backend_config import ConfigurationError

from vtorch.training.logging_util import get_results_subfolder_hierarchy


class EnqueueExperiments:
    """
    Usage example:
    ```
    pipeline = EnqueueExperiments(
    project_name="ys-ds-unlim-aspects",
    task_commands=[
            "run.py --config configs/train_model/eng/nn/sslc_rest.py --experiment_name_suffix enqueued1",
            "run.py --config configs/train_model/eng/nn/sslc_lapt.py --experiment_name_suffix enqueued2",
        ],
    )
    ```
    """

    def __init__(self, project_name: str, task_commands: List[str], queue_name: str = "default"):
        self.task_commands = task_commands
        self.project_name = project_name
        self.queue_name = queue_name

    def run(self) -> None:
        for command in self.task_commands:
            entry_point, *args = command.split()
            # note: only paired arguments works here
            # like --config path_to_config --next_argument_name next_argument_value ...
            # but not --config path_to_config --next_argument_name --one_more_argument
            argparse_arguments = {}
            for i in range(0, len(args), 2):
                argparse_arguments[args[i][2:]] = args[i + 1]

            task = Task.create(
                script=entry_point,
                project_name=self.project_name,
                task_name=self._task_name_from_args(argparse_arguments),
            )

            task.connect(argparse_arguments, "Args")
            Task.enqueue(task, queue_name=self.queue_name)

    @staticmethod
    def _task_name_from_args(args: Dict[str, str]) -> str:
        config_py = args.get("config")
        if config_py is None:
            raise ConfigurationError("command missed `--config` argument")
        experiment_name_suffix = args.get("experiment_name_suffix")
        if experiment_name_suffix is None:
            raise ConfigurationError("command missed `--experiment_name_suffix` argument")
        results_subfolder_hierarchy = f"{get_results_subfolder_hierarchy(config_py)}_{experiment_name_suffix}"
        return results_subfolder_hierarchy.replace(os.path.sep, "_")
