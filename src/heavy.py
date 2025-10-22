import jedi
from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from func_classes import list_classes_functions
from queue import Empty
import queue
from config import getInterpreter, is_frozen
from bash import get_elements

# _cache = {}
# _cache_size_limit = 1000



def jedi_worker(code_queue, result_queue):
    while True:
        try:
            item = code_queue.get(timeout = 1)
        except queue.Empty:
            continue


        if item == "__EXIT__":
            break
        code, line, column = item
        try:
            python_path = getInterpreter()
            if python_path:
                try:
                    env = jedi.create_environment(python_path)
                    script = jedi.Script(code=code, environment = env)
                    definitions = script.help(line, column)
                    result = definitions[0].docstring() if definitions else ""
                except Exception as env_error:
                    script = jedi.Script(code=code)
                    definitions = script.help(line, column)
                    result = definitions[0].docstring() if definitions else ""
            else:
                script = jedi.Script(code=code)
                definitions = script.help(line, column)
                result = definitions[0].docstring() if definitions else ""

            result_queue.put(result)
        except Exception as e:
            result_queue.put(str(e))



def jedi_completion(code_queue, result_queue, current_file):
    while True:
        try:
            item = code_queue.get(timeout = 1)
        except queue.Empty:
            continue

        if item == "__EXIT__":
            break

        code, line, column = item
        try:
            python_path = getInterpreter()
            if python_path:
                try:
                    env = jedi.create_environment(python_path)
                    script = jedi.Script(code=code, path=current_file, environment = env)
                    completions = script.complete(line, column)
                except Exception as env_error:
                    script = jedi.Script(code=code, path=current_file)
                    completions = script.complete(line, column)
            else:
                script = jedi.Script(code=code, path=current_file)
                completions = script.complete(line, column)
 

            payload = []
            for c in completions[:30]:
                try:
                    name = c.name
                    payload.append({
                        "name": name,
                        "type": c.type or "",
                        "description": c.description or ""
                    })

                except Exception as e:
                    pass

            result_queue.put(payload)

        except Exception as e:
            result_queue.put([{"name": str(e), "type": "error", "description": ""}])


class JediBridgeCompletion(QObject):
    result_ready = pyqtSignal(list)

    def __init__(self, code_queue, result_queue):
        super().__init__()
        self.code_queue = code_queue
        self.result_queue = result_queue
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_results)
        self.timer.start(100)

    def request_docstring(self, code_pos_tuple):
    # request_docstring
        self.code_queue.put(code_pos_tuple)

    def check_results(self):
        while not self.result_queue.empty():
            results = self.result_queue.get()
            self.result_ready.emit(results)


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


class SyntaxBridge(QObject):
    result_ready = pyqtSignal(dict)

    def __init__(self, code_queue, result_queue):
        super().__init__()
        self.code_queue = code_queue
        self.result_queue = result_queue
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_results)
        self.timer.start(900)

    def request_docstring(self, code_pos_tuple):
        self.code_queue.put(code_pos_tuple)

    def check_results(self):
        while not self.result_queue.empty():
            results = self.result_queue.get()
            self.result_ready.emit(results)


def syntax_worker(code_queue, result_queue):
    while True:
        try:
            code = code_queue.get(timeout = 1)
        except queue.Empty:
            continue

        # code = code_queue.get()
        # if code == "__EXIT__":
        #     break

        while True:
            try:
                code = code_queue.get_nowait()
                if code == "__EXIT__":
                    return
            except Empty:
                break

        instances = list_classes_functions(code)
        result_queue.put(instances)