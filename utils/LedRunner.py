import threading

class LedRunner:
    def __init__(self):
        self.thread = None
        self.running = False
        
    def __repeat(self, func, args):
        """Will run the given function until the running variable is at False"""
        while self.running:
            func(*args)
            
    def start(self, func, *args):
        """First stop previous thread then start a new thread"""
        self.stop()
        self.running = True
        self.thread = threading.Thread(target=self.__repeat, args=(func, args))
        self.thread.start()
        
    def stop(self):
        """Stop current thread"""
        if self.thread is not None and self.thread.isAlive():
            self.running = False
            self.thread.join()
            
    def once(self, func, *args):
        """Run the given function once"""
        self.stop()
        func(*args)
