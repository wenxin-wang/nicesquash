import json
from datetime import datetime

from api import NiceHashAPI
from config import dict_to_object
from miners import miner_types


class Worker:
    def __init__(self, gpu, conf, loop):
        self.loop = loop
        self.gpu = dict_to_object(gpu)
        self.cwd = conf.cwd
        self.config = conf.config
        self.algos = conf.algos
        self.session = conf.session
        self.is_benchmark = conf.benchmark
        min_wait = self.config.nicehash.min_wait
        self.nicehash = NiceHashAPI(self.gpu.address, min_wait)
        self.miner = None

    def read_heuristics(self):
        h = self.cwd / ("gpu_heuristics_%d.json" % self.gpu.gpu_id)
        if not h.exists():
            return
        with open(h) as f:
            self.heurisitcs = json.load(f)
        return self.heurisitcs

    async def start(self):
        if not self.is_benchmark:
            assert self.read_heuristics()
        if self.is_benchmark:
            await self.benchmark()
        else:
            await self.run()

    async def benchmark(self):
        for algo, algo_conf in self.filter_algos():
            await self.exec(algo, algo_conf)

    def filter_algos(self):
        prices = self.nicehash.get_prices()
        algos = []
        for algo in prices:
            algo_conf = getattr(self.algos, algo['name'], None)
            if algo_conf:
                algos.append((algo, algo_conf))
        return algos

    async def exec(self, algo, algo_conf):
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_p = self.cwd / 'logs' / ('gpu-%s-%s-%s.log' % (self.gpu.gpu_id,
                                                           now, algo['name']))
        if type(algo_conf) is tuple:
            miner_type = miner_types[algo_conf[0]]
            self.miner = miner_type(
                *algo_conf[1:],
                algo=algo,
                gpu=self.gpu,
                log_p=log_p,
                session=self.session,
                loop=self.loop)
        else:
            miner_type = miner_types[algo_conf]
            self.miner = miner_type(algo, self.gpu, log_p, self.session,
                                    self.loop)
        await self.miner.exec()
