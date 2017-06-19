from yaml import load as yaml_load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from pathlib import Path


class Config:
    miner_algo = 'miner_algo.yml'
    config_file = 'config.yml'

    def __init__(self, cwd):
        self.cwd = Path(cwd)

    def read(self):
        self.read_miner_algo()
        self.read_config()

    def read_config(self):
        p = self.cwd / self.config_file
        with open(p) as f:
            config = yaml_load(f)
        nicehash = config.get('nicehash')
        if not nicehash:
            nicehash = {}
            config['nicehash'] = nicehash
        if 'min_wait' not in nicehash:
            nicehash['min_wait'] = None
        self.config = dict_to_object(config)
        return self.config

    def read_miner_algo(self):
        p = self.cwd / self.miner_algo
        with open(p) as f:
            _m = yaml_load(f, Loader=Loader)
        algos = {}
        for m in ['ccminer']:
            m = _m[m]
            for n, c in m.items():
                algos[n] = ('ccminer', c)
        for a, m in _m['other'].items():
            algos[a] = m
        self.algos = dict_to_object(algos)
        return self.algos


class Conf:
    pass

def dict_to_object(d):
    o = Conf()
    for k, v in d.items():
        if type(v) is dict:
            setattr(o, k, dict_to_object(v))
        else:
            setattr(o, k, v)
    return o
