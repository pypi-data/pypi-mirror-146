import logging
import os
import sys
import threading
import traceback
from multiprocessing import Pool as Mpp
from multiprocessing.dummy import Pool as ThreadPool

import tqdm
from tqdm.contrib.concurrent import process_map, thread_map


class MWT(threading.Thread):
    def __init__(self, function, params):
        threading.Thread.__init__(self)
        self.func = function
        self.params = params

    def run(self):
        try:
            return self.func(**self.params)
        except Exception as E:
            exc_type, exc_value, exc_obj = sys.exc_info()
            err = traceback.format_exc(limit=10)
            log = logging.Logger('MULTI_WORKER')
            log.error(f"error in running thread: ({str(self.func)}):\n{E}\n\n{err}")


class FakeSlaves:
    def __init__(self, workers=None, with_tq=False):
        self.workers = workers
        self.with_tq = with_tq

    def work(self, func, params_list: list):
        try:
            # if self.with_tq:
            #     tq = tqdm.tqdm(total=len(params_list))
            #     res_data = self.map_list(func, params_list, tq=tq)
            #     tq.close()
            # else:
            res_data = self.map_list(func, params_list)
            return res_data

        except Exception as E:
            exc_type, exc_value, exc_obj = sys.exc_info()
            err = traceback.format_exc(limit=10)
            log = logging.Logger('Slaves')
            log.error(f"error in Slaves: ({str(func)}):\n{E}\n\n{err}")

    def map_list(self, func, params_list: list, tq=None):
        res_list = list()
        for data in params_list:
            res_list.append(func(data))
            if tq:
                tq.update()
        return res_list


class Slaves:
    def __init__(self, workers=None, with_tq=False):
        self.pool = ThreadPool(workers if workers else 10)
        self.with_tq = with_tq
        self.workers = workers

    def work(self, func, params_list: list):
        try:
            if not self.with_tq:
                return self.pool.map(func, params_list)
            else:
                return thread_map(func, params_list, max_workers=self.workers)
        except Exception as E:
            exc_type, exc_value, exc_obj = sys.exc_info()
            err = traceback.format_exc(limit=10)
            log = logging.Logger('Slaves')
            log.error(f"error in Slaves: ({str(func)}):\n{E}\n\n{err}")


class BigSlaves:
    def __init__(self, workers=None, with_tq=False):
        ava_sys_cpu = os.cpu_count() - 1
        workers = workers if workers else ava_sys_cpu
        if workers > ava_sys_cpu:
            workers = ava_sys_cpu

        self.pool = Mpp(workers)
        self.with_tq = with_tq
        self.workers = workers

    def work(self, func, params_list: list):
        try:
            if not self.with_tq:
                return self.pool.map(func, params_list)
            else:
                return process_map(func, params_list, max_workers=self.workers)
        except Exception as E:
            exc_type, exc_value, exc_obj = sys.exc_info()
            err = traceback.format_exc(limit=10)
            log = logging.Logger('BigSlaves')
            log.error(f"error in BigSlaves: ({str(func)}):\n{E}\n\n{err}")


def test(num):
    return num * num


def test_main():
    import time
    t0 = time.time()
    test_list = list(range(100))
    result = Slaves(4).work(test, test_list)
    t1 = time.time()
    print(result)
    print(t1 - t0)

    t2 = time.time()
    tl = []
    tl_append = tl.append
    for i in test_list:
        tl_append(i * i)
    t3 = time.time()
    print(tl)
    print(t3 - t2)


if __name__ == '__main__':
    test_main()
