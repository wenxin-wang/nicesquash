import os
from subprocess import check_call


class Tmux:
    def __init__(self, name):
        self.name = name

    def set_layout(self, n):
        for _ in range(n):
            self.call('split-window', '-t', '%s:0' % self.name)
        self.call('select-layout', '-t', '%s:0' % self.name, 'tiled')

    def gpu_log(self, gpu, log_p):
        _id = int(gpu.gpu_id) + 1
        self.send_keys(_id, "", 'C-c')
        self.send_keys(_id, 'tail -f %s' % str(log_p))

    def send_keys(self, _id, keys, last='C-m'):
        self.call('send-keys', '-t', '%s:0.%d' % (self.name, _id), keys, last)

    def call(self, *cmd):
        tmux = os.environ.get('TMUX_BIN', 'tmux')
        cmd = [tmux] + list(cmd)
        check_call(cmd)
