from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt6.QtCore import QRegularExpression, QTimer
from config import *
import re

from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont

from collections import defaultdict
from pygments import lex
from pygments.lexers.html import HtmlLexer
from pygments.lexers import BashLexer, CssLexer
from pygments.lexers.configs import DockerLexer
from pygments.lexers.data import YamlLexer


import re

def is_valid_hex_color(hex_code):
    hex_pattern = re.compile(r'^#(?:[0-9a-fA-F]{3}){1,2}$')
    return bool(hex_pattern.match(hex_code))


def get_bash_elements(code):
    types_elements = defaultdict(list)
    tokens = lex(code, BashLexer())

    for token_type, value in tokens:
        if value.strip():
            types_elements[str(token_type)].append(value)

    return types_elements

def get_yaml_elements(code):
    types_elements = defaultdict(list)
    tokens = lex(code, YamlLexer())

    for token_type, value in tokens:
        if value.strip():
            if value == 'true' or value == 'false':
                token_type = 'Token.Boolean'

            elif value == 'null':
                token_type = 'Token.Null'

            elif value.isnumeric():
                token_type = 'Token.Number'

            else:
                try:
                    float(value)
                    token_type = 'Token.Number'
                except ValueError:
                    pass


            types_elements[str(token_type)].append(value)

    return types_elements

def get_docker_elements(code):
    types_elements = defaultdict(list)

    check = []

    tokens = lex(code, DockerLexer())

    for token_type, value in tokens:
        if value.strip():
            if value not in check:
                # if str(token_type) != 'Token.Comment':
                types_elements[str(token_type)].append(value)
            check.append(value)

    return types_elements

def get_css_elements(code):
    types_elements = defaultdict(list)

    check = []

    tokens = lex(code, CssLexer())

    for token_type, value in tokens:
        if value.strip():
            if value not in check:
                if str(token_type) == 'Token.Name.Class':
                    if (value.startswith('1') or value.startswith('2') or value.startswith('3') or value.startswith('4') or value.startswith('5') or value.startswith('6') or value.startswith('7') or value.startswith('8') or value.startswith('9') or value.startswith('0')):
                        token_type = 'Token.Literal.Number.Float'

                types_elements[str(token_type)].append(value)
            check.append(value)

    return types_elements

def get_html_elements(code):
    types_elements = defaultdict(list)

    check = []

    tokens = lex(code, HtmlLexer())

    for token_type, value in tokens:
        if value.strip():
            if value not in check:
                types_elements[str(token_type)].append(value)
            check.append(value)

    return types_elements

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
        self.function_args = set()


        r, g, b = get_comment()
        self.string_format = QTextCharFormat()
        r, g, b = get_string()
        self.string_format.setForeground(QColor(r, g, b))


        r, g, b = get_comment()

        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor(r, g, b))  


        self.string_pattern = QRegularExpression(
            r'''(?:(?:f|fr|r|b|br)?)"([^"\\]|\\.)*"|(?:(?:f|fr|r|b|br)?)'([^'\\]|\\.)*' '''
        )

        self.comment_pattern = QRegularExpression(r'#[^\n]*')


        self.func_args_format = QTextCharFormat()
        r, g, b = get_bracket()
        self.func_args_format.setForeground(QColor(r, g, b))

        self.unused_format = QTextCharFormat()
        r, g, b = get_python_unusedvarColor()
        self.unused_format.setForeground(QColor(r, g, b))


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


        keyword_format = QTextCharFormat()
        r, g, b = get_python_keyword()
        keyword_format.setForeground(QColor(r, g, b))


        string_format = QTextCharFormat()
        r, g, b = get_string()
        string_format.setForeground(QColor(r, g, b))



        self.highlighting_rules.append((
            QRegularExpression(r'''f"([^"\\]|\\.)*"'''),
            self.string_format,
            'f-string'
        ))

        self.highlighting_rules.append((
            QRegularExpression(r'''f'([^'\\]|\\.)*''' + r"'"),
            self.string_format,
            'f-string'
        ))

        self.highlighting_rules.append((
            QRegularExpression(r'''fr"([^"\\]|\\.)*"'''),
            self.string_format,
            'fr-string'
        ))

        self.highlighting_rules.append((
            QRegularExpression(r'''fr'([^'\\]|\\.)*''' + r"'"),
            self.string_format,
            'fr-string'
        ))

        self.highlighting_rules.append((
            QRegularExpression(r'''b"([^"\\]|\\.)*"'''),
            self.string_format,
            'b-string'
        ))

        self.highlighting_rules.append((
            QRegularExpression(r'''b'([^'\\]|\\.)*''' + r"'"),
            self.string_format,
            'b-string'
        ))

        # br-strings
        self.highlighting_rules.append((
            QRegularExpression(r'''br"([^"\\]|\\.)*"'''),
            self.string_format,
            'br-string'
        ))

        self.highlighting_rules.append((
            QRegularExpression(r'''br'([^'\\]|\\.)*''' + r"'"),
            self.string_format,
            'br-string'
        ))

        self.highlighting_rules.append((
            QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"'),
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
            self.func_args_format.setFontItalic(True)

        self.couting = 1



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
            self.setFormat(0, len(text), default_format)

            used_ranges = set()

        # triple_string_formats = [
        #     ('"""', QRegularExpression('"""')),
        #     ("'''", QRegularExpression("'''"))
        # ]

        # for quote, start_expression in triple_string_formats:
        #     if self.previousBlockState() != 1:
        #         start_match = start_expression.match(text)
        #         start_index = start_match.capturedStart() if start_match.hasMatch() else -1
        #     else:
        #         start_index = 0

        #     while start_index >= 0:
        #         # Look for the ending quote after the start
        #         end_match = start_expression.match(text, start_index + 3)

        #         if end_match.hasMatch():
        #             # ✅ Found closing quote on the same line
        #             length = end_match.capturedStart() - start_index + 3
        #             self.setCurrentBlockState(0)  # don't carry to next line
        #         else:
        #             # ❌ No closing quote on this line → multiline docstring
        #             self.setCurrentBlockState(1)
        #             length = len(text) - start_index

        #         string_format = QTextCharFormat()
        #         r, g, b = get_string()
        #         string_format.setForeground(QColor(r, g, b))

        #         self.setFormat(start_index, length, string_format)
        #         used_ranges.add((start_index, start_index + length))

        #         # Continue searching after this match
        #         next_match = start_expression.match(text, start_index + length)
        #         start_index = next_match.capturedStart() if next_match.hasMatch() else -1

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
                    length = len(text) - start_index
                    self.setCurrentBlockState(1)

                string_format = QTextCharFormat()
                r, g, b = get_string()
                string_format.setForeground(QColor(r, g, b))

                self.setFormat(start_index, length, string_format)
                used_ranges.add((start_index, start_index + length))

                if self.currentBlockState() == 0:
                    break

                next_match = start_expression.match(text, start_index + length)
                start_index = next_match.capturedStart() if next_match.hasMatch() else -1


            self.setCurrentBlockState(0)



            ### DOC STRING
            # start_expression = QRegularExpression('"""')
            # start_match = start_expression.match(text)

            # if self.previousBlockState() != 1:
            #     start_index = start_match.capturedStart() if start_match.hasMatch() else -1
            # else:
            #     start_index = 0

            # while start_index >= 0:
            #     end_expression = QRegularExpression('"""')
            #     end_match = end_expression.match(text, start_index + 3)

            #     if end_match.hasMatch():
            #         length = end_match.capturedStart() - start_index + end_match.capturedLength()
            #         self.setCurrentBlockState(0)
            #     else:
            #         self.setCurrentBlockState(1)
            #         length = len(text) - start_index

            #     string_format = QTextCharFormat()
            #     r, g, b = get_string()
            #     string_format.setForeground(QColor(r, g, b))
            #     self.setFormat(start_index, length, string_format)

            #     start_match = start_expression.match(text, start_index + length)
            #     start_index = start_match.capturedStart() if start_match.hasMatch() else -1


            # arg_match = QRegularExpression(r"\bdef\s+\w+\s*\(([^)]*)\)").match(text)
            # if arg_match.hasMatch():
            #     args_str = arg_match.captured(1)
            #     args_start = arg_match.capturedStart(1)



            #     for arg in args_str.split(','):
            #         arg_name = arg.strip().split('=')[0].strip()
            #         if arg_name:

            #             if is_overlapping(args_start, arg_match.capturedLength(1), used_ranges):
            #                 continue

            #             pos = text.find(arg_name, args_start)
            #             if pos != -1:
            #                 self.setFormat(pos, len(arg_name), self.arg_def_format)
            #                 used_ranges.add((pos, pos + len(arg_name)))



            try:
                for name, (pattern, type_name) in self._compiled_patterns.items():
                    it = pattern.globalMatch(text)
                    while it.hasNext():
                        match = it.next()

                        if is_overlapping(match.capturedStart(), match.capturedLength(), used_ranges):
                            continue

                        if type_name == 'class':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.c_instance_foramt)

                        elif type_name == 'function':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.function_calls_format)
                            
                        elif type_name == 'method':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.method_calls_format)
                        # elif type_name == 'attribute':
                            # self.setFormat(match.capturedStart(), match.capturedLength(), self.c_instance_foramt)
                        # elif type_name == 'variable':
                        #     self.setFormat(match.capturedStart(), match.capturedLength(), self.function_calls_format)
                        elif type_name == 'module':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.class_format)
                        elif type_name == 'import' or type_name == 'Fromimport':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.class_format)


                        elif type_name == 'args':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.func_args_format)

                        elif type_name == 'unused':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.unused_format)

                        used_ranges.add((match.capturedStart(), match.capturedStart() + match.capturedLength()))


            except RuntimeError:
                pass

            string_matches = []
            match_it = self.string_pattern.globalMatch(text)
            while match_it.hasNext():
                match = match_it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), self.string_format)
                string_matches.append((match.capturedStart(), match.capturedEnd()))

            # string_matches = []
            # match_it = self.string_pattern.globalMatch(text)
            # while match_it.hasNext():
            #     match = match_it.next()
            #     start, end = match.capturedStart(), match.capturedEnd()

            #     if any(u_start <= start < u_end for u_start, u_end in used_ranges):
            #         continue

            #     self.setFormat(start, match.capturedLength(), self.string_format)
            #     string_matches.append((start, end))


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


        # r, g, b = get_json_boolean()
        r, g, b = get_boolean()

        boolean = QTextCharFormat()
        boolean.setForeground(QColor(r, g, b))

        self.highlighting_rules.append((QRegularExpression('true'), boolean, 'bool'))
        self.highlighting_rules.append((QRegularExpression('false'), boolean, 'bool'))

        r, g, b = get_number()
        number_format = QTextCharFormat()
        number_format.setForeground(QColor(r, g, b))

        self.highlighting_rules.append((QRegularExpression('\\b\\d+\\.?\\d*\\b'), number_format, 'number'))

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
    def __init__(self,use_highlighter ,parent=None, code = None):
        super().__init__(parent)

        self.css_tags = [
            "a", "abbr", "address", "area", "article", "aside", "audio", "b", "base", "bdi", "bdo", "blockquote",
            "body", "br", "button", "canvas", "caption", "cite", "code", "col", "colgroup", "data", "datalist",
            "dd", "del", "details", "dfn", "dialog", "div", "dl", "dt", "em", "embed", "fieldset", "figcaption",
            "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "head", "header", "hr", "html",
            "i", "iframe", "img", "input", "ins", "kbd", "label", "legend", "li", "link", "main", "map", "mark",
            "meta", "meter", "nav", "noscript", "object", "ol", "optgroup", "option", "output", "p", "param",
            "picture", "pre", "progress", "q", "rp", "rt", "ruby", "s", "samp", "script", "section", "select",
            "small", "source", "span", "strong", "style", "sub", "summary", "sup", "table", "tbody", "td",
            "template", "textarea", "tfoot", "th", "thead", "time", "title", "tr", "track", "u", "ul", "var",
            "video", "wbr"
        ]



        self.code = code
        
        self.useit = use_highlighter

        if self.useit:
            self.highlighting_rules = []
            self.setup_highlighting_rules()

        else:
            pass


    def setup_highlighting_rules(self):
        r, g, b = get_string()
        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor(r, g, b))
        self.highlighting_rules.append((QRegularExpression('"[^"\\\\]*(\\\\.[^"\\\\]*)*"'), self.string_format, 'string'))
        # self.highlighting_rules.append((QRegularExpression(r'''(?:(?:f|fr|r|b|br)?)"([^"\\]|\\.)*"|(?:(?:f|fr|r|b|br)?)'([^'\\]|\\.)*' ''', self.string_format, 'string'))

        self.string_pattern = QRegularExpression(
            r'''(?:(?:f|fr|r|b|br)?)"([^"\\]|\\.)*"|(?:(?:f|fr|r|b|br)?)'([^'\\]|\\.)*' '''
        )

        self.highlighting_rules.append((self.string_pattern, self.string_format, 'string'))



        r, g, b = get_comment()
        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor(r, g, b))

        r, g, b = get_number()
        self.number_format = QTextCharFormat()
        self.number_format.setForeground(QColor(r, g, b))

        self.highlighting_rules.append((QRegularExpression(r'\b\d+\.?\d*(px|em|rem|%|vh|vw|vmin|vmax|pt|cm|mm|in)?\b'), self.number_format, 'number'))


        r, g, b = get_punctuation()

        self.css_punctuation = QTextCharFormat()
        self.css_punctuation.setForeground(QColor(r, g, b))

        r, g, b = get_css_decorator()

        self.css_decorator = QTextCharFormat()
        self.css_decorator.setForeground(QColor(r, g, b))

        r, g, b = get_css_property()


        self.css_keyword = QTextCharFormat()
        self.css_keyword.setForeground(QColor(r, g, b))

        r, g, b = get_css_class()

        self.css_class = QTextCharFormat()
        self.css_class.setForeground(QColor(r, g, b))

        # r, g, b = get_html_attribute()
        r, g, b = get_css_property()


        self.css_attribute = QTextCharFormat()
        self.css_attribute.setForeground(QColor(r, g, b))

        r, g, b = get_css_tag()

        self.css_tag = QTextCharFormat()
        # self.css_tag.setForeground(QColor(r, g, b))
        self.css_tag.setForeground(QColor(r, g, b))


        self.hex_format = QTextCharFormat()

        for bracket in ['(', ')', '[', ']', '{', '}']:
            bracket_format = QTextCharFormat()
            r, g, b = get_bracket()
            bracket_format.setForeground(QColor(r, g, b))
            escaped = QRegularExpression.escape(bracket)
            bracket_regex = QRegularExpression(escaped)
            self.highlighting_rules.append((bracket_regex, bracket_format, 'bracket'))

        self.comment_pattern = QRegularExpression('/\*.*?\*/')


        self.string_pattern = QRegularExpression(r'"([^"\\]*(\\.[^"\\]*)*)"')
        self.var_pattern = QRegularExpression(r'\$[A-Za-z_][A-Za-z0-9_]*|\$\{[^}]+\}')


        if useItalic():
            self.comment_format.setFontItalic(True)


    def highlightBlock(self, text):
        def is_overlapping(start, length, used_ranges):
            end = start + length
            for begin, finish in used_ranges:
                if start < finish and end > begin:
                    return True
            return False

        used_ranges = set()
        elements = get_css_elements(text)


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

            string_ranges = []

            string_it = self.string_pattern.globalMatch(text)
            while string_it.hasNext():
                m = string_it.next()
                start = m.capturedStart()
                end = m.capturedEnd()
                self.setFormat(start, end - start, self.string_format)
                string_ranges.append((start, end))
                used_ranges.add((start, end))


            comment_it = self.comment_pattern.globalMatch(text)
            while comment_it.hasNext():
                m = comment_it.next()
                start = m.capturedStart()
                end = m.capturedEnd()

                in_string = any(s <= start < e for s, e in string_ranges)
                if in_string:
                    continue

                self.setFormat(start, end - start, self.comment_format)

            try:

                for token_type, words in elements.items():
                    if not words:
                        continue

                    pattern = r'\b(' + '|'.join(map(re.escape, words)) + r')\b'
                    if token_type == 'Token.Punctuation' or 'Token.Operator':
                        pattern = '(' + '|'.join(map(re.escape, words)) + ')'

                    regex = QRegularExpression(pattern)

                    it = regex.globalMatch(text)

                    while it.hasNext():
                        match = it.next()

                        if is_overlapping(match.capturedStart(), match.capturedLength(), used_ranges):
                            continue


                        if token_type == 'Token.Punctuation':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.css_punctuation)

                        elif token_type == 'Token.Literal.String.Single':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.string_format)


                        elif token_type == 'Token.Name.Tag':
                            for word in words:
                                if word not in self.css_tags:
                                    token_type = 'Token.Keyword'
                                    while ('1' in word or '2' in word or '3' in word or '4' in word or '5' in word or '6' in word or '7' in word or '8' in word or '9' in word or '0' in word) and word in words:

                                        token_type = 'Token.Literal.Number.Integer'
                                        words.remove(word)


                                    else:
                                        pattern = r'\b(' + '|'.join(map(re.escape, words)) + r')\b'

                                        regex = QRegularExpression(pattern)
                                        it = regex.globalMatch(text)

                                        while it.hasNext():
                                            match = it.next()


                                            self.setFormat(match.capturedStart(), match.capturedLength(), self.css_keyword)

                                else:
                                    self.setFormat(match.capturedStart(), match.capturedLength(), self.css_tag)


                        elif token_type == 'Token.Name.Decorator':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.css_decorator)

                        elif token_type == 'Token.Literal.Number.Integer' or token_type == 'Token.Literal.Number.Float' or token_type == 'Token.Operator' or token_type == 'Token.Keyword.Type':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.number_format)


                        elif token_type == 'Token.Keyword':
                            for word in words:
                                while ('1' in word or '2' in word or '3' in word or '4' in word or '5' in word or '6' in word or '7' in word or '8' in word or '9' in word or '0' in word) and word in words:
                                    token_type = 'Token.Literal.Number.Integer'
                                    words.remove(word)

                                else:
                                    pattern = r'\b(' + '|'.join(map(re.escape, words)) + r')\b'

                                    regex = QRegularExpression(pattern)
                                    it = regex.globalMatch(text)

                                    while it.hasNext():
                                        match = it.next()

                                        self.setFormat(match.capturedStart(), match.capturedLength(), self.css_keyword)


                        elif token_type == 'Token.Name.Class':
                            # for _ in range(len(words)):
                            #     for word in words:
                            #         while (word.startswith('1') or word.startswith('2') or word.startswith('3') or word.startswith('4') or word.startswith('5') or word.startswith('6') or word.startswith('7') or word.startswith('8') or word.startswith('9') or word.startswith('0')):
                            #             words.remove(word)
                            # print(words)

                            self.setFormat(match.capturedStart(), match.capturedLength(), self.css_class)

                        elif token_type == 'Token.Name.Namespace':
                            classes = []
                            for word in words:
                                if is_valid_hex_color(f"#{word}"):
                                    self.hex_format.setForeground(QColor(f"#{word}"))
                                    self.setFormat(match.capturedStart(), match.capturedLength(), self.hex_format)

                                else:
                                    classes.append(word)

                            else:
                                pattern = r'\b(' + '|'.join(map(re.escape, classes)) + r')\b'

                                regex = QRegularExpression(pattern)
                                it = regex.globalMatch(text)

                                while it.hasNext():
                                    match = it.next()

                                    self.setFormat(match.capturedStart(), match.capturedLength(), self.css_class)


                        used_ranges.add((match.capturedStart(), match.capturedStart() + match.capturedLength()))

            except Exception as e:
                print(e)


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



class BashSyntaxHighlighter(QSyntaxHighlighter):
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
        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor(r, g, b))
        self.highlighting_rules.append((QRegularExpression('"[^"\\\\]*(\\\\.[^"\\\\]*)*"'), self.string_format, 'string'))


        r, g, b = get_comment()
        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor(r, g, b))

        r, g, b = get_number()
        self.number_format = QTextCharFormat()
        self.number_format.setForeground(QColor(r, g, b))

        # r, g, b = get_bash_boolean()
        r, g, b = get_boolean()

        boolean = QTextCharFormat()
        boolean.setForeground(QColor(r, g, b))

        self.highlighting_rules.append((QRegularExpression('true'), boolean, 'bool'))
        self.highlighting_rules.append((QRegularExpression('false'), boolean, 'bool'))

        r, g, b = get_bash_keyword()

        self.bash_keyword = QTextCharFormat()
        self.bash_keyword.setForeground(QColor(r, g, b))

        self.bash_var = QTextCharFormat()
        self.bash_var.setForeground(QColor(255, 255, 255))

        r, g, b = get_bash_builtin()

        self.bash_builtin = QTextCharFormat()
        self.bash_builtin.setForeground(QColor(r, g, b))


        for bracket in ['(', ')', '[', ']', '{', '}']:
            bracket_format = QTextCharFormat()
            r, g, b = get_bracket()
            bracket_format.setForeground(QColor(r, g, b))
            escaped = QRegularExpression.escape(bracket)
            bracket_regex = QRegularExpression(escaped)
            self.highlighting_rules.append((bracket_regex, bracket_format, 'bracket'))

        self.comment_pattern = QRegularExpression('#[^\n]*')
        self.string_pattern = QRegularExpression(r'"([^"\\]*(\\.[^"\\]*)*)"')
        self.var_pattern = QRegularExpression(r'\$[A-Za-z_][A-Za-z0-9_]*|\$\{[^}]+\}')
        self.number_pattern = QRegularExpression('\\b\\d+\\.?\\d*\\b')

        if useItalic():
            self.comment_format.setFontItalic(True)
            self.bash_builtin.setFontItalic(True)
            self.bash_keyword.setFontItalic(True)


    def highlightBlock(self, text):
        def is_overlapping(start, length, used_ranges):
            end = start + length
            for begin, finish in used_ranges:
                if start < finish and end > begin:
                    return True
            return False

        used_ranges = set()
        elements = get_bash_elements(text)


        for pattern, fmt, name in self.highlighting_rules:
            matches = pattern.globalMatch(text)
            while matches.hasNext():
                match = matches.next()

                start = match.capturedStart()
                length = match.capturedLength()

                if name == 'number':
                    print(match.captured(0))

                if is_overlapping(start, length, used_ranges):
                    continue

                self.setFormat(start, length, fmt)
                used_ranges.add((start, start + length))

            string_ranges = []

            string_it = self.string_pattern.globalMatch(text)
            while string_it.hasNext():
                m = string_it.next()
                start = m.capturedStart()
                end = m.capturedEnd()
                self.setFormat(start, end - start, self.string_format)
                string_ranges.append((start, end))
                used_ranges.add((start, end))

                string_text = text[start:end]
                var_it = self.var_pattern.globalMatch(string_text)
                while var_it.hasNext():
                    v = var_it.next()
                    v_start = start + v.capturedStart()
                    v_end = v_start + v.capturedLength()
                    self.setFormat(v_start, v_end - v_start, self.bash_var)
                    used_ranges.add((v_start, v_end))

            number_it = self.number_pattern.globalMatch(text)
            while number_it.hasNext():
                m = number_it.next()
                start = m.capturedStart()
                end = m.capturedEnd()
                if is_overlapping(start, end - start, used_ranges):
                    continue
                self.setFormat(start, end - start, self.number_format)
                used_ranges.add((start, end))

            comment_it = self.comment_pattern.globalMatch(text)
            while comment_it.hasNext():
                m = comment_it.next()
                start = m.capturedStart()
                end = m.capturedEnd()

                in_string = any(s <= start < e for s, e in string_ranges)
                if in_string:
                    continue

                self.setFormat(start, end - start, self.comment_format)

            try:

                for token_type, words in elements.items():
                    if not words:
                        continue

                    pattern = r'\b(' + '|'.join(map(re.escape, words)) + r')\b'
                    regex = QRegularExpression(pattern)

                    it = regex.globalMatch(text)

                    while it.hasNext():
                        match = it.next()

                        if is_overlapping(match.capturedStart(), match.capturedLength(), used_ranges):
                            continue


                        if token_type == 'Token.Keyword':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.bash_keyword)

                        elif token_type == 'Token.Name.Builtin':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.bash_builtin)

                        used_ranges.add((match.capturedStart(), match.capturedStart() + match.capturedLength()))

            except Exception as e:
                print(e)


class TOMLSyntaxHighlighter(QSyntaxHighlighter):
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
        self.highlighting_rules.append((QRegularExpression('#[^\n]*'), comment_format, 'comment'))

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
        # self.highlighting_rules.append((QRegularExpression('\[[.*?\]]'), section_format, 'section'))


        self.highlighting_rules.append((QRegularExpression('""".*?"""', QRegularExpression.PatternOption.DotMatchesEverythingOption), string_format, 'multiline_string'))
        self.highlighting_rules.append((QRegularExpression("'''.*?'''", QRegularExpression.PatternOption.DotMatchesEverythingOption), string_format, 'multiline_string'))

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


class HTMLSyntaxHighlighter(QSyntaxHighlighter):
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
        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor(r, g, b))
        self.highlighting_rules.append((QRegularExpression('"[^"\\\\]*(\\\\.[^"\\\\]*)*"'), self.string_format, 'string'))


        r, g, b = get_comment()
        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor(r, g, b))

        r, g, b = get_number()
        self.number_format = QTextCharFormat()
        self.number_format.setForeground(QColor(r, g, b))

        r, g, b = get_punctuation()

        self.html_punctuation = QTextCharFormat()
        self.html_punctuation.setForeground(QColor(r, g, b))

        self.html_equal = QTextCharFormat()
        self.html_equal.setForeground(QColor(r, g, b))


        r, g, b = get_html_attribute()

        self.html_attribute = QTextCharFormat()
        self.html_attribute.setForeground(QColor(r, g, b))

        r, g, b = get_html_tag()

        self.html_tag = QTextCharFormat()
        self.html_tag.setForeground(QColor(r, g, b))

        for bracket in ['(', ')', '[', ']', '{', '}']:
            bracket_format = QTextCharFormat()
            r, g, b = get_bracket()
            bracket_format.setForeground(QColor(r, g, b))
            escaped = QRegularExpression.escape(bracket)
            bracket_regex = QRegularExpression(escaped)
            self.highlighting_rules.append((bracket_regex, bracket_format, 'bracket'))

        self.comment_pattern = QRegularExpression('<!--[^\n]*')
        self.string_pattern = QRegularExpression(r'"([^"\\]*(\\.[^"\\]*)*)"')
        self.var_pattern = QRegularExpression(r'\$[A-Za-z_][A-Za-z0-9_]*|\$\{[^}]+\}')
        self.number_pattern = QRegularExpression('\\b\\d+\\.?\\d*\\b')

        if useItalic():
            self.comment_format.setFontItalic(True)


    def highlightBlock(self, text):
        def is_overlapping(start, length, used_ranges):
            end = start + length
            for begin, finish in used_ranges:
                if start < finish and end > begin:
                    return True
            return False

        used_ranges = set()
        elements = get_html_elements(text)


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

            string_ranges = []

            string_it = self.string_pattern.globalMatch(text)
            while string_it.hasNext():
                m = string_it.next()
                start = m.capturedStart()
                end = m.capturedEnd()
                self.setFormat(start, end - start, self.string_format)
                string_ranges.append((start, end))
                used_ranges.add((start, end))

                # string_text = text[start:end]
                # var_it = self.var_pattern.globalMatch(string_text)
                # while var_it.hasNext():
                #     v = var_it.next()
                #     v_start = start + v.capturedStart()
                #     v_end = v_start + v.capturedLength()
                #     self.setFormat(v_start, v_end - v_start, self.bash_var)
                #     used_ranges.add((v_start, v_end))

            number_it = self.number_pattern.globalMatch(text)
            while number_it.hasNext():
                m = number_it.next()
                start = m.capturedStart()
                end = m.capturedEnd()
                if is_overlapping(start, end - start, used_ranges):
                    continue
                self.setFormat(start, end - start, self.number_format)
                used_ranges.add((start, end))

            comment_it = self.comment_pattern.globalMatch(text)
            while comment_it.hasNext():
                m = comment_it.next()
                start = m.capturedStart()
                end = m.capturedEnd()

                in_string = any(s <= start < e for s, e in string_ranges)
                if in_string:
                    continue

                self.setFormat(start, end - start, self.comment_format)

            try:

                for token_type, words in elements.items():
                    if not words:
                        continue

                    pattern = r'\b(' + '|'.join(map(re.escape, words)) + r')\b'
                    if token_type == 'Token.Punctuation' or 'Token.Operator':
                        pattern = '(' + '|'.join(map(re.escape, words)) + ')'

                    regex = QRegularExpression(pattern)

                    it = regex.globalMatch(text)

                    while it.hasNext():
                        match = it.next()

                        if is_overlapping(match.capturedStart(), match.capturedLength(), used_ranges):
                            continue


                        if token_type == 'Token.Punctuation':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.html_punctuation)

                        elif token_type == 'Token.Name.Tag':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.html_tag)

                        elif token_type == 'Token.Name.Attribute':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.html_attribute)

                        elif token_type == 'Token.Name.Operator':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.html_equal)

                        used_ranges.add((match.capturedStart(), match.capturedStart() + match.capturedLength()))

            except Exception as e:
                print(e)



class DockerSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self,use_highlighter ,parent=None, code = None):
        super().__init__(parent)

        self.code = code
        
        self.useit = use_highlighter

        if self.useit:
            self.highlighting_rules = []
            self.setup_highlighting_rules()

        else:
            pass


    def setup_highlighting_rules(self):
        r, g, b = get_string()
        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor(r, g, b))
        self.highlighting_rules.append((QRegularExpression('"[^"\\\\]*(\\\\.[^"\\\\]*)*"'), self.string_format, 'string'))
        # self.highlighting_rules.append((QRegularExpression(r'''(?:(?:f|fr|r|b|br)?)"([^"\\]|\\.)*"|(?:(?:f|fr|r|b|br)?)'([^'\\]|\\.)*' ''', self.string_format, 'string'))

        self.string_pattern = QRegularExpression(
            r'''(?:(?:f|fr|r|b|br)?)"([^"\\]|\\.)*"|(?:(?:f|fr|r|b|br)?)'([^'\\]|\\.)*' '''
        )

        self.highlighting_rules.append((self.string_pattern, self.string_format, 'string'))



        r, g, b = get_comment()
        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor(r, g, b))

        r, g, b = get_number()
        self.number_format = QTextCharFormat()
        self.number_format.setForeground(QColor(r, g, b))

        r, g, b = get_punctuation()

        self.docker_punctuation = QTextCharFormat()
        self.docker_punctuation.setForeground(QColor(r, g, b))

        r, g, b = get_docker_keyword()


        self.docker_keyword = QTextCharFormat()
        self.docker_keyword.setForeground(QColor(r, g, b))

        r, g, b = get_docker_builtin()


        self.docker_builtin = QTextCharFormat()
        self.docker_builtin.setForeground(QColor(r, g, b))



        for bracket in ['(', ')', '[', ']', '{', '}']:
            bracket_format = QTextCharFormat()
            r, g, b = get_bracket()
            bracket_format.setForeground(QColor(r, g, b))
            escaped = QRegularExpression.escape(bracket)
            bracket_regex = QRegularExpression(escaped)
            self.highlighting_rules.append((bracket_regex, bracket_format, 'bracket'))

        self.comment_pattern = QRegularExpression(r'#[^\n]*')



        self.string_pattern = QRegularExpression(r'"([^"\\]*(\\.[^"\\]*)*)"')
        self.var_pattern = QRegularExpression(r'\$[A-Za-z_][A-Za-z0-9_]*|\$\{[^}]+\}')


        if useItalic():
            self.comment_format.setFontItalic(True)


    def highlightBlock(self, text):
        def is_overlapping(start, length, used_ranges):
            end = start + length
            for begin, finish in used_ranges:
                if start < finish and end > begin:
                    return True
            return False


        default_format = QTextCharFormat()
        default_format.setForeground(QColor("white"))
        self.setFormat(0, len(text), default_format)

        used_ranges = set()
        elements = get_docker_elements(text)


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

            string_ranges = []

            string_it = self.string_pattern.globalMatch(text)
            while string_it.hasNext():
                m = string_it.next()
                start = m.capturedStart()
                end = m.capturedEnd()
                self.setFormat(start, end - start, self.string_format)
                string_ranges.append((start, end))
                used_ranges.add((start, end))


            comment_it = self.comment_pattern.globalMatch(text)
            while comment_it.hasNext():
                m = comment_it.next()
                start = m.capturedStart()
                end = m.capturedEnd()

                in_string = any(s <= start < e for s, e in string_ranges)
                if in_string:
                    continue

                self.setFormat(start, end - start, self.comment_format)

            try:

                for token_type, words in elements.items():
                    if not words:
                        continue

                    pattern = r'\b(' + '|'.join(map(re.escape, words)) + r')\b'
                    if token_type == 'Token.Punctuation' or 'Token.Operator':
                        pattern = '(' + '|'.join(map(re.escape, words)) + ')'

                    regex = QRegularExpression(pattern)

                    it = regex.globalMatch(text)

                    while it.hasNext():
                        match = it.next()

                        if is_overlapping(match.capturedStart(), match.capturedLength(), used_ranges):
                            continue


                        if token_type == 'Token.Punctuation':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.docker_punctuation)

                        elif token_type == 'Token.Literal.String.Single':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.string_format)


                        elif token_type == 'Token.Keyword':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.docker_keyword)

                        elif token_type == 'Token.Operator' or token_type == 'Token.Keyword.Type':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.number_format)

                        elif token_type == 'Token.Name.Builtin':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.docker_builtin)

                        elif token_type == 'Token.Comment':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.comment_format)

                        else:
                            self.setFormat(match.capturedStart(), match.capturedLength(), default_format)


                        used_ranges.add((match.capturedStart(), match.capturedStart() + match.capturedLength()))

            except Exception as e:
                print(e)


class YamlSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self,use_highlighter ,parent=None, code = None):
        super().__init__(parent)

        self.code = code
        
        self.useit = use_highlighter

        if self.useit:
            self.highlighting_rules = []
            self.setup_highlighting_rules()

        else:
            pass


    def setup_highlighting_rules(self):
        r, g, b = get_string()
        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor(r, g, b))
        self.highlighting_rules.append((QRegularExpression('"[^"\\\\]*(\\\\.[^"\\\\]*)*"'), self.string_format, 'string'))
        # self.highlighting_rules.append((QRegularExpression(r'''(?:(?:f|fr|r|b|br)?)"([^"\\]|\\.)*"|(?:(?:f|fr|r|b|br)?)'([^'\\]|\\.)*' ''', self.string_format, 'string'))


        r, g, b = get_comment()
        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor(r, g, b))

        r, g, b = get_number()
        self.number_format = QTextCharFormat()
        self.number_format.setForeground(QColor(r, g, b))


        r, g, b = get_boolean()
        self.boolean = QTextCharFormat()
        self.boolean.setForeground(QColor(r, g, b))

        # self.highlighting_rules.append((QRegularExpression('true'), boolean, 'bool'))
        # self.highlighting_rules.append((QRegularExpression('false'), boolean, 'bool'))
        r, g, b = get_punctuation()

        self.yaml_punctuation = QTextCharFormat()
        self.yaml_punctuation.setForeground(QColor(r, g, b))
        r, g, b = get_yaml_null()

        self.yaml_null = QTextCharFormat()
        self.yaml_null.setForeground(QColor(r, g, b))

        r, g, b = get_yaml_types()

        self.yaml_types = QTextCharFormat()
        self.yaml_types.setForeground(QColor(r, g, b))

        r, g, b = get_yaml_items()

        self.yaml_items = QTextCharFormat()
        self.yaml_items.setForeground(QColor(r, g, b))


        for bracket in ['(', ')', '[', ']', '{', '}']:
            bracket_format = QTextCharFormat()
            r, g, b = get_bracket()
            bracket_format.setForeground(QColor(r, g, b))
            escaped = QRegularExpression.escape(bracket)
            bracket_regex = QRegularExpression(escaped)
            self.highlighting_rules.append((bracket_regex, bracket_format, 'bracket'))

        self.comment_pattern = QRegularExpression(r'#[^\n]*')



        self.string_pattern = QRegularExpression(r'"([^"\\]*(\\.[^"\\]*)*)"')
        self.var_pattern = QRegularExpression(r'\$[A-Za-z_][A-Za-z0-9_]*|\$\{[^}]+\}')


        if useItalic():
            self.comment_format.setFontItalic(True)


    def highlightBlock(self, text):
        def is_overlapping(start, length, used_ranges):
            end = start + length
            for begin, finish in used_ranges:
                if start < finish and end > begin:
                    return True
            return False


        default_format = QTextCharFormat()
        default_format.setForeground(QColor("white"))
        self.setFormat(0, len(text), default_format)

        used_ranges = set()
        elements = get_yaml_elements(text)


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

            string_ranges = []

            string_it = self.string_pattern.globalMatch(text)
            while string_it.hasNext():
                m = string_it.next()
                start = m.capturedStart()
                end = m.capturedEnd()
                self.setFormat(start, end - start, self.string_format)
                string_ranges.append((start, end))
                used_ranges.add((start, end))


            comment_it = self.comment_pattern.globalMatch(text)
            while comment_it.hasNext():
                m = comment_it.next()
                start = m.capturedStart()
                end = m.capturedEnd()

                in_string = any(s <= start < e for s, e in string_ranges)
                if in_string:
                    continue

                self.setFormat(start, end - start, self.comment_format)

            try:

                for token_type, words in elements.items():
                    if not words:
                        continue

                    pattern = r'\b(' + '|'.join(map(re.escape, words)) + r')\b'
                    if token_type == 'Token.Punctuation' or 'Token.Operator':
                        pattern = '(' + '|'.join(map(re.escape, words)) + ')'

                    regex = QRegularExpression(pattern)

                    it = regex.globalMatch(text)

                    while it.hasNext():
                        match = it.next()

                        if is_overlapping(match.capturedStart(), match.capturedLength(), used_ranges):
                            continue


                        if token_type == 'Token.Punctuation':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.yaml_punctuation)

                        elif token_type == 'Token.Literal.String' or token_type == 'Token.Literal.Scalar.Plain':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.string_format)


                        elif token_type == 'Token.Operator' or token_type == 'Token.Number':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.number_format)

                        elif token_type == 'Token.Keyword.Type':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.yaml_types)


                        elif token_type == 'Token.Comment':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.comment_format)

                        elif token_type == 'Token.Name.Tag' or token_type == 'Token.Name.Variable':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.yaml_items)

                        elif token_type == 'Token.Boolean':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.boolean)

                        elif token_type == 'Token.Null':
                            self.setFormat(match.capturedStart(), match.capturedLength(), self.yaml_null)


                        else:
                            self.setFormat(match.capturedStart(), match.capturedLength(), default_format)


                        used_ranges.add((match.capturedStart(), match.capturedStart() + match.capturedLength()))

            except Exception as e:
                print(e)