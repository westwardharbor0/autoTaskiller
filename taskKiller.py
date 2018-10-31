import time
import os
import datetime
import json

class TaskKiller:
    #-------------------------------------------------#
    class Task:
        user = ""
        pid, cpu, mem = 0,0,0
        started = ""
        time = ""
        command = ""
        def __init__(self,task):
            args = task
            self.user = args[0]
            self.pid  = int(args[1])
            self.cpu  = args[2].replace(',','.')
            self.mem  = args[3]
            self.started = args[8]
            self.time  = args[9]
            self.command = args[10]
        def getTask(self):
            return {
                'user': self.user,
                'pid':self.pid,
                'cpu':self.cpu,
                'mem':self.mem,
                'started':self.started,
                'time':self.time,
                'command':self.command
            }
        def getTaskS(self):
            return json.dumps(self.getTask())
    #-------------------------------------------------#
    class Loger:
        LOG_NAME = "killed"
        LOG_TYPE = ".txt"
        LOG_FOLDER = 'logs/'
        def write(self,msg):
            ts   = self.stamp('%d-%m-%Y %H:%M:%S')
            file = self.name(self.stamp('_%d_%m_%Y'))
            if not os.path.exists(file):
                open(file, 'w+')
            log = open(file,'a')
            log.write(ts+" ----- "+msg+"\n")
            log.close()

        def stamp(self,format):
            return datetime.datetime.fromtimestamp(time.time()).strftime(format)

        def name(self,name):
            return self.LOG_FOLDER + self.LOG_NAME + name + self.LOG_TYPE
    #-------------------------------------------------#
    class Storer:
        file = 'kill.tsk'
        def writeTasks(self,tasks):
            s = open(self.file, 'w')
            for task in tasks:
                s.write(str(task.pid)+"\n")
            s.close()

        def loadTasks(self):
            s = open(self.file)
            lines = self.mapInts(s.readlines())
            s.close()
            return lines

        def mapInts(self,arr):
            return list(map(lambda x: int(x),arr))
    #-------------------------------------------------#
    TASKS = []
    CPU_LIMIT = 90
    STORER = Storer()
    LOGER = Loger()
    def __init__(self,**args):
        if 'cpulimit' in args:
            self.CPU_LIMIT = args['cpulimit']

    def findCpuUsers(self):
        ret = []
        for task in self.TASKS:
            if(float(task.cpu) > self.CPU_LIMIT):
                ret.append(task.getTask())
        return ret

    def killTask(self,task):
        os.popen("sudo kill "+str(task.pid))
        self.LOGER.write(task.getTaskS())

    def getPids(self):
        ret = []
        for task in self.TASKS:
            ret.append(task.pid)
        return ret

    def getPid(self,pid):
        for task in self.TASKS:
            if task.pid is pid:
                return task
        return False

    def killCpuUsage(self):
        ret = []
        loaded = self.STORER.loadTasks()
        pids = self.STORER.mapInts(self.getPids())
        for pid in pids:
            if pid in loaded:
                self.killTask(self.getPid(pid))
        self.loadTaskList()
        for task in self.TASKS:
            if(float(task.cpu) > self.CPU_LIMIT):
                ret.append(task)

        self.STORER.writeTasks(ret)

    def getTaskList(self):
        ret = []
        for task in self.TASKS:
            ret.append(task.getTask())
        return ret

    def getTasks(self):
        return self.TASKS

    def loadTaskList(self):
        resp = os.popen("sudo ps aux")
        lines = resp.readlines()
        lines.pop(0)
        for line in lines:
            split = line.split(" ")
            split = list(filter(lambda x: x is not "" ,split))
            task = self.Task(split)
            self.TASKS.append(task)




if __name__ == "__main__":
    tasks = TaskKiller(cpulimit=90)
    tasks.loadTaskList()
    tasks.killCpuUsage()
