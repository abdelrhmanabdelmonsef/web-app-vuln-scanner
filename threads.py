import threading
import time

def thread(function, args=()):
    t = threading.Thread(target=function, args=args)
    t.start()
    t.join()

def threads(dict):
    for function,args in dict.items():
        thread(function, args=tuple(args))

def custom_thread(function, args=(), total_requests=1, iteration_requests=1, delay=1):
    times = total_requests // iteration_requests
    for i in range(times):
        for j in range(iteration_requests):
            thread(function,args=args)
        time.sleep(delay)
        
def custom_threads(dict, total_requests=1, times=1):
    threads_num = total_requests // times
    for i in range(times):
        for j in range(threads_num):
            threads(dict)
        time.sleep(1)




