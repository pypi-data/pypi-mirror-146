import os
import argparse

from alice.configparser import ConfigParser
from alice.exceptions import ConfigException, NonZeroRetcode, RunnerError


def gen_env(param_list):
    env_vars = {}
    for item in param_list:
        item_parts = item.split("=")
        if len(item_parts) == 2:
            env_vars[item_parts[0]] = item_parts[1]
        else:
            raise ConfigException(f"Invalid parameter: {item}")
    return env_vars


def parse_jobs(args):
    try:
        if len(args.env) > 0:
            envs = gen_env(args.env)
            if args.verbose:
                print(f"[Alice] Env vars from CLI: {envs}")
        jobParser = ConfigParser(args.input, gen_env(args.env), args.verbose)

        for step in args.steps:
            jobParser.execute(step)
    except ConfigException as e:
        print(f"Configuration error-> {e}")
        exit(1)
    except NonZeroRetcode:
        print("[Alice] FAILED")
        exit(1)
    except RunnerError as e:
        print(f"RunnerError-> {e}")


def main():
    parser = argparse.ArgumentParser(prog="alice")
    parser.add_argument("steps", nargs='*', default=["default"])
    parser.add_argument("-i", "--input", default="alice-ci.yaml")
    parser.add_argument("-e", "--env", nargs='*', default=[])
    parser.add_argument("-a", "--addrunner", nargs='*', default=[])
    parser.add_argument("-v", "--verbose", action='store_true')
    args = parser.parse_args()
    if not os.path.isfile(args.input):
        print(f"No such file: {args.input}")
        exit(1)
    parse_jobs(args)


if __name__ == "__main__":
    main()
