import os
import re
from tmux import Tmux


class Miner:
    def __init__(self, algo, gpu, log_p, session, loop):
        self.algo = algo
        self.gpu = gpu
        self.log_p = log_p
        self.proc = None
        self.loop = loop
        self.tmux = Tmux(session, loop, gpu.gpu_id)

    @property
    def stratum(self):
        name = self.algo['name']
        port = self.algo['port']
        url = 'stratum+tcp://%s.hk.nicehash.com:%s' % (name, port)
        return url

    async def run(self):
        cmd = self.cmd
        prog = cmd[0]
        self.cmd[0] = os.environ.get(prog.upper(), prog)
        cmd = [str(w) for w in cmd]
        if 'DRY' in os.environ:
            cmd = ['echo', '"%s"' % ' '.join(cmd)]
        cmd += ['2>&1', '|', 'tee', str(self.log_p)]
        cmd = ' '.join(cmd)

        await self.tmux.gpu_run(cmd)

    async def stop(self):
        await self.tmux.gpu_stop()


class CCMiner(Miner):
    rate_re = re.compile(
        r"""
        ^\[(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})
        \ (?P<H>\d{2}):(?P<M>\d{2}):(?P<S>\d{2})\]
        .*\ accepted.*,\s+(?P<rate>\S+)\s+(?P<unit_rate>\S*)
        (H|Sol)/s
        """, re.X)

    def __init__(self, ccalgo_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ccalgo_name = ccalgo_name

    @property
    def cmd(self):
        return [
            'ccminer', '-a', self.ccalgo_name, '-d', self.gpu.gpu_id, '-o',
            self.stratum, '-u',
            '%s.%s' % (self.gpu.address, self.gpu.worker)
        ]


class EthMiner(Miner):
    setwork_re = re.compile(r"""
        ^.*(?P<H>\d{2}):(?P<M>\d{2}):(?P<S>\d{2})
        .*set\s+work""", re.X)
    rate_re = re.compile(
        r"""
        ^.*(?P<H>\d{2}):(?P<M>\d{2}):(?P<S>\d{2})
        .*:\s+(?P<rate>\S*\d+)(?P<unit_rate>\D*)H/s\s+
        \[
        A(?P<accepts>\d+)\+(?P<accept_stales>\d+):
        R(?P<rejects>\d+)\+(?P<reject_stales>\d+):
        F(?P<failures>\d+)
        \]
        """, re.X)

    @property
    def cmd(self):
        return [
            'ethminer', '-SP', '2', '-U', '--cuda-devices', self.gpu.gpu_id,
            '-S', self.stratum, '-O',
            '%s.%s:x' % (self.gpu.address, self.gpu.worker)
        ]


class NHEqminer(Miner):
    @property
    def cmd(self):
        return [
            'nheqminer', '-t', '0', '-cd', self.gpu.gpu_id, '-l', self.stratum,
            '-u',
            '%s.%s' % (self.gpu.address, self.gpu.worker)
        ]


miner_types = {
    'ccminer': CCMiner,
    'nheqminer': NHEqminer,
    'ethminer': EthMiner,
}
