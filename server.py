import sys

from app import run
from app.config import init_config

from utils import usage_exit


def main():
    args = sys.argv[1:]

    # env_settings
    if len(args) > 1 and args[0] in ['-e', '--env']:
        env = args[1]
        args = args[2:]
    else:
        env = 'develop'

    # help
    if len(args) > 0 and args[0] in ['-h', '--help']:
        usage_exit()

    # config_initialize
    try:
        init_config(env=env)
    except Exception as e:
        print(e)
        exit(1)

    run(env=env)


if __name__ == '__main__':
    main()
