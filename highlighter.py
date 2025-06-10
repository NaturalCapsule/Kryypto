from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt6.QtCore import QRegularExpression
import ast

class PythonSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []
        self.setup_highlighting_rules()

    def setup_highlighting_rules(self):
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(85, 85, 255))  # Blue
        keyword_format.setFontWeight(QFont.Weight.Bold)


        keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'exec', 'finally', 'for',
            'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
            'not', 'or', 'pass', 'print', 'raise', 'return', 'try',
            'while', 'with', 'yield', 'True', 'False', 'None', 'Execption', 'SyntaxError', 'NameError', 'IndexError', 'AssertionError', 'AttributeError',
            'ZeroDivisionError', 'BaseException', 'TypeError', 'UnboundLocalError', 'ArithmeticError', 'FileNotFoundError', 'FileExistsError', 'FloatingPointError',
            'DeprecationWarning', 'ConnectionAbortedError', 'ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError', 'EOFError'
        ]
        
        for keyword in keywords:
            pattern = QRegularExpression(f'\\b{keyword}\\b')
            self.highlighting_rules.append((pattern, keyword_format, 'keywords'))

        builtin_format = QTextCharFormat()
        builtin_format.setForeground(QColor(170, 85, 0))  # Orange
        builtin_format.setFontWeight(QFont.Weight.Bold)
        
        builtins = [
            'abs', 'all', 'any', 'bin', 'bool', 'chr', 'dict', 'dir',
            'enumerate', 'filter', 'float', 'int', 'len', 'list', 'map',
            'max', 'min', 'open', 'print', 'range', 'str', 'sum', 'tuple',
            'type', 'zip'
        ]
        
        for builtin in builtins:
            pattern = QRegularExpression(f'\\b{builtin}\\b')
            self.highlighting_rules.append((pattern, builtin_format, 'builtins'))

        string_format = QTextCharFormat()
        string_format.setForeground(QColor(0, 128, 0))  # Green
        
        self.highlighting_rules.append((QRegularExpression('"[^"\\\\]*(\\\\.[^"\\\\]*)*"'), string_format, None))
        self.highlighting_rules.append((QRegularExpression("'[^'\\\\]*(\\\\.[^'\\\\]*)*'"), string_format, None))
        
        self.highlighting_rules.append((QRegularExpression('""".*"""'), string_format, 'string'))
        self.highlighting_rules.append((QRegularExpression("'''.*'''"), string_format, 'string'))

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(128, 128, 128))  # Gray
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression('#[^\n]*'), comment_format, 'comment'))

        number_format = QTextCharFormat()
        number_format.setForeground(QColor(255, 0, 255))  # Magenta
        self.highlighting_rules.append((QRegularExpression('\\b\\d+\\.?\\d*\\b'), number_format, 'number'))

        function_format = QTextCharFormat()
        function_format.setForeground(QColor(0, 255, 255))  # Blue
        function_format.setFontWeight(QFont.Weight.Bold)
        self.highlighting_rules.append((QRegularExpression('\\bdef\\s+(\\w+)'), function_format, 'function'))

        class_format = QTextCharFormat()
        class_format.setForeground(QColor(128, 0, 128))  # Purple
        class_format.setFontWeight(QFont.Weight.Bold)
        self.highlighting_rules.append((QRegularExpression('\\bclass\\s+(\\w+)'), class_format, 'class'))

        for punctuation in ['!', '@', '$', '%', '^', '&', '*', '-', '=', '+']:
            punction_format = QTextCharFormat()
            punction_format.setForeground(QColor(255, 0, 0))  # Red
            escaped = QRegularExpression.escape(punctuation)
            punction_regex = QRegularExpression(escaped)
            self.highlighting_rules.append((punction_regex, punction_format, 'punctuation'))

        for bracket in ['(', ')', '{', '}', '[', ']']:
            bracket_format = QTextCharFormat()
            bracket_format.setForeground(QColor(255, 0, 255))  # Red
            escaped = QRegularExpression.escape(bracket)
            bracket_regex = QRegularExpression(escaped)
            self.highlighting_rules.append((bracket_regex, bracket_format, 'bracket'))

        self.arg_def_format = QTextCharFormat()
        self.arg_def_format.setForeground(QColor("purple"))

        self.arg_usage_format = QTextCharFormat()
        self.arg_usage_format.setForeground(QColor("darkMagenta"))

        self.c_instance_foramt = QTextCharFormat()
        self.c_instance_foramt.setForeground(QColor('cyan'))

        self.function_calls_format = QTextCharFormat()
        self.function_calls_format.setForeground(QColor(0, 255, 255))

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

        self.c_instances = set()

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


    def highlight_class_instance(self, instances: str):
        try:
            for key, value in instances.items():
                if value == 'class':
                # self.c_instances = instances.keys()
                    self.c_instances.add(key)
        except Exception:
            self.c_instances.clear()

    def highlight_function_calls(self, calls):
        try:
            for key, value in calls.items():
                if value == 'function':
                # self.c_instances = instances.keys()
                    self.function_calls.add(key)
        except Exception:
            self.c_instances.clear()

    def highlightBlock(self, text):
        default_format = QTextCharFormat()
        default_format.setForeground(QColor("white"))
        default_format.setFontWeight(QFont.Weight.Bold)
        self.setFormat(0, len(text), default_format)

        used_ranges = set()

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(128, 128, 128))  # Gray
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

                if any(start < end and (start + length) > begin for (begin, end) in used_ranges):
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
            string_format.setForeground(QColor(0, 128, 0))  # Green
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
                    pos = text.find(arg_name, args_start)
                    if pos != -1:
                        self.setFormat(pos, len(arg_name), self.arg_def_format)
                        # used_ranges.add((pos, len(arg_name)))
                        used_ranges.add((match.capturedStart(), match.capturedLength()))


        for arg in self.function_args:
            pattern = QRegularExpression(fr"\b{arg}\b")
            it = pattern.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), self.arg_usage_format)
                used_ranges.add((match.capturedStart(), match.capturedStart() + match.capturedLength()))

        for instance in self.c_instances:
            pattern = QRegularExpression(fr"\b{instance}\b")
            it = pattern.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), self.c_instance_foramt)
                used_ranges.add((match.capturedStart(), match.capturedStart() + length))


        for call in self.function_calls:
            pattern = QRegularExpression(fr"\b{call}\b")
            it = pattern.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), self.function_calls_format)
                # used_ranges.add((match.capturedStart(), match.capturedStart() + length))
