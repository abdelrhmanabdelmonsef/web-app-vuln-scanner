import threading
import time

def thread(function, args=()):
    print('in thread')
    t = threading.Thread(target=function, args=args)
    t.start()
    return t 

def join_threads(thread_objects):
    for t in thread_objects:
        t.join()





