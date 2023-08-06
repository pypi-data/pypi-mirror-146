from os.path import join, abspath

from alice.runners.pythonrunner import PythonRunner
from alice.runners.pypirunner import PyPiRunner
from alice.exceptions import ConfigException


class Factory():
    def __init__(self, verbose, globals, runner_configs) -> None:
        self.verbose = verbose
        self.globals = globals
        self.runner_configs = {}
        self.runnertypes = {}
        self.runners = {}
        self.__load_runners()
        self.__gen_runner_configs(runner_configs)

    def __load_runners(self):
        # TODO: Runners can be imported via cli too
        # https://git.gyulai.cloud/gyulaid/alice/issues/4
        # module = __import__("module_file")
        # my_class = getattr(module, "class_name")
        self.runnertypes = {"python": PythonRunner,
                            "pypi": PyPiRunner}

        if (self.verbose):
            print(f"[Alice] Available runners: {'|'.join(self.runnertypes.keys())}")

    def __gen_runner_configs(self, config):
        for runnertype, runnerconfig in config.items():
            if runnertype != "global":
                if (self.verbose):
                    print(f"[Alice] Global config found for runner {runnertype}")
                config = self.globals.copy()
                for key, value in runnerconfig.items():
                    if key == "env":
                        for env_var in value:
                            config["env"][env_var["name"]] = env_var["value"]
                    elif key == "workdir":
                        config["workdir"] = abspath(join(config["workdir"], value))
                    else:
                        config[key] = value
                self.runner_configs[runnertype] = config

    def get_runner(self, runnertype):
        if runnertype not in self.runners:
            if runnertype in self.runnertypes:
                if (self.verbose):
                    print(f"[Alice] Initializing runner: {runnertype}")
                params = {
                    "verbose": self.verbose
                }
                # If there is a runner specific config, use that, else global
                config = self.runner_configs.get(runnertype, self.globals.copy())
                self.runners[runnertype] = self.runnertypes[runnertype](params, config)
            else:
                raise ConfigException(f"Invalid runner type: {runnertype}")
        return self.runners[runnertype]
