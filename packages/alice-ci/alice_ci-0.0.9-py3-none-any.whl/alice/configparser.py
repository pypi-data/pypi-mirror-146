from os import getcwd, path, environ
import subprocess
import yaml

from alice.exceptions import ConfigException
from alice.runnerfactory import Factory


class ConfigParser:
    def __init__(self, file_path, cli_env_vars, verbose=False) -> None:
        self.verbose = verbose
        with open(file_path) as f:
            self.config = yaml.safe_load(f)
        self.factory = Factory(verbose, self.__gen_globals(cli_env_vars), self.config.get("runners", {}))
        self.jobs = self.__get_jobs()
        self.pipelines = self.config.get("pipelines", {})

    # Initialize env and workdir if not present in global
    def __gen_globals(self, cli_vars):
        env_vars = environ.copy()
        env_vars.update(cli_vars)
        globals = {
            "env": env_vars,
            "workdir": getcwd()
        }
        if "runners" in self.config:
            if "global" in self.config["runners"]:
                if "env" in self.config["runners"]["global"]:
                    for var in self.config["runners"]["global"]["env"]:
                        globals["env"][var["name"]] = var["value"]
                if "workdir" in self.config["runners"]["global"]:
                    globals["workdir"] = self.config["runners"]["global"]["workdir"]

        if (self.verbose):
            print(f"[Alice] Configured globals: {globals}")
        return globals

    def __get_jobs(self):
        if "jobs" in self.config:
            jobs = {}
            for job_spec in self.config["jobs"]:
                name = job_spec["name"]
                if name in jobs:
                    raise ConfigException(f"Job with name {name} already exists!")

                jobs[name] = job_spec
            if (self.verbose):
                print(f"[Alice] Parsed jobs: {', '.join(jobs.keys())}")
            return jobs
        else:
            raise ConfigException("No jobs defined in config")

    def __is_changed(self, changes):
        try:
            target = changes["branch"]
            paths = []
            for _path in changes["paths"]:
                paths.append(path.abspath(_path))
            # TODO: Error handling
            command = ["git", "diff", "--name-only", target]
            with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
                p.wait()
                for line in p.stdout:
                    change_path = path.abspath(line.decode("UTF-8").strip())
                    for _path in paths:
                        spec_path = path.abspath(_path)
                        if change_path.startswith(spec_path):
                            if self.verbose:
                                print(f"[Alice] Modified file: {change_path}")
                                print(f"[Alice] Path match: {_path}")
                            return True
        except KeyError:
            raise ConfigException(f"Invalid 'changes' config: {changes}")
        return False

    def execute(self, task_name):
        if task_name in self.jobs:
            self.execute_job(task_name)
        elif task_name in self.pipelines:
            print(f"[Alice][Pipeline] {task_name}: Start")
            self.execute_pipeline(task_name)
            print(f"[Alice][Pipeline] {task_name}: Success")
        else:
            raise ConfigException(f"No such job or pipeline: {task_name}")

    def execute_pipeline(self, pipeline_name):
        if pipeline_name in self.pipelines:
            for job in self.pipelines[pipeline_name]:
                self.execute_job(job)

    def execute_job(self, job_name):
        if job_name in self.jobs:
            print(f"[Alice][Job] {job_name}: Start")
            job_spec = self.jobs[job_name]
            should_run = True
            if "changes" in job_spec:
                should_run = self.__is_changed(job_spec["changes"])
            if should_run:
                runner = self.factory.get_runner(job_spec["type"])
                runner.run(job_spec)
                status = "SUCCESS"
            else:
                status = "SKIP, no change detected"
            print(f"[Alice][Job] {job_name}: {status}")
