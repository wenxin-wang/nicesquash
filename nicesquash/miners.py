import os
from subprocess import Popen, STDOUT


class Miner:
    def __init__(self, algo, gpu, log_p):
        self.algo = algo
        self.gpu = gpu
        self.log_p = log_p
        self.proc = None

    @property
    def stratum(self):
        name = self.algo['name']
        port = self.algo['port']
        url = 'stratum+tcp://%s.hk.nicehash.com:%s' % (name, port)
        return url

    def exec(self):
        cmd = self.cmd
        prog = cmd[0]
        self.cmd[0] = os.environ.get(prog.upper(), prog)
        cmd = [str(w) for w in cmd]
        if 'DRY' in os.environ:
            cmd = ['echo', '"%s"' % ' '.join(cmd)]
        with open(self.log_p, 'w') as f:
            self.proc = Popen(cmd, stdout=f, stderr=STDOUT)
        return self.proc


class CCMiner(Miner):
    def __init__(self, ccalgo_name, algo, gpu, log_p):
        self.algo = algo
        # CCMiner has its own naming
        self.ccalgo_name = ccalgo_name
        self.gpu = gpu
        self.log_p = log_p
        self.proc = None

    @property
    def cmd(self):
        return [
            'ccminer', '-a', self.ccalgo_name, '-d', self.gpu.gpu_id, '-o',
            self.stratum, '-u',
            '%s.%s' % (self.gpu.address, self.gpu.worker)
        ]


class EthMiner(Miner):
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
