import jedi


from PyQt6.QtCore import QObject, QTimer, pyqtSignal

def jedi_worker(code_queue, result_queue):
    while True:
        item = code_queue.get()
        if item == "__EXIT__":
            break
        code, line, column = item
        try:
            script = jedi.Script(code=code)
            definitions = script.help(line, column)
            result = definitions[0].docstring() if definitions else ""
            result_queue.put(result)
        except Exception as e:
            result_queue.put(str(e))


class JediBridge(QObject):
    result_ready = pyqtSignal(str)

    def __init__(self, code_queue, result_queue):
        super().__init__()
        self.code_queue = code_queue
        self.result_queue = result_queue
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_results)
        self.timer.start(100)

    def request_docstring(self, code_pos_tuple):
        self.code_queue.put(code_pos_tuple)

    def check_results(self):
        while not self.result_queue.empty():
            results = self.result_queue.get()
            self.result_ready.emit(results)