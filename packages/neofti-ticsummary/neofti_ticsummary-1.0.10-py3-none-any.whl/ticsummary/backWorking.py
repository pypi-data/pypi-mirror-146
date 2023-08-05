from PyQt6.QtCore import QObject, QThread, pyqtSignal

def factoryThreadByTask(task,callback,**kwargs):
    thread = QThread()
    worker = __Worker__(thread, task,**kwargs)
    worker.finished.connect(callback)
    worker.moveToThread(thread)
    return ControllerBWTask(thread,worker)

class __Worker__(QObject):
    finished = pyqtSignal()
    def __init__(self,thread,task,**kwargs):
        super().__init__()
        self.task=task
        self.kwargs=kwargs
        thread.started.connect(self.run)
        self.finished.connect(thread.quit)
        self.finished.connect(self.deleteLater)
        thread.finished.connect(thread.deleteLater)
    def run(self):
        self.task(**self.kwargs)
        self.finished.emit()

class ControllerBWTask():
    def __init__(self,thread:QThread,worker:__Worker__):
        self.thread = thread
        self.worker = worker
    def start(self):
        self.thread.start()
