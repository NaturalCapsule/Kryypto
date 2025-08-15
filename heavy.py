import jedi
from PyQt6.QtCore import QObject, QTimer, pyqtSignal

# def is_cursor_in_string(text, cursor_pos):
#     before_cursor = text[:cursor_pos]

#     single_quotes = before_cursor.count("'") - before_cursor.count("\\'")
#     double_quotes = before_cursor.count('"') - before_cursor.count('\\"')
#     if single_quotes % 2 == 1 or double_quotes % 2 == 1:
#         return True

#     return False


# def is_cursor_in_parentheses(text, cursor_pos):
#     before_cursor = text[:cursor_pos]
#     parenthes = before_cursor.count("(") - before_cursor.count(')')

#     if parenthes % 2 == 1:
#         return True

#     return False


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


def jedi_completion(code_queue, result_queue, current_file):
    while True:
        item = code_queue.get()
        if item == "__EXIT__":
            break
        code, line, column = item

        try:
            script = jedi.Script(code=code, path = fr"{current_file}")
            completions = script.complete(line, column)


            payload = []
            for c in completions[:30]:
                try:
                    name = getattr(c, "name", None) or ""
                    ctype = getattr(c, "type", None) or ""
                    description = getattr(c, "description", None) or ""

                    suffix = getattr(c, "suffix", None)
                    if suffix:
                        name += suffix

                    payload.append({
                        "name": name,
                        "type": ctype,
                        "description": description
                    })
                except Exception as inner_err:
                    print(f"Skipped completion due to error: {inner_err}")
                    continue

            result_queue.put(payload)

        except Exception as e:
            print(e)


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