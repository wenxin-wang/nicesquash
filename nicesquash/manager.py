from worker import Worker


class Manager:
    def __init__(self, conf):
        self.conf = conf
        self.workers = [
            Worker(gpu, conf)
            for gpu in conf.config.cuda
        ]
        nw = len(conf.config.cuda)
        conf.tmux.set_layout(nw)

    def kickOff(self):
        if self.conf.benchmark:
            for w in self.workers:
                w.start()
