import threading


def threaded(func):
    """
    Decorator to start a function in a new thread
    """
    def thr(*args, **kwargs):
        threading.Thread(target=func, args=(*args,), kwargs={**kwargs, }).start()
    return thr
