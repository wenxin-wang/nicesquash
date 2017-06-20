import argparse
from config import Config
from manager import Manager


def get_args():
    parser = argparse.ArgumentParser(
        description='Simple Manager and Monitor for NiceHash')
    parser.add_argument('-d', '--directory', help='working directory')
    parser.add_argument(
        '-b',
        '--benchmark',
        action='store_true',
        help='whether to do benchmark'
    )
    return parser.parse_args()


def main():
    args = get_args()
    conf = Config(args.directory)
    conf.read()
    conf.benchmark = args.benchmark
    m = Manager(conf)
    m.kickOff()


if __name__ == '__main__':
    main()
