import time
import asyncio as aio
import aiohttp


class NiceHashAPI:
    api_url = 'https://api.nicehash.com/api?'
    last_req_time = None

    def __init__(self, addr, min_wait, loop):
        self.addr = addr
        self.prices = None
        self.stats = None
        self.min_wait = min_wait or 3
        self.workers = None
        self.loop = loop

    async def get_prices(self):
        res = await self.request('simplemultialgo.info')
        self.prices = res['result']['simplemultialgo']
        return self.prices

    async def get_stats(self):
        res = await self.request('stats.provider', addr=self.addr)
        self.stats = res['result']['stats']
        return self.stats

    async def get_workers(self, algo):
        res = await self.request(
                'stats.provider.workers', addr=self.addr, algo=algo)
        self.workers = res['result']['workers']
        return self.stats

    def print_stats(self):
        if not self.prices:
            self.get_prices()
        if not self.stats:
            self.get_stats()
        for algo in self.iter_stats():
            _id, balance, accepted_speed, rejected_speed = algo
            info = self.prices[_id]
            assert info['algo'] == _id
            paying = float(info['paying'])
            print(info['name'], balance, accepted_speed * paying,
                  rejected_speed * paying)

    def iter_stats(self, has_balance=True, has_speed=False):
        if not self.stats:
            self.get_stats()
        for algo in self.stats:
            balance = float(algo['balance'])
            if has_balance and balance == 0:
                continue
            accepted_speed = float(algo['accepted_speed'])
            rejected_speed = float(algo['rejected_speed'])
            if has_speed and (accepted_speed == 0 and rejected_speed == 0):
                continue
            _id = algo['algo']
            yield _id, balance, accepted_speed, rejected_speed

    async def request(self, method, **params):
        url = self.get_url(method, **params)
        if self.last_req_time:
            elapse = time.time() - self.last_req_time
            if elapse < self.min_wait:
                await aio.sleep(self.min_wait - elapse)
        self.last_req_time = time.time()

        async with aiohttp.ClientSession(loop=self.loop) as session:
            async with session.get(url) as res:
                return await res.json(content_type=None)

    @classmethod
    def get_url(cls, method, **params):
        if params:
            ps = ['%s=%s' % (k, v) for k, v in params.items()]
            params = '&' + '&'.join(ps)
        else:
            params = ''
        return cls.api_url + 'method=%s' % method + params
