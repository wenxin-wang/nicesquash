from worker import Worker
from tmux import Tmux
import asyncio as aio


class Manager:
    def __init__(self, conf, loop):
        self.conf = conf
        self.loop = loop
        self.tmux = Tmux(conf.session, loop)
        self.workers = [
            Worker(gpu, conf, loop)
            for gpu in conf.config.cuda
        ]

    async def kickOff(self):
        nw = len(self.conf.config.cuda)
        await self.tmux.set_layout(nw)
        if self.conf.benchmark:
            for w in self.workers:
                await w.start()
        else:
            futs = [
                aio.ensure_future(w.start())
                for w in self.workers
            ]
            await aio.gather(*futs)
