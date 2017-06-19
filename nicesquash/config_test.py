from config import Config
from pathlib import Path

conf = Config(Path(__file__).parent)


def read_yaml():
    print(conf.read_miner_algo())


if __name__ == '__main__':
    read_yaml()
