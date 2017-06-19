from worker import Worker


class Scheduler:
    def __init__(self, conf):
        self.conf = conf
        self.workers = [
            Worker(gpu, conf)
            for gpu in conf.config.cuda
        ]

    def kickOff(self):
        if self.conf.config.benchmark:
            for w in self.workers:
                w.start()
