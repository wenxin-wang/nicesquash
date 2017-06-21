import argparse
import asyncio as aio
import aiohttp

from config import Config
from manager import Manager


def get_args():
    parser = argparse.ArgumentParser(
        description='Simple Manager and Monitor for NiceHash')
    parser.add_argument('-d', '--directory', help='working directory')
    parser.add_argument('-s', '--session', help='tmux session')
    parser.add_argument(
        '-b',
        '--benchmark',
        action='store_true',
        help='whether to do benchmark'
    )
    return parser.parse_args()


async def main(loop):
    args = get_args()
    conf = Config(args.directory)
    conf.read()
    conf.benchmark = args.benchmark
    conf.session = args.session
    m = Manager(conf, loop)
    await m.kickOff()


if __name__ == '__main__':
    loop = aio.get_event_loop()
    loop.run_until_complete(main(loop))
