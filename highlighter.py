from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt6.QtCore import QRegularExpression, Qt


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
            'while', 'with', 'yield', 'True', 'False', 'None'
        ]
        
        for keyword in keywords:
            pattern = QRegularExpression(f'\\b{keyword}\\b')
            self.highlighting_rules.append((pattern, keyword_format, None))

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
            self.highlighting_rules.append((pattern, builtin_format, None))

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
        function_format.setForeground(QColor(0, 0, 255))  # Blue
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
            bracket_format.setForeground(QColor(255, 255, 255))  # Red
            escaped = QRegularExpression.escape(bracket)
            bracket_regex = QRegularExpression(escaped)
            self.highlighting_rules.append((bracket_regex, bracket_format, 'bracket'))

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
        default_format = QTextCharFormat()
        default_format.setForeground(QColor("white"))
        default_format.setFontWeight(QFont.Weight.Bold)

        self.setFormat(0, len(text), default_format)

        used_ranges = set()

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(128, 128, 128))
        comment_format.setFontItalic(True)

        comment_regex = QRegularExpression('#[^\n]*')
        comment_matcher = comment_regex.globalMatch(text)

        while comment_matcher.hasNext():
            match = comment_matcher.next()
            start = match.capturedStart()
            length = match.capturedLength()
            self.setFormat(start, length, comment_format)
            used_ranges.add((start, start + length))

        for pattern, format, name in self.highlighting_rules:
            if name == 'comment':
                continue

            iterator = pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                start = match.capturedStart()
                length = match.capturedLength()

                if any(start < end and (start + length) > begin for (begin, end) in used_ranges):
                    continue

                self.setFormat(start, length, format)
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