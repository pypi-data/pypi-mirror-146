import argparse

from vtorch.agent.worker import Worker


def execute(args: argparse.Namespace) -> None:
    _worker = Worker(cpu_only=args.cpu_only, gpus=args.gpus)
    _worker.execute(
        task_id=args.id,
        log_level=args.log_level,
        disable_monitoring=args.disable_monitoring,
        require_queue=args.require_queue,
        log_file=args.log_file,
        standalone_mode=args.standalone_mode,
        clone=args.clone,
        projects_path=args.projects_path,
        venv_name=args.venv_name,
    )


def daemon(args: argparse.Namespace) -> None:
    _worker = Worker(debug=args.debug, cpu_only=args.cpu_only, gpus=args.gpus)
    _worker.daemon(
        queues=args.queues,
        venv_names=args.venv_names,
        projects_paths=args.projects_paths,
        log_level=args.log_level,
        foreground=args.foreground,
        detached=args.detached,
        order_fairness=args.order_fairness,
        child_report_tags=args.child_report_tags,
        use_owner_token=args.use_owner_token,
        standalone_mode=args.standalone_mode,
        services_mode=args.services_mode,
        uptime=args.uptime,
        downtime=args.downtime,
        stop=args.stop,
        create_queue=args.create_queue,
        status=args.status,
        gpus=args.gpus,
        dynamic_gpus=args.dynamic_gpus,
    )


def main() -> None:
    common_args_parser = argparse.ArgumentParser(add_help=False)
    common_args_parser.add_argument(
        "--standalone-mode",
        action="store_true",
        help="Do not use any network connects, assume everything is pre-installed",
    )
    common_args_parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARN", "WARNING", "ERROR", "CRITICAL"],
        help="{DEBUG,INFO,WARN,WARNING,ERROR,CRITICAL} | default is INFO",
    )
    common_args_parser.add_argument(
        "--gpus",
        type=str,
        help="Specify active GPUs to use Equivalent to setting NVIDIA_VISIBLE_DEVICES "
        "Examples: --gpus 0 or --gpu 0,1,2 or --gpus all",
    )
    common_args_parser.add_argument("--cpu-only", action="store_true", help="Disable GPU access, only use CPU")

    # execute single / daemon
    parser = argparse.ArgumentParser(add_help=False)
    subparsers = parser.add_subparsers()
    execute_parser = subparsers.add_parser("execute", parents=[common_args_parser])
    execute_parser.add_argument("--id", type=str, required=True, help="Task ID to run")
    execute_parser.add_argument(
        "--log-file", type=str, required=False, help="Output task execution (stdout/stderr) into text file"
    )
    execute_parser.add_argument(
        "--disable-monitoring", action="store_true", help="Disable logging & monitoring (stdout is still visible)"
    )
    execute_parser.add_argument(
        "--projects-path",
        type=str,
        default=".",
        help="path where your projects are located (e.g '~/.' if your projects are located " "in the home directory)",
    )
    execute_parser.add_argument("--venv-name", type=str, default="venv", help="venv name")
    execute_parser.add_argument(
        "--require-queue",
        action="store_true",
        help="If the specified task is not queued (in any Queue), the execution will fail.",
    )
    execute_parser.add_argument(
        "--clone",
        action="store_true",
        help="Clone the experiment before execution, and execute the cloned experiment)",
    )
    execute_parser.set_defaults(func=execute)

    daemon_parser = subparsers.add_parser("daemon", parents=[common_args_parser])
    daemon_parser.add_argument(
        "--foreground",
        action="store_true",
        help="Pipe full log to stdout/stderr, should not be used if running in background",
    )
    daemon_parser.add_argument("--queues", nargs="+", required=True, help="queue ids/names to pull tasks from")
    daemon_parser.add_argument(
        "--projects-paths",
        nargs="+",
        required=True,
        help="paths where projects are located in the same order as --queues are specified",
    )
    daemon_parser.add_argument(
        "--venv-names", nargs="+", default=None, help="venv names in the same order as --queues are specified"
    )
    daemon_parser.add_argument("--debug", action="store_true")
    daemon_parser.add_argument(
        "--order-fairness",
        action="store_true",
        help="Pull from each queue in a round-robin order, instead of priority order.",
    )
    daemon_parser.add_argument("--services-mode", action="store_true")
    daemon_parser.add_argument(
        "--child-report-tags",
        nargs="+",
        help="List of tags to send with the status reports from the worker that runs a task",
    )
    daemon_parser.add_argument(
        "--create-queue", action="store_true", help="Create requested queue if it does not exist already."
    )
    daemon_parser.add_argument("--detached", action="store_true", help="Detached mode, run agent in the background")
    daemon_parser.add_argument(
        "--stop", action="store_true", help="Stop the running agent (based on the same set of arguments)"
    )
    daemon_parser.add_argument(
        "--dynamic-gpus",
        action="store_true",
        help="Allow to dynamically allocate gpus based on queue properties, configure with "
        "'--queue <queue_name>=<num_gpus>'. Example: '--dynamic-gpus --gpus 0-3 --queue "
        "dual_gpus=2 single_gpu=1' Example Opportunistic: '--dynamic-gpus --gpus 0-3 "
        "--queue dual_gpus=2 max_quad_gpus=1-4",
    )
    daemon_parser.add_argument(
        "--uptime",
        type=str,
        help="Specify uptime for clearml-agent in '<hours> <days>' format. for example, use "
        "'17-20 TUE' to set Tuesday's uptime to 17-20Note: Make sure to have only one of "
        "uptime/downtime configuration and not both.",
    )
    daemon_parser.add_argument(
        "--downtime",
        type=str,
        help="Specify downtime for clearml-agent in '<hours> <days>' format. for example, use "
        "'09-13 TUE' to set Tuesday's downtime to 09-13Note: Make sure to have only on of "
        "uptime/downtime configuration and not both.",
    )
    daemon_parser.add_argument(
        "--status",
        action="store_true",
        help="Print the worker's schedule (uptime properties, server's runtime properties and " "listening queues)",
    )
    daemon_parser.add_argument(
        "--use-owner-token",
        action="store_true",
        help="Generate and use task owner token for the execution of the task",
    )
    daemon_parser.set_defaults(func=daemon)

    arguments = parser.parse_args()
    arguments.func(arguments)


if __name__ == "__main__":
    main()
