
from TerminatedTask import os, sys, asyncio, time, TerminatedTask, signal

class PermamentProcess:

    def __init__(self, cmd = '', time_limit = 0, live_time = 10) -> None:
        self._cmd = cmd
        self._time_limit = time_limit
        self._live_time = live_time
        self.__trigger_time = int(time.time())

        self.process = None

        self.__stdout = ''
        self.__stderr = ''

    def _callback(self, stdout, stderr):
        self.__stdout = stdout
        self.__stderr = stderr

    def run(self):
        self.process = TerminatedTask(cmd = self._cmd, callback=self._callback, time_limit=self._time_limit)
        result = self.process.run()
        print(result)

    def kill_task(self):
        pass

    def isRunning(self, searchableString = ''):
        # checking interval
        if int(time.time() - self.__trigger_time) > self._live_time and self.process:
            # kill old task
            self.process.kill_process()
            self.kill_task()
        
        # check if task is alive
        task = TerminatedTask(cmd = f'''ps aux | grep {searchableString} ''')
        stdout = task.run()

        if task.isCompleted and not task.hasError:
            result = stdout['stdout'].splitlines()
            if len(result) >= 3:
                pass
        


        print(f'''ps aux | grep "{searchableString}" ''')
        stdout = task.run()
        if task.isCompleted and not task.hasError:
            print('outputddd = ')
            result = [x for x in stdout['stdout'].splitlines() if ' grep ' not in x and '/bin/sh' not in x]
            if len(result):
                print('ddd = ', int(result[0].rsplit()[1]))
            for item in result:
                print(item)


if __name__ == '__main__':
    cmd = '''sleep 8; echo "something here, once more";'''
    cmd = f'''python3 {os.getcwd()}/check.py 20'''
    p = PermamentProcess(cmd = cmd, time_limit=1)
    p.isRunning(searchableString='check.py ')