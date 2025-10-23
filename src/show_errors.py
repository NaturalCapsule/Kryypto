import ast
import cssutils
import io
import logging
import re
import json
import commentjson
import importlib.util
import builtins

from PyQt6.QtGui import QTextCursor, QColor, QTextCharFormat, QTextCursor, QColor
from PyQt6.QtCore import QTimer, QRunnable, Q_ARG
from lark.exceptions import UnexpectedToken
from threading import Thread
from multiprocessing import Process, Queue
from concurrent.futures import ProcessPoolExecutor

from func_classes import list_classes_functions
from config import set_advancedHighlighting

class AnalysisWorker(QRunnable):
    def __init__(self, code, callback, task_id):
        super().__init__()
        self.code = code
        self.callback = callback
        self.task_id = task_id
        self.setAutoDelete(True)
    
    def run(self):
        try:
            if hasattr(self.callback, '_current_task_id') and self.callback._current_task_id != self.task_id:
                return
            
            instances = list_classes_functions(self.code)

            if hasattr(self.callback, '_current_task_id') and self.callback._current_task_id != self.task_id:
                return
                
            from PyQt6.QtCore import QMetaObject, Qt
            QMetaObject.invokeMethod(self.callback, "_update_highlighter", 
                                   Qt.ConnectionType.QueuedConnection,
                                   Q_ARG(dict, instances))
        except Exception as e:
            print(f"Analysis error: {e}")


class ShowErrors:
    def __init__(self, parent, highlighter):
        super().__init__()
        parent.textChanged.connect(self.schedule_check)
        self.exec = ProcessPoolExecutor(max_workers = 4)


        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.check_syntax)

        self.error_label = None
        self.nameErrorlabel = None
        self.parent = parent
        self.highlighter = highlighter
        
        
        self._current_code = ""
        self._last_instances = {}
        self._use_background = True
        self._use_sync_fallback = False
        self._current_task_id = 0
        self._max_file_size = 50000
        self._sync_threshold = 500

    def schedule_check(self):
        self.timer.stop()
        self.timer.start(800)

    def check_syntax(self):
        missing_modules = []
        defined = set()
        used = set()
        code = self.parent.toPlainText()
        
        if code == self._current_code:
            return
            
        self._current_code = code
        self.clear_error_highlighting()

        try:
            tree = ast.parse(code)

            if self.error_label:
                self.error_label.setText("✔️ No SyntaxError")

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        mod = alias.name.split('.')[0]
                        if not importlib.util.find_spec(mod):
                            missing_modules.append(mod)
                        defined.add(alias.asname or mod)

                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        root_mod = node.module.split('.')[0]
                        if not importlib.util.find_spec(root_mod):
                            missing_modules.append(node.module)
                        for alias in node.names:
                            defined.add(alias.asname or alias.name)

                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    defined.add(node.name)
                    for arg in node.args.args:
                        defined.add(arg.arg)
                    if node.args.vararg:
                        defined.add(node.args.vararg.arg)
                    if node.args.kwarg:
                        defined.add(node.args.kwarg.arg)

                elif isinstance(node, ast.ClassDef):
                    defined.add(node.name)

                elif isinstance(node, ast.ExceptHandler):
                    if node.name:
                        defined.add(node.name)

                elif isinstance(node, ast.Name):
                    if isinstance(node.ctx, ast.Store):
                        defined.add(node.id)
                    elif isinstance(node.ctx, ast.Load):
                        used.add(node.id)

            undefined = used - defined - set(dir(builtins))
            if undefined:
                self.nameErrorlabel.setText(f"⚠️ Undefined: {undefined}")
            else:
                self.nameErrorlabel.setText(f'✔️ No NameError')

            if set_advancedHighlighting():
                self.parse_code(code)

        except (SyntaxError, NameError) as e:
            if self.error_label:
                self.error_label.setText(f"❌ SyntaxError Line: {e.lineno}: {e.msg}")
            self.underline_error(e.lineno, e.offset)

    def parse_code(self, code):
        if set_advancedHighlighting():
            future = self.exec.submit(list_classes_functions, code)
            future.add_done_callback(self.on_done)

    def on_done(self, future):
        try:
            tokens = future.result()
            self.analyze_code(tokens)
        except Exception as e:
            print(f"Error in on_done: {e}")

    def clear_error_highlighting(self):
        cursor = self.parent.textCursor()
        cursor.beginEditBlock()

        cursor.select(QTextCursor.SelectionType.Document)
        fmt = QTextCharFormat()
        fmt.setUnderlineStyle(QTextCharFormat.UnderlineStyle.NoUnderline)
        cursor.setCharFormat(fmt)

        cursor.endEditBlock()

    def underline_error(self, line, column):
        cursor = self.parent.textCursor()
        cursor.beginEditBlock()

        cursor.movePosition(QTextCursor.MoveOperation.Start)
        for _ in range(line - 1):
            cursor.movePosition(QTextCursor.MoveOperation.Down)

        cursor.movePosition(QTextCursor.MoveOperation.Right, n=column - 1)
        cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor)

        fmt = QTextCharFormat()
        fmt.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SpellCheckUnderline)
        fmt.setUnderlineColor(QColor("red"))
        cursor.setCharFormat(fmt)

        cursor.endEditBlock()

    def analyze_code(self, instances):
        try:
            if instances != self._last_instances:
                self._last_instances = instances
                self.highlighter.get_calls(instances)
                self.highlighter.rehighlight()
        except Exception as e:
            print(f"Error in analyze_code: {e}")

    
    def enable_sync_fallback(self):
        self._use_sync_fallback = True
        self._use_background = False
        
    def set_max_file_size(self, size):
        self._max_file_size = size

    def set_sync_threshold(self, threshold):
        self._sync_threshold = threshold

class ShowJsonErrors:
    def __init__(self, parent, highlighter, file_path, use_jsonc):
        parent.textChanged.connect(self.schedule_check)
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.check_syntax)
        self.error_label = None
        self.parent = parent
        self.highlighter = highlighter
        self.file_path = file_path
        self.use_jsonc = use_jsonc
        self.count_json = 0
        self.count_jsonc = 0

    def schedule_check(self):
            self.timer.start(500)

    def check_syntax(self):
        self.clear_error_highlighting()
        if not self.use_jsonc:
            try:
                file = self.parent.toPlainText()
                self.count_json += 1
                if self.count_json == 1:
                        if len(file) == 0:
                            self.parent.setPlainText('{\n    \n}')
                json.loads(file)
                if self.error_label:
                    self.error_label.setText("✔️ No syntax errors")

                Thread(target = lambda: self.analyze_code(self.parent), daemon = False).start()


            except json.JSONDecodeError as e:
                if self.error_label:
                    self.error_label.setText(f"❌ Line {e.lineno}: {e.msg}")

                self.underline_error(e.lineno, e.colno)
        else:
            try:
                self.count_jsonc += 1
                content = self.parent.toPlainText()
                if self.count_jsonc == 1:
                    if len(content) == 0:
                        self.parent.setPlainText("{\n    \n}")

                commentjson.loads(content)

                if self.error_label:
                    self.error_label.setText("✔️ No syntax errors")

                Thread(target=lambda: self.analyze_code(self.parent), daemon=False).start()

            except (UnexpectedToken, ValueError) as e:
                if self.error_label:
                    self.error_label.setText(f"❌ Error: {str(e)}")


    def clear_error_highlighting(self):
        cursor = self.parent.textCursor()

        cursor.beginEditBlock()

        cursor.select(QTextCursor.SelectionType.Document)
        fmt = QTextCharFormat()
        fmt.setUnderlineStyle(QTextCharFormat.UnderlineStyle.NoUnderline)
        cursor.setCharFormat(fmt)

        cursor.endEditBlock()

    def underline_error(self, line, column):

        cursor = self.parent.textCursor()

        cursor.beginEditBlock()

        cursor.movePosition(QTextCursor.MoveOperation.Start)
        if line <=3:
            for _ in range(line - 1):
                cursor.movePosition(QTextCursor.MoveOperation.Down)

        elif line <= 11 and line >=3:         
            for _ in range(line + 3):
                cursor.movePosition(QTextCursor.MoveOperation.Down)


        else:

            for _ in range(line + 5):
                cursor.movePosition(QTextCursor.MoveOperation.Down)

        cursor.movePosition(QTextCursor.MoveOperation.Right, n=column - 1)

        cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor)

        fmt = QTextCharFormat()
        fmt.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SpellCheckUnderline)
        fmt.setUnderlineColor(QColor("red"))
        cursor.setCharFormat(fmt)

        cursor.endEditBlock()


    def analyze_code(self, main_text):
        self.highlighter.rehighlight()


class ShowCssErrors:
    def __init__(self, parent, highlighter):
        parent.textChanged.connect(self.schedule_check)
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.check_syntax)
        self.error_label = None
        self.parent = parent
        self.highlighter = highlighter



    def schedule_check(self):
            self.timer.start(500)

    def check_syntax(self):
        log_output = io.StringIO()
        handler = logging.StreamHandler(log_output)
        cssutils.log.setLevel(logging.ERROR)
        cssutils.log.addHandler(handler)
        cssutils.parseString(self.parent.toPlainText())
        cssutils.log.removeHandler(handler)
        log_text = log_output.getvalue()
        cssutils.ser.prefs.useMinified()
        cssutils.log.setLevel(logging.FATAL) 


        self.clear_error_highlighting()
        pattern = r"\[(\d+):(\d+):.*?\]"

        matches = re.findall(pattern, log_text)

        if matches:

            for line, col in matches:

                self.underline_error(line, col)
                if self.error_label:
                    self.error_label.setText(f"❌ Line: {int(line) - 1}: {col}")

        else:
            if self.error_label:
                self.error_label.setText("No Errors!")

        Thread(target=lambda: self.analyze_code, daemon=False).start()
        log_output.close()


    def clear_error_highlighting(self):
        cursor = self.parent.textCursor()

        cursor.beginEditBlock()

        cursor.select(QTextCursor.SelectionType.Document)
        fmt = QTextCharFormat()
        fmt.setUnderlineStyle(QTextCharFormat.UnderlineStyle.NoUnderline)
        cursor.setCharFormat(fmt)

        cursor.endEditBlock()

    def underline_error(self, line, column):

        cursor = self.parent.textCursor()

        cursor.beginEditBlock()

        cursor.movePosition(QTextCursor.MoveOperation.Start)

        for _ in range(int(line) - 1):
            cursor.movePosition(QTextCursor.MoveOperation.Down)


        cursor.movePosition(QTextCursor.MoveOperation.Right, n=int(column) - 1)

        cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor)

        fmt = QTextCharFormat()
        fmt.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SpellCheckUnderline)
        fmt.setUnderlineColor(QColor("red"))
        cursor.setCharFormat(fmt)

        cursor.endEditBlock()

    def analyze_code(self):
        self.highlighter.rehighlight()