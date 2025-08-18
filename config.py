from configparser import ConfigParser
import sys

config = ConfigParser()
config.read('config/configuration.cfg')


def get_comment():
    con = config.get('AllFormats', 'comment')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_number():
    con = config.get('AllFormats', 'number')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_punctuation():
    con = config.get('AllFormats', 'punctuation')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_bracket():
    con = config.get('AllFormats', 'bracket')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_string():
    con = config.get('AllFormats', 'string')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)


def get_python_class():
    con = config.get('Python', 'class')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_python_function():
    con = config.get('Python', 'function')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_python_method():
    con = config.get('Python', 'method')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_python_keyword():
    con = config.get('Python', 'keyword')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)


def get_python_argument():
    con = config.get('Python', 'argument')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_python_builtin():
    con = config.get('Python', 'builtin')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def set_advancedHighlighting():
    return config.getboolean('Python', "AdvancedSyntaxHighlighting")


def get_config_comment():
    con = config.get('Config', 'comment')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_config_number():
    con = config.get('Config', 'number')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_config_string():
    con = config.get('Config', 'string')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_config_section():
    con = config.get('Config', 'section')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_config_option():
    con = config.get('Config', 'option')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_config_bracket():
    con = config.get('Config', 'bracket')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)


def get_json_string():
    con = config.get('Json', 'string')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_json_comment():
    con = config.get('Json', 'comment')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)
    
def get_json_boolean():
    con = config.get('Json', 'boolean')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)
    
def get_json_number():
    con = config.get('Json', 'number')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_json_bracket():
    con = config.get('Json', 'bracket')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_json_curlyBracket():
    con = config.get('Json', 'curlyBracket')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)


def get_css_string():
    con = config.get('Css', 'string')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_css_comment():
    con = config.get('Css', 'comment')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_css_hexcolor():
    con = config.get('Css', 'hex-color')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)


def get_css_property():
    con = config.get('Css', 'property')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_css_bracket():
    con = config.get('Css', 'bracket')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_css_number():
    con = config.get('Css', 'number')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_css_class():
    con = config.get('Css', 'class')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_css_none():
    con = config.get('Css', 'none')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_markdown_comment():
    con = config.get('MarkDown', 'comment')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)


def get_markdown_number():
    con = config.get('MarkDown', 'number')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)


def get_markdown_backtick():
    con = config.get('MarkDown', 'backtick')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_markdown_bracket():
    con = config.get('MarkDown', 'bracket')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_markdown_strikeThrough():
    con = config.get('MarkDown', 'strikeThrough')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_markdown_equal():
    con = config.get('MarkDown', 'equal')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)



def get_markdown_line():
    con = config.get('MarkDown', 'line')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)
    
def get_markdown_header1():
    con = config.get('MarkDown', 'header1')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)


def get_markdown_header2():
    con = config.get('MarkDown', 'header2')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)


def get_markdown_header3():
    con = config.get('MarkDown', 'header3')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_markdown_header4():
    con = config.get('MarkDown', 'header4')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)


def get_markdown_header5():
    con = config.get('MarkDown', 'header5')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_markdown_header6():
    con = config.get('MarkDown', 'header6')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_markdown_italicBold():
    con = config.get('MarkDown', 'italicBold')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)



def get_markdown_italic():
    con = config.get('MarkDown', 'italic')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_markdown_bold():
    con = config.get('MarkDown', 'bold')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)
    

def get_markdown_blockQotes():
    con = config.get('MarkDown', 'blockQotes')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_markdown_unordered():
    con = config.get('MarkDown', 'unordered')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_markdown_bracket():
    con = config.get('MarkDown', 'bracket')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)


def get_fontFamily():
    return config.get('Appearance', 'FontFamily')

def write_config(value, section, option):
    config[section][option] = str(value)
    with open ('config/configuration.cfg', 'w', encoding = 'utf-8') as configfile:
        config.write(configfile)

def get_fontSize():
    return config.getint('Appearance', 'FontSize')

def get_openedDir():
    dir = config.get('Appearance', 'openedfolder')
    if dir:
        return dir
    else:
        return None

def get_stylefile():
    style_file = config.get('Appearance', 'StyleFile')
    if style_file:
        return style_file
    else:
        return 'config/style.css'

def useItalic():
    con = config.getboolean('AllFormats', 'Italic')
    if con:
        return con
    else:
        return False


def get_cursorColor():
    con = config.get('Cursor', 'Color')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)


def get_cursorWidth():
    return config.getint('Cursor', 'Width')

def newLine():
    return config.get('ShortCuts', 'new-line')


def DeleteLine():
    return config.get('ShortCuts', 'deleteCurrent-line')


def GotoBlock_():
    return config.get('ShortCuts', 'GotoBlock')


def IncreaseFont():
    return config.get('ShortCuts', 'IncreaseFont')


def DecreaseFont():
    return config.get('ShortCuts', 'DecreaseFont')


def IndentCurrentLine():
    return config.get('ShortCuts', 'IndentCurrent-line')


def removeIndentCurrent():
    return config.get('ShortCuts', 'removeIndentCurrent-line')


def MoveTabRight():
    return config.get('ShortCuts', 'MoveTabRight')


def MoveTabLeft():
    return config.get('ShortCuts', 'MoveTabLeft')


def RemoveCurrentTab():
    return config.get('ShortCuts', 'RemoveCurrentTab')

def Hide_Show_term():
    return config.get('ShortCuts', 'Hide-Show-Terminal')

def Hide_Show_viewer():
    return config.get('ShortCuts', 'Hide-Show-DirectoryViewer')

def Hide_Show_gitpanel():
    return config.get('ShortCuts', 'Hide-Show-GitPanel')

def KillTerminalSession():
    return config.get('ShortCuts', 'KillTerminalSession')

def RunCurrentPythonFile():
    return config.get('ShortCuts', 'RunCurrentPythonFile')

def OpenConfigFile():
    return config.get('ShortCuts', 'OpenConfigFile')


def OpenStyleFile():
    return config.get('ShortCuts', 'OpenStyleFile')

def Maximize():
    return config.get('ShortCuts', 'Maximize')

def SaveCurrentFile():
    return config.get('ShortCuts', 'SaveCurrentFile')

def SelectFolder():
    return config.get('ShortCuts', 'SelectFolder')

def Show_Hide_Shortcuts():
    return config.get('ShortCuts', 'Hide-Show-ShortCuts')

def Minimize():
    return config.get('ShortCuts', 'Minimize')

def Close():
    return config.get('ShortCuts', 'Close')

def Reboot():
    return config.get('ShortCuts', 'Reboot')

def setCustomTitleBar():
    return config.getboolean('Appearance', 'CustomTitleBar')

def get_cursorBlinkingRate():
    return config.getint('Cursor', 'BlinkingRate')

def showCompleter():
    return config.getboolean('Python', 'ShowCompleter')
    
def showDocstringpanel():
    return config.getboolean('Python', 'ShowDocStringPanel')

def getInterpreter():
    con = config.get('Python', 'pythoninterpreter')
    if con and con.lower() != 'none':

        return con
    else:
        return sys.executable