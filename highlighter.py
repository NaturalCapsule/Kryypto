import ast
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt6.QtCore import QRegularExpression


class PythonSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self,use_highlighter ,parent=None):
        super().__init__(parent)

        self.useit = use_highlighter

        if self.useit:
            self.highlighting_rules = []
            self.setup_highlighting_rules()

        else:
            pass

    def setup_highlighting_rules(self):
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(203, 166, 247))  # Blue
        # keyword_format.setForeground(QColor(85, 85, 255))  # Blue
        keyword_format.setFontWeight(QFont.Weight.Bold)


        string_format = QTextCharFormat()
        # string_format.setForeground(QColor(0, 128, 0))  # Green
        string_format.setForeground(QColor(166, 227, 161))  # Green

        self.highlighting_rules.append((QRegularExpression('"[^"\\\\]*(\\\\.[^"\\\\]*)*"'), string_format, 'string'))
        self.highlighting_rules.append((QRegularExpression("'[^'\\\\]*(\\\\.[^'\\\\]*)*'"), string_format, 'string'))
        

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

        builtin_format = QTextCharFormat()
        # builtin_format.setForeground(QColor(243, 139, 168))
        # builtin_format.setForeground(QColor(203, 166, 247))  # Blue
        builtin_format.setForeground(QColor(137, 180, 250))  # Blue
        builtin_format.setFontItalic(True)

        # builtin_format.setForeground(QColor(170, 85, 0))  # Orange
        builtin_format.setFontWeight(QFont.Weight.Bold)
        
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




        # self.highlighting_rules.append((QRegularExpression('""".*"""'), string_format, 'string'))
        # self.highlighting_rules.append((QRegularExpression("'''.*'''"), string_format, 'string'))

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(128, 128, 128))  
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression('#[^\n]*'), comment_format, 'comment'))

        number_format = QTextCharFormat()
        # number_format.setForeground(QColor(255, 0, 255))  # Magenta
        number_format.setForeground(QColor(250, 179, 135))  # Magenta

        self.highlighting_rules.append((QRegularExpression('\\b\\d+\\.?\\d*\\b'), number_format, 'number'))

        function_format = QTextCharFormat()
        function_format.setForeground(QColor(137, 180, 250))  # Blue
        # function_format.setForeground(QColor(0, 255, 255))  # Blue
        function_format.setFontWeight(QFont.Weight.Bold)
        # self.arg_def_format.setFontWeight(QFont.Weight.Bold)
        function_format.setFontItalic(True)

        self.highlighting_rules.append((QRegularExpression('\\bdef\\s+(\\w+)'), function_format, 'function'))

        class_format = QTextCharFormat()
        class_format.setForeground(QColor(249, 226, 175))  # Purple
        # class_format.setForeground(QColor(128, 0, 128))  # Purple
        class_format.setFontWeight(QFont.Weight.Bold)
                # self.arg_def_format.setFontWeight(QFont.Weight.Bold)
        class_format.setFontItalic(True)

        self.highlighting_rules.append((QRegularExpression('\\bclass\\s+(\\w+)'), class_format, 'class'))


        for punctuation in ['!', '@', '$', '%', '^', '&', '*', '-', '=', '+', '>', '<']:
            punction_format = QTextCharFormat()
            # punction_format.setForeground(QColor(255, 0, 0))  # Red
            punction_format.setForeground(QColor(243, 139, 168))  # Orange

            escaped = QRegularExpression.escape(punctuation)
            punction_regex = QRegularExpression(escaped)
            self.highlighting_rules.append((punction_regex, punction_format, 'punctuation'))

        for bracket in ['(', ')', '{', '}', '[', ']']:
            bracket_format = QTextCharFormat()
            bracket_format.setForeground(QColor(243, 139, 168))
            escaped = QRegularExpression.escape(bracket)
            bracket_regex = QRegularExpression(escaped)
            self.highlighting_rules.append((bracket_regex, bracket_format, 'bracket'))

        self.arg_def_format = QTextCharFormat()
        # self.arg_def_format.setForeground(QColor("purple"))
        self.arg_def_format.setForeground(QColor(243, 139, 168))  # Orange

        self.arg_def_format.setFontWeight(QFont.Weight.Bold)
        self.arg_def_format.setFontItalic(True)

        self.arg_usage_format = QTextCharFormat()
        # self.arg_usage_format.setForeground(QColor("darkMagenta"))
        self.arg_usage_format.setForeground(QColor(205, 214, 244))
        self.arg_usage_format.setForeground(QColor(243, 139, 168))  # Orange


        self.arg_usage_format.setFontWeight(QFont.Weight.Bold)
        self.arg_usage_format.setFontItalic(True)



        self.c_instance_foramt = QTextCharFormat()
        self.c_instance_foramt.setForeground(QColor(249, 226, 175))

        self.c_instance_foramt.setFontWeight(QFont.Weight.Bold)  # Make class names bold
        self.c_instance_foramt.setFontItalic(True)  


        self.function_calls_format = QTextCharFormat()
        # self.function_calls_format.setForeground(QColor(0, 255, 255))
        self.function_calls_format.setForeground(QColor(137, 180, 250))  # Blue

        self.function_calls_format.setFontWeight(QFont.Weight.Bold)
        self.function_calls_format.setFontItalic(True)
        # variable_formar = QTextCharFormat()
        # variable_formar.setForeground(QColor(0, 128, 0))  # Dark green
        # assignment_format.setFontWeight(QFont.Weight.Bold)

        # Regex explanation:
        #   \b       = word boundary
        #   \w+      = variable name
        #   \s*=\s*  = equals with optional spaces
        #   \w+      = class or identifier



        #assignment_regex = QRegularExpression(r'\b(\w+)\s*=\s*')
        # this works try it on..!!
        # assignment_regex = QRegularExpression(r'\b(\w+)\s*=')
        # variable_regex = QRegularExpression(r'\b(\w+)\s*=')
        # self.highlighting_rules.append((variable_regex, variable_formar, 'variable'))

        self.function_args = set()

        # self.c_instances = set()
        self.c_instances = {}


        self.function_calls = set()

    def set_code(self, code: str):
        try:
            tree = ast.parse(code)
            self.function_args.clear()
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    for arg in node.args.args:
                        self.function_args.add(arg.arg)
        except Exception:
            self.function_args.clear()


    def get_calls(self, instances: dict):
        try:
            self.c_instances = instances
        except Exception:
            self.c_instances.clear()

    def highlight_function_calls(self, calls):
        try:
            self.function_calls.clear()
            for key, value in calls.items():
                if value == 'function':
                    self.function_calls.add(key)
        except Exception:
            # self.c_instances.clear()
            self.function_calls.clear()

    def highlightBlock(self, text):
        def is_overlapping(start, length, used_ranges):
            end = start + length
            for begin, finish in used_ranges:
                if start < finish and end > begin:
                    return True
            return False


        if self.useit:

            default_format = QTextCharFormat()
            default_format.setForeground(QColor("white"))
            default_format.setFontWeight(QFont.Weight.Bold)
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
                    string_format.setForeground(QColor(166, 227, 161))  # Green
                    # string_format.setForeground(QColor(0, 128, 0))  # Green
                    self.setFormat(start_index, length, string_format)
                    used_ranges.add((start_index, start_index + length))

                    next_match = start_expression.match(text, start_index + length)
                    start_index = next_match.capturedStart() if next_match.hasMatch() else -1

            comment_format = QTextCharFormat()
            comment_format.setForeground(QColor(108, 112, 134))  
            # comment_format.setForeground(QColor(128, 128, 128))  
            comment_format.setFontItalic(True)

            comment_regex = QRegularExpression(r'#[^\n]*')
            comment_matcher = comment_regex.globalMatch(text)
            while comment_matcher.hasNext():
                match = comment_matcher.next()
                start = match.capturedStart()
                length = match.capturedLength()
                self.setFormat(start, length, comment_format)
                used_ranges.add((start, start + length))

            for pattern, fmt, name in self.highlighting_rules:
                if name == 'comment':
                    continue

                matches = pattern.globalMatch(text)
                while matches.hasNext():
                    match = matches.next()
                    if name == 'class' or name == 'function':
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
                string_format.setForeground(QColor(166, 227, 161))  # Green
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
                for call, type in self.c_instances.items():
                    pattern = QRegularExpression(fr"\b{call}\b")
                    it = pattern.globalMatch(text)
                    while it.hasNext():
                        match = it.next()

                        if is_overlapping(match.capturedStart(), match.capturedLength(), used_ranges):
                            continue


                        if type == 'class':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.c_instance_foramt)
                        elif type == 'function':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.function_calls_format)

                        used_ranges.add((match.capturedStart(), match.capturedStart() + match.capturedLength()))

            except RuntimeError:
                pass
                # self.c_instances.clear()

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
        comment_format.setForeground(QColor(128, 128, 128))
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression(';[^\n]*'), comment_format, 'comment'))


        string_format = QTextCharFormat()
        string_format.setForeground(QColor(166, 227, 161))
        self.highlighting_rules.append((QRegularExpression('"[^"\\\\]*(\\\\.[^"\\\\]*)*"'), string_format, 'string'))
        self.highlighting_rules.append((QRegularExpression("'[^'\\\\]*(\\\\.[^'\\\\]*)*'"), string_format, 'string'))


        number_format = QTextCharFormat()
        number_format.setForeground(QColor(250, 179, 135))

        self.highlighting_rules.append((QRegularExpression('\\b\\d+\\.?\\d*\\b'), number_format, 'number'))

        section_format = QTextCharFormat()
        section_format.setForeground(QColor(249, 226, 175))
        section_format.setFontWeight(QFont.Weight.Bold)
        section_format.setFontItalic(True)

        self.highlighting_rules.append((QRegularExpression('\[.*?\]'), section_format, 'section'))

        variable_format = QTextCharFormat()
        variable_format.setForeground(QColor(137, 180, 250))  # Blue

        variable_format.setFontWeight(QFont.Weight.Bold)
        variable_format.setFontItalic(True)

        self.highlighting_rules.append((QRegularExpression('^\s*\w+(?=\s*=)'), variable_format, 'variable'))
        self.highlighting_rules.append((QRegularExpression('^\s*\w+(?=\s* )'), variable_format, 'variable'))
        self.highlighting_rules.append((QRegularExpression(r'\b\w+(?=\s*=)'), variable_format, 'variable'))


        for punctuation in ['#', '!', '@', '$', '%', '^', '&', '*', '-', '=', '+']:
            punction_format = QTextCharFormat()
            punction_format.setForeground(QColor(243, 139, 168))

            escaped = QRegularExpression.escape(punctuation)
            punction_regex = QRegularExpression(escaped)
            self.highlighting_rules.append((punction_regex, punction_format, 'punctuation'))

        for bracket in ['(', ')', '{', '}', '[', ']']:
            bracket_format = QTextCharFormat()
            bracket_format.setForeground(QColor(243, 139, 168))
            escaped = QRegularExpression.escape(bracket)
            bracket_regex = QRegularExpression(escaped)
            self.highlighting_rules.append((bracket_regex, bracket_format, 'bracket'))



        # string_format = QTextCharFormat()
        # string_format.setForeground(QColor(166, 227, 161))

        # self.highlighting_rules.append((QRegularExpression('"[^"\\\\]*(\\\\.[^"\\\\]*)*"'), string_format, 'string'))
        # self.highlighting_rules.append((QRegularExpression("'[^'\\\\]*(\\\\.[^'\\\\]*)*'"), string_format, 'string'))



        # variable_formar = QTextCharFormat()
        # variable_formar.setForeground(QColor(0, 128, 0))  # Dark green
        # assignment_format.setFontWeight(QFont.Weight.Bold)

        # Regex explanation:
        #   \b       = word boundary
        #   \w+      = variable name
        #   \s*=\s*  = equals with optional spaces
        #   \w+      = class or identifier



        #assignment_regex = QRegularExpression(r'\b(\w+)\s*=\s*')
        # this works try it on..!!
        # assignment_regex = QRegularExpression(r'\b(\w+)\s*=')
        # variable_regex = QRegularExpression(r'\b(\w+)\s*=')
        # self.highlighting_rules.append((variable_regex, variable_formar, 'variable'))


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
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(166, 227, 161))
        self.highlighting_rules.append((QRegularExpression('"[^"\\\\]*(\\\\.[^"\\\\]*)*"'), string_format, 'string'))

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(128, 128, 128))
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression('//[^\n]*'), comment_format, 'comment'))


        boolean = QTextCharFormat()
        boolean.setForeground(QColor(0, 179, 135))

        self.highlighting_rules.append((QRegularExpression('true'), boolean, 'bool'))
        self.highlighting_rules.append((QRegularExpression('false'), boolean, 'bool'))


        number_format = QTextCharFormat()
        number_format.setForeground(QColor(250, 179, 135))

        self.highlighting_rules.append((QRegularExpression('\\b\\d+\\.?\\d*\\b'), number_format, 'number'))


        for punctuation in ['#', '!', '@', '$', '%', '^', '&', '*', '-', '=', '+']:
            punction_format = QTextCharFormat()
            punction_format.setForeground(QColor(243, 139, 168))

            escaped = QRegularExpression.escape(punctuation)
            punction_regex = QRegularExpression(escaped)
            self.highlighting_rules.append((punction_regex, punction_format, 'punctuation'))


        for bracket in ['{', '}']:
            bracket_format = QTextCharFormat()
            bracket_format.setForeground(QColor(249, 226, 175))
            escaped = QRegularExpression.escape(bracket)
            bracket_regex = QRegularExpression(escaped)
            self.highlighting_rules.append((bracket_regex, bracket_format, 'bracket'))

        for bracket in ['(', ')', '[', ']']:
            bracket_format = QTextCharFormat()
            bracket_format.setForeground(QColor(243, 139, 168))
            escaped = QRegularExpression.escape(bracket)
            bracket_regex = QRegularExpression(escaped)
            self.highlighting_rules.append((bracket_regex, bracket_format, 'bracket'))

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
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(128, 128, 128))
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression('/\*.*?\*/'), comment_format, 'comment'))


        string_format = QTextCharFormat()
        string_format.setForeground(QColor(166, 227, 161))
        self.highlighting_rules.append((QRegularExpression('"[^"\\\\]*(\\\\.[^"\\\\]*)*"'), string_format, 'string'))
        self.highlighting_rules.append((QRegularExpression("'[^'\\\\]*(\\\\.[^'\\\\]*)*'"), string_format, 'string'))

        # class_format = QTextCharFormat()
        # class_format.setForeground(QColor(249, 226, 175))


        class_format = QTextCharFormat()
        class_format.setForeground(QColor(249, 226, 175))  # Choose your color
        class_format.setFontWeight(QFont.Weight.Bold)
        class_format.setFontItalic(True)

        self.highlighting_rules.append((
            QRegularExpression(r'#(?![0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?\b)[\w-]+'),
            class_format,
            'css-id'
        ))

        self.highlighting_rules.append((
            QRegularExpression(r'\.(?!\d)\w[\w-]*'),
            class_format,
            'css-class'
        ))

        color_format = QTextCharFormat()
        color_format.setForeground(QColor(203, 166, 247))

        self.highlighting_rules.append((
            QRegularExpression(r'#(?:[0-9a-fA-F]{3}){1,2}\b'),
            color_format,
            'hex-color'
        ))


        property_format = QTextCharFormat()
        property_format.setForeground(QColor(137, 180, 250))
        property_format.setFontWeight(QFont.Weight.Bold)
        property_format.setFontItalic(True)

        self.highlighting_rules.append((QRegularExpression(r'[a-zA-Z-]+(?=:)'), property_format, 'property'))

        number_format = QTextCharFormat()
        number_format.setForeground(QColor(250, 179, 135))

        self.highlighting_rules.append((QRegularExpression(r'\b\d+\.?\d*(px|em|rem|%|vh|vw|vmin|vmax|pt|cm|mm|in)?\b'), number_format, 'number')
)

        none_format = QTextCharFormat()
        none_format.setForeground(QColor(243, 139, 168))


        self.highlighting_rules.append((QRegularExpression('none'), none_format, 'none'))


        for punctuation in ['!', '@', '$', '%', '^', '&', '*', '-', '=', '+']:
            punction_format = QTextCharFormat()
            punction_format.setForeground(QColor(243, 139, 168))

            escaped = QRegularExpression.escape(punctuation)
            punction_regex = QRegularExpression(escaped)
            self.highlighting_rules.append((punction_regex, punction_format, 'punctuation'))


        for bracket in ['(', ')', '[', ']', '{', '}']:
            bracket_format = QTextCharFormat()
            bracket_format.setForeground(QColor(243, 139, 168))
            escaped = QRegularExpression.escape(bracket)
            bracket_regex = QRegularExpression(escaped)
            self.highlighting_rules.append((bracket_regex, bracket_format, 'bracket'))

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
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(128, 128, 128))
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression('<!--.*?-->'), comment_format, 'comment'))

        command_format = QTextCharFormat()
        command_format.setForeground(QColor(249, 226, 175))

        self.highlighting_rules.append((QRegularExpression(r'``([^`]+)``'), command_format, 'command_format'))
        self.highlighting_rules.append((QRegularExpression(r'(`{1,3})(?!\1)(.*?)\1'), command_format, 'inline_code'))



        strikethrough_format = QTextCharFormat()
        strikethrough_format.setForeground(QColor("gray"))
        strikethrough_format.setFontStrikeOut(True)


        self.highlighting_rules.append((QRegularExpression(r'~~(.*?)~~'), strikethrough_format, 'strikethrough_format'))

        brackets_format = QTextCharFormat()
        brackets_format.setForeground(QColor(249, 226, 175))
        brackets_format.setFontWeight(QFont.Weight.Bold)
        brackets_format.setFontItalic(True)

        self.highlighting_rules.append((QRegularExpression('\[.*?\]'), brackets_format, 'brackets'))
        self.highlighting_rules.append((QRegularExpression('^\{.*?\}'), brackets_format, 'braces'))
        self.highlighting_rules.append((QRegularExpression('^\(.*?\)'), brackets_format, 'brackets'))


        equal_format = QTextCharFormat()
        equal_format.setForeground(QColor(243, 139, 168))

        self.highlighting_rules.append((QRegularExpression('^={3,}'), equal_format, 'equal'))

        line_format = QTextCharFormat()
        line_format.setForeground(QColor(243, 255, 0))

        self.highlighting_rules.append((QRegularExpression('^-{3,}'), line_format, 'line'))
        self.highlighting_rules.append((QRegularExpression('^_{3,}'), line_format, 'line'))
        self.highlighting_rules.append((QRegularExpression(r'^\*{3,}'), line_format, 'line'))


        header_1_format = QTextCharFormat()
        header_1_format.setForeground(QColor(0, 0, 144))  
        header_1_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression('^# [^\n]*'), header_1_format, 'header1'))



        header_2_format = QTextCharFormat()
        header_2_format.setForeground(QColor(0, 144, 144))  
        header_2_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression('^## [^\n]*'), header_2_format, 'header2'))


        header_3_format = QTextCharFormat()
        header_3_format.setForeground(QColor(0, 0, 255))  
        header_3_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression('^### [^\n]*'), header_3_format, 'header3'))


        header_4_format = QTextCharFormat()
        header_4_format.setForeground(QColor(0, 0, 200))  
        header_4_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression('^#### [^\n]*'), header_4_format, 'header4'))



        header_5_format = QTextCharFormat()
        header_5_format.setForeground(QColor(200, 0, 244))  
        header_5_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression('^##### [^\n]*'), header_5_format, 'header5'))



        header_6_format = QTextCharFormat()
        header_6_format.setForeground(QColor(0, 244, 244))  
        header_6_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression('^###### [^\n]*'), header_6_format, 'header1'))

        italic_bold_format = QTextCharFormat()
        italic_bold_format.setForeground(QColor(255, 244, 144))  
        italic_bold_format.setFontItalic(True)
        italic_bold_format.setFontWeight(QFont.Weight.Bold)

        self.highlighting_rules.append((QRegularExpression(r'\*\*\*(.+?)\*\*\*'), italic_bold_format, 'italic_bold'))


        bold_format = QTextCharFormat()
        bold_format.setForeground(QColor(255, 1, 1))  
        bold_format.setFontWeight(QFont.Weight.Bold)

        self.highlighting_rules.append((QRegularExpression(r'\*\*(.*?)\*\*'), bold_format, 'bold_*'))
        self.highlighting_rules.append((QRegularExpression(r'__(.*?)__'), bold_format, 'bold_underscore'))

        italic_format = QTextCharFormat()
        italic_format.setForeground(QColor(0, 244, 144))  
        italic_format.setFontItalic(True)

        self.highlighting_rules.append((QRegularExpression(r'\*(.*?)\*'), italic_format, 'italic_format'))


        blockqotes_format = QTextCharFormat()
        blockqotes_format.setForeground(QColor(0, 244, 244))  
        blockqotes_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression('^> [^\n]*'), blockqotes_format, 'blockqotes_format'))


        number_format = QTextCharFormat()
        number_format.setForeground(QColor(250, 179, 135))

        self.highlighting_rules.append((QRegularExpression('^\\b\\d+\\.?\\d*\\b. '), number_format, 'number'))


        unordered_format = QTextCharFormat()
        unordered_format.setForeground(QColor(250, 179, 0))

        self.highlighting_rules.append((QRegularExpression(r'^- [^\n]*'), unordered_format, 'unordered_format'))
        self.highlighting_rules.append((QRegularExpression(r'^\+ [^\n]*'), unordered_format, 'unordered_format'))
        self.highlighting_rules.append((QRegularExpression(r'^\* [^\n]*'), unordered_format, 'unordered_format'))



        for bracket in ['(', ')', '[', ']', '{', '}']:
            bracket_format = QTextCharFormat()
            bracket_format.setForeground(QColor(243, 139, 168))
            escaped = QRegularExpression.escape(bracket)
            bracket_regex = QRegularExpression(escaped)
            self.highlighting_rules.append((bracket_regex, bracket_format, 'bracket'))

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