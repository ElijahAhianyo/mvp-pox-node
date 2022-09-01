import multiprocessing, math, gc
import threading, subprocess, asyncio, time, psutil, os, sys, platform, random, json
try:
    from src.node_benchmark.tests.algorithms.sorts import *
    from src.node_benchmark.tests.algorithms.search import *
except ImportError as e:
    from tests.algorithms.sorts import *
    from tests.algorithms.search import *

class Task:
    obj = {'deviceInformation': {}, 'tasks': {}}
    def __init__(self) -> None:
        self.functions = [
            bubble_sort,
            pancake_sort,
            pigeonhole_sort,
            double_sort,
            # bogo_sort, 

            jump_search,
            linear_search,
            Binary_search,
            fibonacci_search
        ]

        self.dump()

    def dump(self):
        iters_count = 1000
        _list = [random.randint(0, iters_count) for i in range(iters_count)]

        self.getDeviceInformation()

        self.measure(title='SingleProcess', callback=self.singLeProcess, _list = _list)
        self.measure(title='MultiThreading', callback=self.multiThreading, _list = _list)
        self.measure(title='MultiProcessing', callback=self.multiprocessing, _list = _list)
        self.measure(title='AsyncIO', callback=self.asyncIo, _list = _list)

        with open(os.path.join(os.getcwd(), 'node-benchmark-result.json'), 'w') as w:
            json.dump(self.obj, w)
        self.obj = {}

    def getDeviceInformation(self) -> None:
        print(f'\nDevice/System Information:\n')
        modelName = [x.split(':')[1].strip() for x in subprocess.check_output("lscpu", shell=True).strip().decode().splitlines() if 'Model name' in x]
        if modelName:
            self._print(key  = 'Processor', value = modelName[0])
        self._print(key = "Number of CPUs", value = multiprocessing.cpu_count())
        platform_list = ['architecture','platform','system']
        [self._print(key = p, value = getattr(platform, p)()) for p in platform_list]
        self._print(key = 'ram space', value = f"{round(psutil.virtual_memory().total / 1024 / 1024 / 1024, 2)}G")
        self._print(key = 'Python Version', value = sys.version)
        print(f"\n{('-' * 10)} \n")
        
    @classmethod
    def _print(cls, key, value) -> None:
        print(f"{key}: {value}")
        cls.obj['deviceInformation'][key] = value

    @classmethod
    def measure(cls, title = '', callback = None, *args, **kwargs) -> None:
        print(f'**** {title}...\n')
        t = time.time()
        callback(*args, **kwargs)
        tm = round(time.time() - t, 4)
        print(f"\nsum = {tm}\n{'-' * 10} \n")
        gc.collect()
        time.sleep(2)
        cls.obj['tasks'][title] = tm

    # --- tasks

    def singLeProcess(self, _list) -> None:
        [function(_list.copy()) for  function in self.functions]

    def multiThreading(self, _list = None) -> None:
        threads = []
        for function in self.functions:
            thread = threading.Thread(target = function, args = (_list.copy(), ))
            thread.start()
            threads.append(thread)
        [t.join() for t in threads]

    def multiprocessing(self, _list = None) -> None:
        for function in self.functions:
            process = multiprocessing.Process(target = function, args = (_list.copy(), ))
            process.start()
        [p.join() for p in multiprocessing.active_children()]

    def asyncIo(self, _list = None) -> None:
        try:
            asyncio.run(asyncio.gather(*[function(_list.copy()) for function in self.functions], return_exceptions=False))
        except TypeError:
            pass


if __name__ == '__main__':
    task = Task()