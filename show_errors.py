import ast
import cssutils
import io
import logging
import re, jedi
import json, commentjson

from PyQt6.QtGui import QTextCursor, QColor, QTextCharFormat, QTextCursor, QColor
from PyQt6.QtCore import QTimer, QRunnable, pyqtSlot, pyqtSignal, QObject, QThread, QMutex, QMutexLocker
from PyQt6.QtWidgets import QApplication

from func_classes import list_classes_functions
from lark.exceptions import UnexpectedToken
from threading import Thread
class SyntaxCheckerWorker(QObject):
    
    finished = pyqtSignal(dict, str)
    error = pyqtSignal(int, int, str)
    
    def __init__(self):
        super().__init__()
        self.current_code = ""
        self.should_cancel = False
    
    @pyqtSlot(str)
    def process_code(self, code):
        self.current_code = code
        self.should_cancel = False
        
        if not code.strip():
            self.finished.emit({}, "✔️ No syntax errors")
            return
        
        try:
            if self.should_cancel:
                return
                
            ast.parse(code)
            
            if self.should_cancel:
                return
            
            instances = self.list_classes_functions(code)
            
            if self.should_cancel:
                return
                
            self.finished.emit(instances, "✔️ No syntax errors")
            
        except (SyntaxError, NameError) as e:
            if self.should_cancel:
                return
                
            line = getattr(e, 'lineno', 1) or 1
            offset = getattr(e, 'offset', 1) or 1
            msg = getattr(e, 'msg', 'Syntax error') or 'Syntax error'
            
            self.error.emit(line, offset, f"❌ Line {line}: {msg}")
    
    @pyqtSlot()
    def cancel_processing(self):
        self.should_cancel = True
    
    def list_classes_functions(self, code):
        try:
            if self.should_cancel:
                return {}
                
            func_class_instances = {}
            
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if self.should_cancel:
                    return {}
                
                if isinstance(node, ast.FunctionDef):
                    func_class_instances[node.name] = 'function'
                elif isinstance(node, ast.ClassDef):
                    func_class_instances[node.name] = 'class'
                elif isinstance(node, ast.Assign):
                    if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
                        class_name = node.value.func.id
                        if class_name not in ('int', 'len', 'str', 'float', 'bool', 'list', 'dict', 'tuple', 'set'):
                            func_class_instances[class_name] = 'class'
                elif isinstance(node, ast.ImportFrom) and node.module:
                    func_class_instances[node.module] = 'class'
                elif isinstance(node, ast.Call):
                    func = node.func
                    if isinstance(func, ast.Attribute):
                        func_class_instances[func.attr] = 'function'
            
            if len(code) < 10000 and not self.should_cancel:
                try:
                    script = jedi.Script(code=code)
                    names = script.get_names(all_scopes=True, definitions=True)
                    
                    for name in names:
                        if self.should_cancel:
                            break
                            
                        if name.type in ['class', 'module']:
                            func_class_instances[name.name] = 'class'
                        elif name.type == 'function':
                            func_class_instances[name.name] = 'function'
                            
                except Exception:
                    pass
            
            return func_class_instances
            
        except Exception:
            return {}


class ShowErrors:
    
    def __init__(self, parent, highlighter):
        self.parent = parent
        self.highlighter = highlighter
        self.error_label = None
        
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.run_check)
        
        self.parent.textChanged.connect(self.schedule_check)
        
        self.thread = QThread()
        self.worker = SyntaxCheckerWorker()
        self.worker.moveToThread(self.thread)
        
        self.worker.finished.connect(self.handle_success)
        self.worker.error.connect(self.handle_error)
        
        self.thread.start()
        
        self.is_processing = False
    
    def schedule_check(self):
        self.timer.stop()
        
        if self.is_processing:
            self.worker.cancel_processing()
        
        self.timer.start(500)
    
    def run_check(self):
        if not self.thread.isRunning():
            return
        
        self.clear_error_highlighting()
        
        code = self.parent.toPlainText()
        
        self.is_processing = True
        
        QApplication.instance().processEvents()
        self.worker.process_code(code)
    
    def handle_success(self, instances, message):
        self.is_processing = False
        
        if self.error_label:
            self.error_label.setText(message)
        
        self.analyze_code(instances)
    
    def handle_error(self, lineno, offset, message):
        self.is_processing = False
        
        if self.error_label:
            self.error_label.setText(message)
        
        self.underline_error(lineno, offset)
    
    def clear_error_highlighting(self):
        try:
            cursor = self.parent.textCursor()
            cursor.beginEditBlock()
            
            cursor.select(QTextCursor.SelectionType.Document)
            fmt = QTextCharFormat()
            fmt.setUnderlineStyle(QTextCharFormat.UnderlineStyle.NoUnderline)
            cursor.mergeCharFormat(fmt)
            
            cursor.endEditBlock()
        except Exception:
            pass
    
    def underline_error(self, line, column):
        try:
            cursor = self.parent.textCursor()
            cursor.beginEditBlock()
            
            cursor.movePosition(QTextCursor.MoveOperation.Start)
            
            cursor.movePosition(QTextCursor.MoveOperation.Down, 
                              QTextCursor.MoveMode.MoveAnchor, line - 1)
            
            if column and column > 1:
                cursor.movePosition(QTextCursor.MoveOperation.Right, 
                                  QTextCursor.MoveMode.MoveAnchor, column - 1)
            
            cursor.select(QTextCursor.SelectionType.WordUnderCursor)
            if not cursor.hasSelection():
                cursor.movePosition(QTextCursor.MoveOperation.Right, 
                                  QTextCursor.MoveMode.KeepAnchor, 1)
            
            fmt = QTextCharFormat()
            fmt.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SpellCheckUnderline)
            fmt.setUnderlineColor(QColor("red"))
            cursor.mergeCharFormat(fmt)
            
            cursor.endEditBlock()
        except Exception:
            pass
    
    def analyze_code(self, instances):
        try:
            if hasattr(self.highlighter, 'get_calls'):
                self.highlighter.get_calls(instances)
            doc_length = len(self.parent.toPlainText())
            
            if doc_length < 20000:
                QTimer.singleShot(150, self._safe_rehighlight)
            else:
                print(f"Skipping rehighlight for large document ({doc_length} chars)")
                
        except Exception as e:
            print(f"Analysis error: {e}")
    
    def _safe_rehighlight(self):
        try:
            if hasattr(self.highlighter, 'rehighlight'):
                self.highlighter.rehighlight()
        except Exception as e:
            print(f"Rehighlight error: {e}")
    
    def cleanup(self):
        self.timer.stop()
        
        if self.is_processing:
            self.worker.cancel_processing()
        
        self.thread.quit()
        if not self.thread.wait(2000):
            self.thread.terminate()
            self.thread.wait(1000)



# class ShowErrors:
#     def __init__(self, parent, highlighter):
#         parent.textChanged.connect(self.schedule_check)


#         self.timer = QTimer()
#         self.timer.setSingleShot(True)
#         self.timer.timeout.connect(self.check_syntax)
        
#         self.error_label = None
#         self.parent = parent
#         self.highlighter = highlighter

#     def schedule_check(self):
#         self.timer.start(500)

#     def check_syntax(self):
#         code = self.parent.toPlainText()

#         # self.clear_error_highlighting()

#         try:
#             # ast.parse(code)
#             # pass

#             if self.error_label:
#                 self.error_label.setText("✔️ No syntax errors")
#             # instances = list_classes_functions(code)
#             instances = list_classes_functions(code)
#             print(instances)

#             self.analyze_code(instances)


#         except (SyntaxError, NameError) as e:
#             if self.error_label:
#                 self.error_label.setText(f"❌ Line {e.lineno}: {e.msg}")
#             self.underline_error(e.lineno, e.offset)

#     def clear_error_highlighting(self):
#         cursor = self.parent.textCursor()
#         cursor.beginEditBlock()

#         cursor.select(QTextCursor.SelectionType.Document)
#         fmt = QTextCharFormat()
#         fmt.setUnderlineStyle(QTextCharFormat.UnderlineStyle.NoUnderline)
#         cursor.setCharFormat(fmt)

#         cursor.endEditBlock()

#     def underline_error(self, line, column):
#         cursor = self.parent.textCursor()
#         cursor.beginEditBlock()

#         cursor.movePosition(QTextCursor.MoveOperation.Start)
#         for _ in range(line - 1):
#             cursor.movePosition(QTextCursor.MoveOperation.Down)

#         cursor.movePosition(QTextCursor.MoveOperation.Right, n=column - 1)
#         cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor)

#         fmt = QTextCharFormat()
#         fmt.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SpellCheckUnderline)
#         fmt.setUnderlineColor(QColor("red"))
#         cursor.setCharFormat(fmt)

#         cursor.endEditBlock()

#     def analyze_code(self, instances):
#         self.highlighter.get_calls(instances)
#         self.highlighter.rehighlight()



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