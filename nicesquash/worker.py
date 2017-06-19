import json
from datetime import datetime

from api import NiceHashAPI
from config import dict_to_object


class Worker:
    def __init__(self, gpu, conf):
        self.gpu = dict_to_object(gpu)
        self.cwd = conf.cwd
        self.config = conf.config
        self.algos = conf.algos
        min_wait = self.config.nicehash.min_wait
        self.nicehash = NiceHashAPI(self.gpu.address, min_wait)
        self.miner = None
        self.clog_p = self.cwd / 'logs' / ('gpu-%s-cur.log' % self.gpu.gpu_id)
        self.clog_p.touch()

    def read_heuristics(self):
        h = self.cwd / ("gpu_heuristics_%d.json" % self.gpu.gpu_id)
        if not h.exists():
            return
        with open(h) as f:
            self.heurisitcs = json.load(f)
        return self.heurisitcs

    def start(self):
        if not self.config.benchmark:
            assert self.read_heuristics()
        if self.config.benchmark:
            self.benchmark()
        else:
            self.run()

    def benchmark(self):
        print(self.nicehash.get_prices())
        self.exec(None)

    def exec(self, miner_type):
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_p = self.cwd / 'logs' / ('gpu-%s-%s.log' % (now, self.gpu.gpu_id))
        if self.clog_p.exists():
            self.clog_p.unlink()
        self.clog_p.symlink_to(log_p)
        log_p.touch()
        # self.miner = miner_type(self.gpu, self.algos)
