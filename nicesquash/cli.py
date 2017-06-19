import argparse
from config import Config
from scheduler import Scheduler


def get_args():
    parser = argparse.ArgumentParser(
        description='Simple Scheduler and Monitor for NiceHash')
    parser.add_argument('-d', '--directory', help='working directory')
    parser.add_argument(
        '-b',
        '--benchmark',
        type=int,
        default=None,
        help='Run benchmark, set stable time (default 30)')
    return parser.parse_args()


def main():
    args = get_args()
    conf = Config(args.directory)
    conf.read()
    conf.config.benchmark = args.benchmark
    s = Scheduler(conf)
    s.kickOff()


if __name__ == '__main__':
    main()
