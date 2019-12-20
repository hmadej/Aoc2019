import threading


class ConcurrentPipe:
    def __init__(self):
        self.message = 0
        self.producer_lock = threading.Lock()
        self.consumer_lock = threading.Lock()
        self.consumer_lock.acquire()
        # nothing to be consumer initially

    def get_input(self):
        self.consumer_lock.acquire()
        message = self.message
        self.message = 0
        self.producer_lock.release()
        return message

    def set_output(self, message):
        self.producer_lock.acquire()
        self.message = message
        self.consumer_lock.release()


class Pipe:
    def __init__(self):
        self.message = 0
        self.lock = threading.Lock()

    def get_input(self):
        self.lock.acquire()
        message = self.message
        self.lock.release()
        return message

    def set_output(self, message):
        self.lock.acquire()
        self.message = message
        self.lock.release()

    def inspect(self):
        return self.message
