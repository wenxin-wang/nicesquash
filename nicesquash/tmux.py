import os
import asyncio as aio


class Tmux:
    def __init__(self, name, loop, gpu_id=None):
        self.name = name
        self.loop = loop
        self.cid = None
        if gpu_id is not None:
            self.cid = int(gpu_id) + 1

    async def set_layout(self, n):
        for _ in range(n):
            await self.exec('split-window', '-t', '%s:0' % self.name)
        await self.exec('select-layout', '-t', '%s:0' % self.name, 'tiled')

    async def gpu_run(self, cmd):
        await self.gpu_stop()
        await self.send_keys(cmd)

    async def gpu_stop(self):
        await self.send_keys("", 'C-c')

    async def send_keys(self, keys, last='C-m'):
        await self.exec('send-keys', '-t', '%s:0.%d' % (self.name, self.cid),
                        keys, last)

    def exec(self, *cmd):
        tmux = os.environ.get('TMUX_BIN', 'tmux')
        cmd = [tmux] + list(cmd)
        return aio.create_subprocess_exec(*cmd, loop=self.loop)
