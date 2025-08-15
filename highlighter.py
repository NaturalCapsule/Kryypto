# import ast
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt6.QtCore import QRegularExpression, QRunnable, pyqtSignal, QObject, QThreadPool
from config import *

# import ast
import re
from PyQt6.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal, QTimer, QMutex
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt6.QtWidgets import QApplication





class PythonSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self,use_highlighter ,parent=None):
        super().__init__(parent)

        self.useit = use_highlighter

        if self.useit:
            self.highlighting_rules = []
            self.setup_highlighting_rules()

        else:
            pass

        self._compiled_patterns = {}
        self._last_instances = {}

    def setup_highlighting_rules(self):
        r, g, b = get_comment()
        self.string_format = QTextCharFormat()
        r, g, b = get_string()
        self.string_format.setForeground(QColor(r, g, b))


        r, g, b = get_comment()

        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor(r, g, b))  
        # self.highlighting_rules.append((QRegularExpression('#[^\n]*'), self.comment_format, 'comment'))


        self.string_pattern = QRegularExpression(r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\'')
        self.comment_pattern = QRegularExpression(r'#[^\n]*')

        # self.highlighting_rules.append((
        #     QRegularExpression(r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\'|#[^\n]*'),
        #     string_format,
        #     'mixed'
        # ))


        self.func_args_format = QTextCharFormat()
        r, g, b = get_bracket()
        self.func_args_format.setForeground(QColor(r, g, b))


        # self.comment_format = QTextCharFormat()
        # self.comment_format.setForeground(QColor(r, g, b))  
        # self.highlighting_rules.append((QRegularExpression('#[^\n]*'), self.comment_format, 'comment'))



        # string_format = QTextCharFormat()
        # r, g, b = get_string()
        # string_format.setForeground(QColor(r, g, b))

        self.highlighting_rules.append((
            QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"'),
            self.string_format,
            'string'
        ))
        self.highlighting_rules.append((
            QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'"),
            self.string_format,
            'string'
        ))

        # self.highlighting_rules.append((
        #     QRegularExpression(r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\'|#[^\n]*'),
        #     string_format,  # We'll decide formatting dynamically
        #     'mixed'
        # ))



        # r, g, b = get_comment()
        # self.comment_format = QTextCharFormat()
        # self.comment_format.setForeground(QColor(r, g, b))  
        # self.highlighting_rules.append((QRegularExpression('#[^\n]*'), self.comment_format, 'comment'))



        keyword_format = QTextCharFormat()
        r, g, b = get_python_keyword()
        keyword_format.setForeground(QColor(r, g, b))


        string_format = QTextCharFormat()
        r, g, b = get_string()
        string_format.setForeground(QColor(r, g, b))

        
        self.highlighting_rules.append((
            QRegularExpression(r'''(?<=\W|^)f"[^"\\]*(\\.[^"\\]*)*"'''),
            self.string_format,
            'f-string'
        ))

        self.highlighting_rules.append((
            QRegularExpression(r'''(?<=\W|^)f'[^'\\]*(\\.[^'\\]*)*' '''),
            self.string_format,
            'f-string'
        ))



        self.highlighting_rules.append((
            QRegularExpression(r'''(?<=\W|^)fr"[^"\\]*(\\.[^"\\]*)*"'''),
            self.string_format,
            'fr-string'
        ))

        self.highlighting_rules.append((
            QRegularExpression(r"""fr'[^'\\]*(\\.[^'\\]*)*""" + r"'"),
            self.string_format,
            'fr-string'
        ))


        self.highlighting_rules.append((
            QRegularExpression(r'''(?<=\W|^)b"[^"\\]*(\\.[^"\\]*)*"'''),
            self.string_format,
            'b-string'
        ))

        self.highlighting_rules.append((
            QRegularExpression(r"""b'[^'\\]*(\\.[^'\\]*)*""" + r"'"),
            self.string_format,
            'b-string'
        ))

        self.highlighting_rules.append((
            QRegularExpression(r'''(?<=\W|^)br"[^"\\]*(\\.[^"\\]*)*"'''),
            self.string_format,
            'br-string'
        ))

        self.highlighting_rules.append((
            QRegularExpression(r"""br'[^'\\]*(\\.[^'\\]*)*""" + r"'"),
            self.string_format,
            'br-string'
        ))

        self.highlighting_rules.append((
            QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"'),
            self.string_format,
            'string'
        ))
        self.highlighting_rules.append((
            QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'"),
            self.string_format,
            'string'
        ))

        keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'exec', 'finally', 'for',
            'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
            'not', 'or', 'pass', 'raise', 'return', 'try',
            'while', 'with', 'yield', 'super', 'True', 'False', 'None', 'Execption', "BaseException",
    "Exception",
    "ArithmeticError",
    "FloatingPointError",
    "OverflowError",
    "ZeroDivisionError",
    "AssertionError",
    "AttributeError",
    "BufferError",
    "EOFError",
    "ImportError",
    "ModuleNotFoundError",
    "LookupError",
    "IndexError",
    "KeyError",
    "MemoryError",
    "NameError",
    "UnboundLocalError",
    "OSError",
    "BlockingIOError",
    "ChildProcessError",
    "ConnectionError",
    "BrokenPipeError",
    "ConnectionAbortedError",
    "ConnectionRefusedError",
    "ConnectionResetError",
    "FileExistsError",
    "FileNotFoundError",
    "InterruptedError",
    "IsADirectoryError",
    "NotADirectoryError",
    "PermissionError",
    "ProcessLookupError",
    "TimeoutError",
    "ReferenceError",
    "RuntimeError",
    "NotImplementedError",
    "RecursionError",
    "StopIteration",
    "StopAsyncIteration",
    "SyntaxError",
    "IndentationError",
    "TabError",
    "SystemError",
    "TypeError",
    "ValueError",
    "UnicodeError",
    "UnicodeDecodeError",
    "UnicodeEncodeError",
    "UnicodeTranslateError",
    "Warning",
    "DeprecationWarning",
    "PendingDeprecationWarning",
    "RuntimeWarning",
    "SyntaxWarning",
    "UserWarning",
    "FutureWarning",
    "ImportWarning",
    "UnicodeWarning",
    "BytesWarning",
    "ResourceWarning",
    "GeneratorExit",
    "KeyboardInterrupt",
    "SystemExit"
        ]
        
        for keyword in keywords:
            pattern = QRegularExpression(f'\\b{keyword}\\b')
            self.highlighting_rules.append((pattern, keyword_format, 'keywords'))

        r, g, b = get_python_builtin()

        builtin_format = QTextCharFormat()
        builtin_format.setForeground(QColor(r, g, b))
        
        builtins = [
            "abs", "aiter", "all", "any", "anext", "ascii", "bin", "bool", "breakpoint",
            "bytearray", "bytes", "callable", "chr", "classmethod", "compile", "complex",
            "delattr", "dict", "dir", "divmod", "enumerate", "eval", "exec", "filter",
            "float", "format", "frozenset", "getattr", "globals", "hasattr", "hash", "help",
            "hex", "id", "input", "int", "isinstance", "issubclass", "iter", "len", "list",
            "locals", "map", "max", "memoryview", "min", "next", "object", "oct", "open",
            "ord", "pow", "print", "property", "range", "repr", "reversed", "round", "set",
            "setattr", "slice", "sorted", "staticmethod", "str", "sum", "super", "tuple",
            "type", "vars", "zip"
        ]



        for builtin in builtins:
            pattern = QRegularExpression(f'\\b{builtin}\\b')
            self.highlighting_rules.append((pattern, builtin_format, 'builtins'))


        r, g, b = get_number()
        number_format = QTextCharFormat()
        number_format.setForeground(QColor(r, g, b))

        self.highlighting_rules.append((QRegularExpression('\\b\\d+\\.?\\d*\\b'), number_format, 'number'))

        r, g, b = get_python_function()

        function_format = QTextCharFormat()
        function_format.setForeground(QColor(r, g, b))

        self.highlighting_rules.append((QRegularExpression('\\bdef\\s+(\\w+)'), function_format, 'function'))


        r, g, b = get_python_class()
        self.class_format = QTextCharFormat()
        self.class_format.setForeground(QColor(r, g, b))

        self.highlighting_rules.append((QRegularExpression('\\bclass\\s+(\\w+)'), self.class_format, 'class'))

        self.highlighting_rules.append((
            QRegularExpression(r'^\bimport\s+([a-zA-Z0-9_,\s]+)'), self.class_format, 'import'
        ))

        self.highlighting_rules.append((
            QRegularExpression(r'\bfrom\s+([a-zA-Z0-9_.]+)\s+import\b'), self.class_format, 'Fromimport'
        ))

        # self.highlighting_rules.append((
        #     QRegularExpression(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b(?=\.)'),
        #     self.class_format, 'class'
        # ))

        for punctuation in ['!', '@', '$', '%', '^', '&', '*', '-', '=', '+', '>', '<']:
            punction_format = QTextCharFormat()
            r, g, b = get_punctuation()
            punction_format.setForeground(QColor(r, g, b))

            escaped = QRegularExpression.escape(punctuation)
            punction_regex = QRegularExpression(escaped)
            self.highlighting_rules.append((punction_regex, punction_format, 'punctuation'))

        for bracket in ['(', ')', '{', '}', '[', ']']:
            bracket_format = QTextCharFormat()
            r, g ,b = get_bracket()
            bracket_format.setForeground(QColor(r, g, b))
            escaped = QRegularExpression.escape(bracket)
            bracket_regex = QRegularExpression(escaped)
            self.highlighting_rules.append((bracket_regex, bracket_format, 'bracket'))


        r, g, b = get_python_argument()
        self.arg_def_format = QTextCharFormat()
        self.arg_def_format.setForeground(QColor(r, g, b))


        self.arg_usage_format = QTextCharFormat()
        self.arg_usage_format.setForeground(QColor(r, g, b)) 


        r, g, b = get_python_class()
        self.c_instance_foramt = QTextCharFormat()
        self.c_instance_foramt.setForeground(QColor(r, g, b))

        r, g, b = get_python_function()
        self.function_calls_format = QTextCharFormat()
        self.function_calls_format.setForeground(QColor(r, g, b))

        r, g, b = get_python_method()
        self.method_calls_format = QTextCharFormat()
        self.method_calls_format.setForeground(QColor(r, g, b))

        self.function_args = set()

        self.c_instances = {}


        self.function_calls = set()

        self.class_dots = set()

        if useItalic():
            self.function_calls_format.setFontItalic(True)
            self.method_calls_format.setFontItalic(True)
            self.c_instance_foramt.setFontItalic(True)  
            self.arg_usage_format.setFontItalic(True)
            self.arg_def_format.setFontItalic(True)
            self.class_format.setFontItalic(True)
            function_format.setFontItalic(True)
            self.comment_format.setFontItalic(True)
            builtin_format.setFontItalic(True)

        self.couting = 1

    # def set_code(self, code: str):
    #     try:
    #         tree = ast.parse(code)
    #         self.function_args.clear()
    #         for node in ast.walk(tree):
    #             if isinstance(node, ast.FunctionDef):
    #                 for arg in node.args.args:
    #                     self.function_args.add(arg.arg)
    #     except Exception:
    #         self.function_args.clear()


    def get_calls(self, instances: dict):
        try:
            if instances == self._last_instances:
                return
                
            self.c_instances = instances
            self._last_instances = instances.copy()
            
            self._compiled_patterns.clear()
            
            for name, type_name in instances.items():
                escaped_name = QRegularExpression.escape(name)
                pattern = QRegularExpression(fr"\b{escaped_name}\b")
                self._compiled_patterns[name] = (pattern, type_name)
                
        except Exception:
            self.c_instances.clear()
            self._compiled_patterns.clear()
            self._last_instances.clear()

    def highlight_function_calls(self, calls):
        try:
            self.function_calls.clear()
            for key, value in calls.items():
                if value == 'function':
                    self.function_calls.add(key)
        except Exception:
            self.function_calls.clear()

    # def get_classes(self):
    #     from func_classes import check_class

    #     for classes in check_class:
    #         if not classes:
    #             continue  # skip empty strings

    #         if classes not in self.class_dots:
    #             import re
    #         # Optionally: escape special regex characters in classes
    #             safe_class = re.escape(classes)

    #             pattern = QRegularExpression(rf'\b{safe_class}\b(?=\.)')
    #             if not pattern.isValid():
    #                 print(f"Invalid regex for: {safe_class}")
    #                 continue

    #             self.highlighting_rules.append((pattern, self.class_format, 'class'))
    #         self.class_dots.add(classes)


    def highlightBlock(self, text):
        def is_overlapping(start, length, used_ranges):
            end = start + length
            for begin, finish in used_ranges:
                if start < finish and end > begin:
                    return True
            return False



        if self.useit:
            # self.get_classes()

            default_format = QTextCharFormat()
            default_format.setForeground(QColor("white"))
            self.setFormat(0, len(text), default_format)

            used_ranges = set()

            triple_string_formats = [
                ('"""', QRegularExpression('"""')),
                ("'''", QRegularExpression("'''"))
            ]

            for quote, start_expression in triple_string_formats:
                if self.previousBlockState() != 1:
                    start_match = start_expression.match(text)
                    start_index = start_match.capturedStart() if start_match.hasMatch() else -1
                else:
                    start_index = 0

                while start_index >= 0:
                    end_match = start_expression.match(text, start_index + 3)

                    if end_match.hasMatch():
                        length = end_match.capturedStart() - start_index + 3
                        self.setCurrentBlockState(0)
                    else:
                        self.setCurrentBlockState(1)
                        length = len(text) - start_index

                    string_format = QTextCharFormat()
                    r, g, b = get_string()
                    string_format.setForeground(QColor(r, g, b))

                    self.setFormat(start_index, length, string_format)
                    used_ranges.add((start_index, start_index + length))

                    next_match = start_expression.match(text, start_index + length)
                    start_index = next_match.capturedStart() if next_match.hasMatch() else -1


            for pattern, fmt, name in self.highlighting_rules:
                matches = pattern.globalMatch(text)
                while matches.hasNext():
                    match = matches.next()
                    if name == 'class' or name == 'function' or name == 'import' or name == 'Fromimport':
                        if (name == 'class' and match.captured(1) not in self.class_dots) or (name == 'import' and match.captured(1) not in self.class_dots):

                            if not match.captured(1) or match.captured(1) == '*':
                                continue

                            if match.captured(1) not in self.class_dots:
                                import re
                                safe_class = re.escape(match.captured(1))

                                pattern = QRegularExpression(rf'\b{safe_class}\b(?=\.)')
                                if not pattern.isValid():
                                    print(f"Invalid regex for: {safe_class}")
                                    continue

                                self.highlighting_rules.append((pattern, self.class_format, 'class'))
                            self.class_dots.add(match.captured(1))



                        start = match.capturedStart(1)
                        length = match.capturedLength(1)
                    else:
                        start = match.capturedStart()
                        length = match.capturedLength()

                    if is_overlapping(start, length, used_ranges):
                        continue


                    self.setFormat(start, length, fmt)
                    used_ranges.add((start, start + length))

            self.setCurrentBlockState(0)

            start_expression = QRegularExpression('"""')
            start_match = start_expression.match(text)

            if self.previousBlockState() != 1:
                start_index = start_match.capturedStart() if start_match.hasMatch() else -1
            else:
                start_index = 0

            while start_index >= 0:
                end_expression = QRegularExpression('"""')
                end_match = end_expression.match(text, start_index + 3)

                if end_match.hasMatch():
                    length = end_match.capturedStart() - start_index + end_match.capturedLength()
                    self.setCurrentBlockState(0)
                else:
                    self.setCurrentBlockState(1)
                    length = len(text) - start_index

                string_format = QTextCharFormat()
                r, g, b = get_string()
                string_format.setForeground(QColor(r, g, b))
                self.setFormat(start_index, length, string_format)

                start_match = start_expression.match(text, start_index + length)
                start_index = start_match.capturedStart() if start_match.hasMatch() else -1


            arg_match = QRegularExpression(r"\bdef\s+\w+\s*\(([^)]*)\)").match(text)
            if arg_match.hasMatch():
                args_str = arg_match.captured(1)
                args_start = arg_match.capturedStart(1)



                for arg in args_str.split(','):
                    arg_name = arg.strip().split('=')[0].strip()
                    if arg_name:

                        if is_overlapping(args_start, arg_match.capturedLength(1), used_ranges):
                            continue

                        pos = text.find(arg_name, args_start)
                        if pos != -1:
                            self.setFormat(pos, len(arg_name), self.arg_def_format)
                            used_ranges.add((pos, pos + len(arg_name)))



            for arg in self.function_args:
                pattern = QRegularExpression(fr"\b{arg}\b")
                it = pattern.globalMatch(text)


                while it.hasNext():
                    match = it.next()

                    if is_overlapping(match.capturedStart(), match.capturedLength(), used_ranges):
                        continue

                    self.setFormat(match.capturedStart(), match.capturedLength(), self.arg_usage_format)
                    used_ranges.add((match.capturedStart(), match.capturedStart() + match.capturedLength()))


            try:
                for name, (pattern, type_name) in self._compiled_patterns.items():
                    it = pattern.globalMatch(text)
                    while it.hasNext():
                        match = it.next()

                        if is_overlapping(match.capturedStart(), match.capturedLength(), used_ranges):
                            continue

                        if type_name == 'class':
                            # self.setFormat(match.capturedStart(), match.capturedLength(), self.c_instance_foramt)
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.c_instance_foramt)

                        elif type_name == 'function':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.function_calls_format)
                        elif type_name == 'method':
                            # print(name)
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.method_calls_format)
                        # elif type_name == 'attribute':
                        #     print(name)
                            # self.setFormat(match.capturedStart(), match.capturedLength(), self.c_instance_foramt)
                        # elif type_name == 'variable':
                        #     self.setFormat(match.capturedStart(), match.capturedLength(), self.function_calls_format)
                        elif type_name == 'module':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.class_format)
                            # self.setFormat(match.capturedStart(), match.capturedLength(), self.function_calls_format)
                        elif type_name == 'import' or type_name == 'Fromimport':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.class_format)
                            # self.setFormat(match.capturedStart(), match.capturedLength(), self.function_calls_format)


                        elif type_name == 'args':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.func_args_format)


                        used_ranges.add((match.capturedStart(), match.capturedStart() + match.capturedLength()))


            except RuntimeError:
                pass

            string_matches = []
            match_it = self.string_pattern.globalMatch(text)
            while match_it.hasNext():
                match = match_it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), self.string_format)
                string_matches.append((match.capturedStart(), match.capturedEnd()))

            # Then, highlight comments **only if they are outside string ranges**
            match_it = self.comment_pattern.globalMatch(text)
            while match_it.hasNext():
                match = match_it.next()
                start, end = match.capturedStart(), match.capturedEnd()

                # Check if inside any string range
                if not any(s <= start < e for s, e in string_matches):
                    self.setFormat(start, end - start, self.comment_format)


class ConfigSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self,use_highlighter ,parent=None):
        super().__init__(parent)

        self.useit = use_highlighter

        if self.useit:
            self.highlighting_rules = []
            self.setup_highlighting_rules()

        else:
            pass


    def setup_highlighting_rules(self):
        comment_format = QTextCharFormat()
        r, g, b = get_comment()
        comment_format.setForeground(QColor(r, g, b))
        self.highlighting_rules.append((QRegularExpression(';[^\n]*'), comment_format, 'comment'))

        r, g, b = get_string()
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(r, g, b))
        self.highlighting_rules.append((QRegularExpression('"[^"\\\\]*(\\\\.[^"\\\\]*)*"'), string_format, 'string'))
        self.highlighting_rules.append((QRegularExpression("'[^'\\\\]*(\\\\.[^'\\\\]*)*'"), string_format, 'string'))

        r, g, b = get_number()
        number_format = QTextCharFormat()
        number_format.setForeground(QColor(r, g, b))

        self.highlighting_rules.append((QRegularExpression('\\b\\d+\\.?\\d*\\b'), number_format, 'number'))


        r, g, b = get_config_section()
        section_format = QTextCharFormat()
        section_format.setForeground(QColor(r, g, b))

        self.highlighting_rules.append((QRegularExpression('\[.*?\]'), section_format, 'section'))

        r, g, b = get_config_option()
        variable_format = QTextCharFormat()
        variable_format.setForeground(QColor(r, g, b))  # Blue

        self.highlighting_rules.append((QRegularExpression(r'^\s*[\w-]+(?=\s*=)'), variable_format, 'variable'))
        self.highlighting_rules.append((QRegularExpression('^\s*\w+(?=\s*=)'), variable_format, 'variable'))
        self.highlighting_rules.append((QRegularExpression('^\s*\w+(?=\s* )'), variable_format, 'variable'))
        self.highlighting_rules.append((QRegularExpression(r'\b\w+(?=\s*=)'), variable_format, 'variable'))


        for bracket in ['(', ')', '{', '}', '[', ']']:
            bracket_format = QTextCharFormat()
            r, g, b = get_bracket()
            bracket_format.setForeground(QColor(r, g, b))
            escaped = QRegularExpression.escape(bracket)
            bracket_regex = QRegularExpression(escaped)
            self.highlighting_rules.append((bracket_regex, bracket_format, 'bracket'))

        if useItalic():
            comment_format.setFontItalic(True)
            variable_format.setFontItalic(True)
            section_format.setFontItalic(True)


    def highlightBlock(self, text):

        def is_overlapping(start, length, used_ranges):
            end = start + length
            for begin, finish in used_ranges:
                if start < finish and end > begin:
                    return True
            return False

        used_ranges = set()

        for pattern, fmt, name in self.highlighting_rules:


            matches = pattern.globalMatch(text)
            while matches.hasNext():
                match = matches.next()

                start = match.capturedStart()
                length = match.capturedLength()

                if is_overlapping(start, length, used_ranges):
                    continue


                self.setFormat(start, length, fmt)
                used_ranges.add((start, start + length))


class JsonSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self,use_highlighter ,parent=None):
        super().__init__(parent)

        self.useit = use_highlighter

        if self.useit:
            self.highlighting_rules = []
            self.setup_highlighting_rules()

        else:
            pass


    def setup_highlighting_rules(self):
        r, g, b = get_string()
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(r, g, b))
        self.highlighting_rules.append((QRegularExpression('"[^"\\\\]*(\\\\.[^"\\\\]*)*"'), string_format, 'string'))


        r, g, b = get_comment()
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(r, g, b))
        # comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression('//[^\n]*'), comment_format, 'comment'))


        r, g, b = get_json_boolean()
        boolean = QTextCharFormat()
        boolean.setForeground(QColor(r, g, b))

        self.highlighting_rules.append((QRegularExpression('true'), boolean, 'bool'))
        self.highlighting_rules.append((QRegularExpression('false'), boolean, 'bool'))

        r, g, b = get_number()
        number_format = QTextCharFormat()
        number_format.setForeground(QColor(r, g, b))

        self.highlighting_rules.append((QRegularExpression('\\b\\d+\\.?\\d*\\b'), number_format, 'number'))


        # for punctuation in ['#', '!', '@', '$', '%', '^', '&', '*', '-', '=', '+']:
        #     punction_format = QTextCharFormat()
        #     punction_format.setForeground(QColor(243, 139, 168))

        #     escaped = QRegularExpression.escape(punctuation)
        #     punction_regex = QRegularExpression(escaped)
        #     self.highlighting_rules.append((punction_regex, punction_format, 'punctuation'))


        for bracket in ['{', '}']:
            bracket_format = QTextCharFormat()
            r, g, b = get_number()
            bracket_format.setForeground(QColor(r, g, b))
            escaped = QRegularExpression.escape(bracket)
            bracket_regex = QRegularExpression(escaped)
            self.highlighting_rules.append((bracket_regex, bracket_format, 'bracket'))

        for bracket in ['(', ')', '[', ']']:
            bracket_format = QTextCharFormat()
            r, g, b = get_bracket()
            bracket_format.setForeground(QColor(r, g, b))
            escaped = QRegularExpression.escape(bracket)
            bracket_regex = QRegularExpression(escaped)
            self.highlighting_rules.append((bracket_regex, bracket_format, 'bracket'))

        if useItalic():
            comment_format.setFontItalic(True)


    def highlightBlock(self, text):
        def is_overlapping(start, length, used_ranges):
            end = start + length
            for begin, finish in used_ranges:
                if start < finish and end > begin:
                    return True
            return False

        used_ranges = set()

        for pattern, fmt, name in self.highlighting_rules:


            matches = pattern.globalMatch(text)
            while matches.hasNext():
                match = matches.next()

                start = match.capturedStart()
                length = match.capturedLength()

                if is_overlapping(start, length, used_ranges):
                    continue

                self.setFormat(start, length, fmt)
                used_ranges.add((start, start + length))


class CssSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self,use_highlighter ,parent=None):
        super().__init__(parent)

        self.useit = use_highlighter

        if self.useit:
            self.highlighting_rules = []
            self.setup_highlighting_rules()

        else:
            pass


    def setup_highlighting_rules(self):
        r, g, b = get_comment()
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(r, g, b))
        # comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression('/\*.*?\*/'), comment_format, 'comment'))


        r, g, b = get_string()
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(r, g, b))
        self.highlighting_rules.append((QRegularExpression('"[^"\\\\]*(\\\\.[^"\\\\]*)*"'), string_format, 'string'))
        self.highlighting_rules.append((QRegularExpression("'[^'\\\\]*(\\\\.[^'\\\\]*)*'"), string_format, 'string'))

        # class_format = QTextCharFormat()
        # class_format.setForeground(QColor(249, 226, 175))

        r, g, b = get_css_class()
        self.class_format = QTextCharFormat()
        self.class_format.setForeground(QColor(r, g, b))  # Choose your color
        # class_format.setFontWeight(QFont.Weight.Bold)
        # class_format.setFontItalic(True)

        self.highlighting_rules.append((
            QRegularExpression(r'#(?![0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?\b)[\w-]+'),
            self.class_format,
            'css-id'
        ))

        self.highlighting_rules.append((
            QRegularExpression(r'\.(?!\d)\w[\w-]*'),
            self.class_format,
            'css-class'
        ))


        r, g, b = get_css_hexcolor()
        color_format = QTextCharFormat()
        color_format.setForeground(QColor(r, g, b))

        self.highlighting_rules.append((
            QRegularExpression(r'#(?:[0-9a-fA-F]{3}){1,2}\b'),
            color_format,
            'hex-color'
        ))

        r, g, b = get_css_property()
        property_format = QTextCharFormat()
        property_format.setForeground(QColor(r, g, b))
        # property_format.setFontWeight(QFont.Weight.Bold)
        # property_format.setFontItalic(True)

        self.highlighting_rules.append((QRegularExpression(r'[a-zA-Z-]+(?=:)'), property_format, 'property'))

        r, g, b = get_number()

        number_format = QTextCharFormat()
        number_format.setForeground(QColor(r, g, b))

        self.highlighting_rules.append((QRegularExpression(r'\b\d+\.?\d*(px|em|rem|%|vh|vw|vmin|vmax|pt|cm|mm|in)?\b'), number_format, 'number')
)
        r, g, b = get_css_none()
        none_format = QTextCharFormat()
        none_format.setForeground(QColor(r, g, b))


        self.highlighting_rules.append((QRegularExpression('none'), none_format, 'none'))


        # for punctuation in ['!', '@', '$', '%', '^', '&', '*', '-', '=', '+']:
        #     punction_format = QTextCharFormat()
        #     punction_format.setForeground(QColor(243, 139, 168))

        #     escaped = QRegularExpression.escape(punctuation)
        #     punction_regex = QRegularExpression(escaped)
        #     self.highlighting_rules.append((punction_regex, punction_format, 'punctuation'))


        for bracket in ['(', ')', '[', ']', '{', '}']:
            bracket_format = QTextCharFormat()
            r, g, b = get_bracket()
            bracket_format.setForeground(QColor(r, g, b))
            escaped = QRegularExpression.escape(bracket)
            bracket_regex = QRegularExpression(escaped)
            self.highlighting_rules.append((bracket_regex, bracket_format, 'bracket'))

        if useItalic():
            comment_format.setFontItalic(True)
            self.class_format.setFontItalic(True)
            property_format.setFontItalic(True)


    def highlightBlock(self, text):
        def is_overlapping(start, length, used_ranges):
            end = start + length
            for begin, finish in used_ranges:
                if start < finish and end > begin:
                    return True
            return False

        used_ranges = set()

        for pattern, fmt, name in self.highlighting_rules:


            matches = pattern.globalMatch(text)
            while matches.hasNext():
                match = matches.next()

                start = match.capturedStart()
                length = match.capturedLength()

                if is_overlapping(start, length, used_ranges):
                    continue

                self.setFormat(start, length, fmt)
                used_ranges.add((start, start + length))



class MarkdownSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self,use_highlighter ,parent=None):
        super().__init__(parent)

        self.useit = use_highlighter

        if self.useit:
            self.highlighting_rules = []
            self.setup_highlighting_rules()

        else:
            pass


    def setup_highlighting_rules(self):
        r, g, b = get_comment()
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(r, g, b))
        # comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression('<!--.*?-->'), comment_format, 'comment'))


        r, g, b = get_markdown_backtick()
        command_format = QTextCharFormat()
        command_format.setForeground(QColor(r, g, b))

        self.highlighting_rules.append((QRegularExpression(r'``([^`]+)``'), command_format, 'command_format'))
        self.highlighting_rules.append((QRegularExpression(r'(`{1,3})(?!\1)(.*?)\1'), command_format, 'inline_code'))


        r, g, b = get_markdown_strikeThrough()
        strikethrough_format = QTextCharFormat()
        strikethrough_format.setForeground(QColor(r, g, b))
        strikethrough_format.setFontStrikeOut(True)


        self.highlighting_rules.append((QRegularExpression(r'~~(.*?)~~'), strikethrough_format, 'strikethrough_format'))

        r, g, b = get_markdown_bracket()
        brackets_format = QTextCharFormat()
        brackets_format.setForeground(QColor(r, g, b))
        # brackets_format.setFontWeight(QFont.Weight.Bold)
        # brackets_format.setFontItalic(True)

        self.highlighting_rules.append((QRegularExpression('\[.*?\]'), brackets_format, 'brackets'))
        self.highlighting_rules.append((QRegularExpression('^\{.*?\}'), brackets_format, 'braces'))
        self.highlighting_rules.append((QRegularExpression('^\(.*?\)'), brackets_format, 'brackets'))

        r, g, b = get_markdown_equal()
        equal_format = QTextCharFormat()
        equal_format.setForeground(QColor(r, g, b))

        self.highlighting_rules.append((QRegularExpression('^={3,}'), equal_format, 'equal'))


        r, g, b = get_markdown_line()
        line_format = QTextCharFormat()
        line_format.setForeground(QColor(r, g, b))

        self.highlighting_rules.append((QRegularExpression('^-{3,}'), line_format, 'line'))
        self.highlighting_rules.append((QRegularExpression('^_{3,}'), line_format, 'line'))
        self.highlighting_rules.append((QRegularExpression(r'^\*{3,}'), line_format, 'line'))

        r, g, b = get_markdown_header1()
        header_1_format = QTextCharFormat()
        header_1_format.setForeground(QColor(r, g, b))  
        # header_1_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression('^# [^\n]*'), header_1_format, 'header1'))


        r, g, b = get_markdown_header2()
        header_2_format = QTextCharFormat()
        header_2_format.setForeground(QColor(r, g, b))  
        # header_2_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression('^## [^\n]*'), header_2_format, 'header2'))

        r, g, b = get_markdown_header3()
        header_3_format = QTextCharFormat()
        header_3_format.setForeground(QColor(r, g, b))  
        # header_3_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression('^### [^\n]*'), header_3_format, 'header3'))

        r, g, b = get_markdown_header4()
        header_4_format = QTextCharFormat()
        header_4_format.setForeground(QColor(r, g, b))  
        # header_4_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression('^#### [^\n]*'), header_4_format, 'header4'))


        r, g, b = get_markdown_header5()
        header_5_format = QTextCharFormat()
        header_5_format.setForeground(QColor(r, g, b))  
        # header_5_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression('^##### [^\n]*'), header_5_format, 'header5'))


        r, g, b = get_markdown_header6()
        header_6_format = QTextCharFormat()
        header_6_format.setForeground(QColor(r, g, b))  
        # header_6_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression('^###### [^\n]*'), header_6_format, 'header1'))


        r, g, b = get_markdown_italicBold()
        italic_bold_format = QTextCharFormat()
        italic_bold_format.setForeground(QColor(r, g, b))  
        italic_bold_format.setFontItalic(True)
        italic_bold_format.setFontWeight(QFont.Weight.Bold)

        self.highlighting_rules.append((QRegularExpression(r'\*\*\*(.+?)\*\*\*'), italic_bold_format, 'italic_bold'))

        r, g, b = get_markdown_bold()
        bold_format = QTextCharFormat()
        bold_format.setForeground(QColor(r, g, b))  
        bold_format.setFontWeight(QFont.Weight.Bold)

        self.highlighting_rules.append((QRegularExpression(r'\*\*(.*?)\*\*'), bold_format, 'bold_*'))
        self.highlighting_rules.append((QRegularExpression(r'__(.*?)__'), bold_format, 'bold_underscore'))


        r, g, b = get_markdown_italic()
        italic_format = QTextCharFormat()
        italic_format.setForeground(QColor(r, g, b))  
        italic_format.setFontItalic(True)

        self.highlighting_rules.append((QRegularExpression(r'\*(.*?)\*'), italic_format, 'italic_format'))

        r, g, b = get_markdown_blockQotes()
        blockqotes_format = QTextCharFormat()
        blockqotes_format.setForeground(QColor(r, g, b))  
        # blockqotes_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression('^> [^\n]*'), blockqotes_format, 'blockqotes_format'))

        r, g, b = get_number()
        number_format = QTextCharFormat()
        number_format.setForeground(QColor(r, g, b))

        self.highlighting_rules.append((QRegularExpression('^\\b\\d+\\.?\\d*\\b. '), number_format, 'number'))

        r, g, b = get_markdown_unordered()
        unordered_format = QTextCharFormat()
        unordered_format.setForeground(QColor(r, g, b))

        self.highlighting_rules.append((QRegularExpression(r'^- [^\n]*'), unordered_format, 'unordered_format'))
        self.highlighting_rules.append((QRegularExpression(r'^\+ [^\n]*'), unordered_format, 'unordered_format'))
        self.highlighting_rules.append((QRegularExpression(r'^\* [^\n]*'), unordered_format, 'unordered_format'))



        for bracket in ['(', ')', '[', ']', '{', '}']:
            bracket_format = QTextCharFormat()
            r, g, b = get_bracket()
            bracket_format.setForeground(QColor(r, g, b))
            escaped = QRegularExpression.escape(bracket)
            bracket_regex = QRegularExpression(escaped)
            self.highlighting_rules.append((bracket_regex, bracket_format, 'bracket'))

        if useItalic():
            blockqotes_format.setFontItalic(True)
            header_1_format.setFontItalic(True)
            header_2_format.setFontItalic(True)
            header_3_format.setFontItalic(True)
            header_4_format.setFontItalic(True)
            header_5_format.setFontItalic(True)
            header_6_format.setFontItalic(True)
            comment_format.setFontItalic(True)


    def highlightBlock(self, text):
        def is_overlapping(start, length, used_ranges):
            end = start + length
            for begin, finish in used_ranges:
                if start < finish and end > begin:
                    return True
            return False

        used_ranges = set()

        for pattern, fmt, name in self.highlighting_rules:


            matches = pattern.globalMatch(text)
            while matches.hasNext():
                match = matches.next()

                start = match.capturedStart()
                length = match.capturedLength()

                if is_overlapping(start, length, used_ranges):
                    continue

                self.setFormat(start, length, fmt)
                used_ranges.add((start, start + length))