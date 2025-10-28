## Could've made a helper function but whatever.
import configparser
import sys
import os
import platform

if platform.system() == "Windows":
    path = fr'C:\Users\{os.getlogin()}\AppData\Roaming\Kryypto\config\configuration.cfg'
elif platform.system() == 'Linux':
    # path = '~/.config/KryyptoConfig/config/configuration.cfg'
    path = os.path.expanduser('~/.config/KryyptoConfig/config/configuration.cfg')

config = configparser.ConfigParser()
config.read(path)


def write_config(value, section, option):
    config[section][option] = str(value)
    with open (path, 'w', encoding = 'utf-8') as configfile:
        config.write(configfile)

def get_comment():
    try:
        con = config.get('AllFormats', 'comment')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'AllFormat', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'AllFormats', 'comment')
        return 255, 255, 255

def get_boolean():
    try:
        con = config.get('AllFormats', 'boolean')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'AllFormat', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'AllFormats', 'boolean')
        return 255, 255, 255

def get_number():
    try:
        con = config.get('AllFormats', 'number')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'AllFormat', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'AllFormats', 'number')
        return 255, 255, 255

def get_punctuation():
    try:
        con = config.get('AllFormats', 'punctuation')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'AllFormat', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'AllFormats', 'punctuation')
        return 255, 255, 255

def get_bracket():
    try:
        con = config.get('AllFormats', 'bracket')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'AllFormat', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'AllFormats', 'bracket')
        return 255, 255, 255

def get_string():
    try:
        con = config.get('AllFormats', 'string')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Python', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'AllFormats', 'string')
        return 255, 255, 255



def get_python_class():
    try:
        con = config.get('Python', 'class')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Python', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'Python', 'class')
        return 255, 255, 255

def get_python_function():
    try:
        con = config.get('Python', 'function')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Python', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'Python', 'function')
        return 255, 255, 255


def get_python_method():
    try:
        con = config.get('Python', 'method')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Python', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'Python', 'method')
        return 255, 255, 255

def get_python_keyword():
    try:
        con = config.get('Python', 'keyword')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Python', 'temp')
        return 255, 255, 255        
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'Python', 'keyword')
        return 255, 255, 255


def get_python_argument():
    try:
        con = config.get('Python', 'argument')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Python', 'temp')
        return 255, 255, 255        
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'Python', 'argument')

def get_python_builtin():
    try:
        con = config.get('Python', 'builtin')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Python', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'Python', 'builtin')
        return 255, 255, 255

def get_python_unusedvarColor():
    try:
        con = config.get('Python', 'unusedvariable')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Python', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("128, 128, 128", 'Python', 'unusedvariable')
        return 128, 128, 128

def set_advancedHighlighting():
    try:
        return config.getboolean('Python', "AdvancedSyntaxHighlighting")
    except configparser.NoOptionError:
        write_config(bool('False'), 'Python', "AdvancedSyntaxHighlighting")
        return False


def get_config_comment():
    try:
        con = config.get('Config', 'comment')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Config', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'Config', 'comment')
        return 255, 255, 255

def get_config_number():
    try:
        con = config.get('Config', 'number')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Config', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'Config', 'number')
        return 255, 255, 255

def get_config_string():
    try:
        con = config.get('Config', 'string')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Config', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'Config', 'string')
        return 255, 255, 255

def get_config_section():
    try:
        con = config.get('Config', 'section')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Config', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'Config', 'section')
        return 255, 255, 255

def get_config_option():
    try:
        con = config.get('Config', 'option')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Config', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'Config', 'option')

def get_config_bracket():
    try:
        con = config.get('Config', 'bracket')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Config', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'Config', 'bracket')
        return 255, 255, 255


def get_json_string():
    try:
        con = config.get('Json', 'string')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Json', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'Json', 'string')

def get_json_comment():
    try:
        con = config.get('Json', 'comment')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Json', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'Json', 'comment')
        return 255, 255, 255

def get_json_boolean():
    try:
        con = config.get('Json', 'boolean')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Json', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'Json', 'boolean')
        return 255, 255, 255

def get_json_number():
    try:
        con = config.get('Json', 'number')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Json', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'Json', 'number')

def get_json_bracket():
    try:
        con = config.get('Json', 'bracket')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Json', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'Json', 'bracket')

def get_json_curlyBracket():
    try:
        con = config.get('Json', 'curlyBracket')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Json', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'Json', 'curlyBracket')
        return 255, 255, 255


# def get_css_hexcolor():
#     try:
#         con = config.get('Css', 'hex-color')
#         r, g, b = con.split(',')
#         return int(r), int(g), int(b)
#     except configparser.NoSectionError:
#         write_config('255, 255, 255', 'Css', 'temp')
#         return 255, 255, 255
#     except configparser.NoOptionError:
#         write_config("255, 255, 255", 'Css', 'hex-color')
#         return 255, 255, 255


def get_css_property():
    try:
        con = config.get('Css', 'property')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Css', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255")
        return 255, 255, 255

def get_css_tag():
    try:
        con = config.get('Css', 'tag')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Css', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'Css', 'tag')
        return 255, 255, 255

def get_css_decorator():
    try:
        con = config.get('Css', 'decorator')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Css', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'Css', 'decorator')
        return 255, 255, 255

def get_css_class():
    try:
        con = config.get('Css', 'class')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Css', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'Css', 'class')
        return 255, 255, 255

def get_markdownpreview_file():
    try:
        con = config.get('MarkDown', 'markdownpreview')
        if con:
            return con

    
        else:
            if platform.system() == 'Windows':
                write_config(fr'C:\Users\{os.getlogin()}\AppData\Roaming\Kryypto\config\markdown.css', 'MarkDown', 'markdownpreview')
                return fr'C:\Users\{os.getlogin()}\AppData\Roaming\Kryypto\config\markdown.css'
            elif platform.system() == "Linux":
                write_config(fr'~/.config/KryyptoConfig/config/markdown.css', 'MarkDown', 'markdownpreview')
                path = os.path.expanduser('~/.config/KryyptoConfig/config/markdown.css')
                return path


    except configparser.NoOptionError:
        if platform.system() == 'Windows':
            write_config(fr'C:\Users\{os.getlogin()}\AppData\Roaming\Kryypto\config\markdown.css', 'MarkDown', 'markdownpreview')
            return fr'C:\Users\{os.getlogin()}\AppData\Roaming\Kryypto\config\markdown.css'
        elif platform.system() == "Linux":
            write_config(fr'~/.config/KryyptoConfig/config/markdown.css', 'MarkDown', 'markdownpreview')
            path = os.path.expanduser('~/.config/KryyptoConfig/config/markdown.css')
            return path


def get_markdown_backtick():
    try:
        con = config.get('MarkDown', 'backtick')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'MarkDown', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'MarkDown', 'backtick')
        return 255, 255, 255

def get_markdown_bracket():
    try:
        con = config.get('MarkDown', 'bracket')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'MarkDown', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'MarkDown', 'bracket')
        return 255, 255, 255

def get_markdown_strikeThrough():
    try:
        con = config.get('MarkDown', 'strikeThrough')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'MarkDown', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'MarkDown', 'strikeThrough')
        return 255, 255, 255

def get_markdown_equal():
    try:
        con = config.get('MarkDown', 'equal')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'MarkDown', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'MarkDown', 'equal')
        return 255, 255, 255


def get_markdown_line():
    try:
        con = config.get('MarkDown', 'line')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'MarkDown', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'MarkDown', 'line')
        return 255, 255, 255

def get_markdown_header1():
    try:
        con = config.get('MarkDown', 'header1')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'MarkDown', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'MarkDown', 'header1')
        return 255, 255, 255

def get_markdown_header2():
    try:
        con = config.get('MarkDown', 'header2')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'MarkDown', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'MarkDown', 'header2')
        return 255, 255, 255

def get_markdown_header3():
    try:
        con = config.get('MarkDown', 'header3')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'MarkDown', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'MarkDown', 'header3')
        return 255, 255, 255


def get_markdown_header4():
    try:
        con = config.get('MarkDown', 'header4')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'MarkDown', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'MarkDown', 'header4')
        return 255, 255, 255


def get_markdown_header5():
    try:
        con = config.get('MarkDown', 'header5')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'MarkDown', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'MarkDown', 'header5')
        return 255, 255, 255

def get_markdown_header6():
    try:
        con = config.get('MarkDown', 'header6')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'MarkDown', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'MarkDown', 'header6')
        return 255, 255, 255

def get_markdown_italicBold():
    try:
        con = config.get('MarkDown', 'italicBold')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'MarkDown', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config('255, 255, 255', 'MarkDown', 'italicBold')
        return 255, 255, 255

def get_markdown_italic():
    try:
        con = config.get('MarkDown', 'italic')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'MarkDown', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config('255, 255, 255', 'MarkDown', 'italic')
        return 255, 255, 255

def get_markdown_bold():
    try:
        con = config.get('MarkDown', 'bold')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'MarkDown', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config('255, 255, 255', 'MarkDown', 'bold')
        return 255, 255, 255


def get_markdown_blockQotes():
    try:
        con = config.get('MarkDown', 'blockQotes')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'MarkDown', 'temp')
        return 255, 255, 255


    except configparser.NoOptionError:
        write_config('255, 255, 255', 'MarkDown', 'blockQotes')
        return 255, 255, 255

def get_markdown_unordered():
    try:
        con = config.get('MarkDown', 'unordered')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoOptionError:
        write_config('255, 255, 255', 'MarkDown', 'unordered')
        return 255, 255, 255

def get_markdown_bracket():
    try:
        con = config.get('MarkDown', 'bracket')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoOptionError:
        write_config('255, 255, 255', 'MarkDown', 'bracket')
        return 255, 255, 255

def get_bash_boolean():
    try:
        con = config.get('Bash', 'boolean')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Bash', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'Bash', 'boolean')
        return 255, 255, 255

def get_bash_keyword():
    try:
        con = config.get('Bash', 'keyword')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Bash', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'Bash', 'keyword')
        return 255, 255, 255

def get_bash_builtin():
    try:
        con = config.get('Bash', 'builtin')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Bash', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'Bash', 'builtin')
        return 255, 255, 255


def get_html_tag():
    try:
        con = config.get('Html', 'tag')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Html', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'Html', 'tag')
        return 255, 255, 255

def get_html_attribute():
    try:
        con = config.get('Html', 'attribute')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Html', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'Html', 'attribute')
        return 255, 255, 255


def get_docker_keyword():
    try:
        con = config.get('Docker', 'keyword')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Docker', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'Docker', 'keyword')
        return 255, 255, 255

def get_docker_builtin():
    try:
        con = config.get('Docker', 'builtin')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Docker', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'Docker', 'builtin')
        return 255, 255, 255

def get_yaml_items():
    try:
        con = config.get('Yaml', 'items')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Yaml', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'Yaml', 'items')
        return 255, 255, 255

def get_yaml_null():
    try:
        con = config.get('Yaml', 'null')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Yaml', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'Yaml', 'null')
        return 255, 255, 255

def get_yaml_types():
    try:
        con = config.get('Yaml', 'type')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoSectionError:
        write_config('255, 255, 255', 'Yaml', 'temp')
        return 255, 255, 255
    except configparser.NoOptionError:
        write_config("255, 255, 255", 'Yaml', 'type')
        return 255, 255, 255

def get_fontFamily():
    try:
        return config.get('Appearance', 'FontFamily')
    except configparser.NoOptionError:
        write_config('Segoe UI', 'Appearance', 'FontFamily')
        return 'Segoe UI'


def get_fontSize():
    try:
        return config.getint('Appearance', 'FontSize')
    except configparser.NoOptionError:
        write_config(12, 'Appearance', 'FontSize')
        return 12

def get_openedDir():
    try:
        dir = config.get('Appearance', 'openedfolder')
        if dir:
            return dir
        else:
            return None
    except configparser.NoOptionError:
        write_config('', 'Appearance', 'openedfolder')
        return None

def show_titleBar():
    try:
        return config.getboolean('Appearance', 'showtitlebar')
    except configparser.NoOptionError:
        write_config('True', 'Appearance', 'showtitlebar')
        return True

def get_stylefile():
    try:
        style_file = config.get('Appearance', 'StyleFile')
        if style_file:
            return style_file
        else:
            if platform.system() == 'Windows':
                write_config(fr'C:\Users\{os.getlogin()}\AppData\Roaming\Kryypto\config\style.css', 'Appearance', 'StyleFile')
                return fr'C:\Users\{os.getlogin()}\AppData\Roaming\Kryypto\config\style.css'
            elif platform.system() == "Linux":
                write_config(fr'~/.config/KryyptoConfig/config/style.css', 'Appearance', 'StyleFile')
                # return f'~/.config/KryyptoConfig/config/style.css'
                path = os.path.expanduser('~/.config/KryyptoConfig/config/style.css')
                return path


    except configparser.NoOptionError:
        # write_config(fr'C:\Users\{os.getlogin()}\AppData\Roaming\Kryypto\config\style.css', 'Appearance', 'StyleFile')
        # return fr'C:\Users\{os.getlogin()}\AppData\Roaming\Kryypto\config\style.css'
        if platform.system() == 'Windows':
            write_config(fr'C:\Users\{os.getlogin()}\AppData\Roaming\Kryypto\config\style.css', 'Appearance', 'StyleFile')
            return fr'C:\Users\{os.getlogin()}\AppData\Roaming\Kryypto\config\style.css'
        elif platform.system() == "Linux":
            write_config(fr'~/.config/KryyptoConfig/config/style.css', 'Appearance', 'StyleFile')
            # return fr'~/.config/KryyptoConfig/config/style.css'
            path = os.path.expanduser('~/.config/KryyptoConfig/config/style.css')
            return path



def useItalic():
    try:
        con = config.getboolean('AllFormats', 'Italic')
        if con:
            return con
        else:
            return False
    except configparser.NoOptionError:
        write_config('False', 'AllFormats', 'Italic')
        return False


def get_cursorColor():
    try:
        con = config.get('Cursor', 'Color')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoOptionError:
        write_config('255, 255, 255', 'Cursor', 'Color')
        return 255, 255, 255


def get_cursorWidth():
    try:
        return config.getint('Cursor', 'Width')
    except configparser.NoOptionError:
        write_config('3', 'Cursor', 'Width')
        return 3

def newLine():
    try:
        return config.get('ShortCuts', 'new-line')
    except configparser.NoOptionError:
        write_config('Ctrl+Return', 'ShortCuts', 'new-line')
        return 'Ctrl+Return'


def DeleteLine():
    try:
        return config.get('ShortCuts', 'deleteCurrent-line')
    except configparser.NoOptionError:
        write_config('Ctrl+Shift+K', 'ShortCuts', 'deleteCurrent-line')
        return 'Ctrl+Shift+K'


def GotoBlock_():
    try:
        return config.get('ShortCuts', 'GotoBlock')
    except configparser.NoOptionError:
        write_config('Ctrl+Shift+H', 'ShortCuts', 'GotoBlock')
        return 'Ctrl+Shift+H'


def IncreaseFont():
    try:
        return config.get('ShortCuts', 'IncreaseFont')
    except configparser.NoOptionError:
        write_config('Ctrl+=', 'ShortCuts', 'IncreaseFont')
        return 'Ctrl+='


def DecreaseFont():
    try:
        return config.get('ShortCuts', 'reducefont')
    except configparser.NoOptionError:
        write_config('Ctrl+-', 'ShortCuts', 'reducefont')
        return 'Ctrl+-'


def IndentCurrentLine():
    try:
        return config.get('ShortCuts', 'IndentCurrent-line')
    except configparser.NoOptionError:
        write_config('Ctrl+]', 'ShortCuts', 'IndentCurrent-line')
        return 'Ctrl+]'


def removeIndentCurrent():
    try:
        return config.get('ShortCuts', 'removeIndentCurrent-line')
    except configparser.NoOptionError:
        write_config('Ctrl+[', 'ShortCuts', 'removeIndentCurrent-line')
        return 'Ctrl+['


def MoveTabRight():
    try:
        return config.get('ShortCuts', 'MoveTabRight')
    except configparser.NoOptionError:
        write_config('Ctrl+Shift+T','ShortCuts', 'MoveTabRight')
        return 'Ctrl+Shift+T'


def MoveTabLeft():
    try:
        return config.get('ShortCuts', 'MoveTabLeft')
    except configparser.NoOptionError:
        write_config('Ctrl+Shift+E', 'ShortCuts', 'MoveTabLeft')
        return 'Ctrl+Shift+E'

def RemoveCurrentTab():
    try:
        return config.get('ShortCuts', 'RemoveCurrentTab')
    except configparser.NoOptionError:
        write_config('Ctrl+Shift+R', 'ShortCuts', 'RemoveCurrentTab')
        return 'Ctrl+Shift+R'


def Hide_Show_term():
    try:
        return config.get('ShortCuts', 'Hide-Show-Terminal')
    except configparser.NoOptionError:
        write_config('Ctrl+T', 'ShortCuts', 'Hide-Show-Terminal')
        return 'Ctrl+T'

def Hide_Show_viewer():
    try:
        return config.get('ShortCuts', 'Hide-Show-DirectoryViewer')
    except configparser.NoOptionError:
        write_config('Ctrl+B','ShortCuts', 'Hide-Show-DirectoryViewer')
        return 'Ctrl+B'

def Hide_Show_gitpanel():
    try:
        return config.get('ShortCuts', 'Hide-Show-GitPanel')
    except configparser.NoOptionError:
        write_config('Ctrl+G', 'ShortCuts', 'Hide-Show-GitPanel')
        return 'Ctrl+G'

def KillTerminalSession():
    try:
        return config.get('ShortCuts', 'KillTerminalSession')
    except configparser.NoOptionError:
        write_config('Ctrl+Shift+G', 'ShortCuts', 'KillTerminalSession')
        return 'Ctrl+Shift+G'

def RunCurrentPythonFile():
    try:
        return config.get('ShortCuts', 'RunCurrentPythonFile')
    except configparser.NoOptionError:
        write_config('Ctrl+N', 'ShortCuts', 'RunCurrentPythonFile')
        return 'Ctrl+N'

def OpenConfigFile():
    try:
        return config.get('ShortCuts', 'OpenConfigFile')
    except configparser.NoOptionError:
        write_config('Ctrl+Shift+O', 'ShortCuts', 'OpenConfigFile')
        return 'Ctrl+Shift+O'


def OpenStyleFile():
    try:
        return config.get('ShortCuts', 'OpenStyleFile')
    except configparser.NoOptionError:
        write_config('Ctrl+Shift+S', 'ShortCuts', 'OpenStyleFile')
        return 'Ctrl+Shift+S'

def OpenMarkDownFile():
    try:
        return config.get('ShortCuts', 'OpenMarkdownfile')
    except configparser.NoOptionError:
        write_config('Ctrl+Shift+M', 'ShortCuts', 'OpenMarkdownfile')
        return 'Ctrl+Shift+M'

def Maximize():
    try:
        return config.get('ShortCuts', 'Maximize')
    except configparser.NoOptionError:
        write_config('Ctrl+M', 'ShortCuts', 'Maximize')
        return 'Ctrl+M'

def SaveCurrentFile():
    try:
        return config.get('ShortCuts', 'SaveCurrentFile')
    except configparser.NoOptionError:
        write_config('Ctrl+S','ShortCuts', 'SaveCurrentFile' )
        return 'Ctrl+S'

def SelectFolder():
    try:
        return config.get('ShortCuts', 'SelectFolder')
    except configparser.NoOptionError:
        write_config('Ctrl+I', 'ShortCuts', 'SelectFolder')
        return 'Ctrl+I'

def Show_Hide_Shortcuts():
    try:
        return config.get('ShortCuts', 'Hide-Show-ShortCuts')
    except configparser.NoOptionError:
        write_config('Ctrl+L', 'ShortCuts', 'Hide-Show-ShortCuts')
        return 'Ctrl+L'


def MoveBlockDown():
    try:
        return config.get('ShortCuts', 'MoveBlockDown')
    except configparser.NoOptionError:
        write_config('Alt+Down', 'ShortCuts', 'MoveBlockDown')
        return 'Alt+Down'

def MoveBlockUp():
    try:
        return config.get('ShortCuts', 'MoveBlockUp')
    except configparser.NoOptionError:
        write_config('Alt+Up', 'ShortCuts', 'MoveBlockUp')
        return 'Alt+Up'

def bookmarkLine():
    try:
        return config.get('ShortCuts', 'bookmarkline')
    except configparser.NoOptionError:
        write_config('Ctrl+O', 'ShortCuts', 'bookmarkline')
        return 'Ctrl+O'


def removebookmarkedline():
    try:
        return config.get('ShortCuts', 'removebookmarkedline')
    except configparser.NoOptionError:
        write_config('Ctrl+E', 'ShortCuts', 'removebookmarkedline')
        return 'Ctrl+E'


def gotobookmarkedline():
    try:
        return config.get('ShortCuts', 'gotobookmarkedline')
    except configparser.NoOptionError:
        write_config('Ctrl+R', 'ShortCuts', 'gotobookmarkedline')
        return 'Ctrl+R'

def Minimize():
    try:
        return config.get('ShortCuts', 'Minimize')
    except configparser.NoOptionError:
        write_config("Ctrl+;", 'ShortCuts', 'Minimize')
        return 'Ctrl+;'

def Close():
    try:
        return config.get('ShortCuts', 'Close')
    except configparser.NoOptionError:
        write_config('Ctrl+P', 'ShortCuts', 'Close')
        return 'Ctrl+P'


def Reboot():
    try:
        return config.get('ShortCuts', 'Reboot')
    except configparser.NoOptionError:
        write_config('Ctrl+Shift+P', 'ShortCuts', 'Reboot')
        return 'Ctrl+Shift+P'

def setCustomTitleBar():
    try:
        return config.getboolean('Appearance', 'CustomTitleBar')
    except configparser.NoOptionError:
        write_config('False', 'Appearance', 'CustomTitleBar')
        return False

def get_cursorBlinkingRate():
    try:
        return config.getint('Cursor', 'BlinkingRate')
    except configparser.NoOptionError:
        write_config('300', 'Cursor', 'BlinkingRate')
        return 300


def get_docstring_size():
    try:
        con = config.getint('Dock', 'docstring-size')
        return con
    except configparser.NoOptionError:
        write_config('300', 'Dock', 'docstring-size')
        return 300

def get_terminal_size():
    try:
        con = config.getint('Dock', 'terminal-size')
        return con
    except configparser.NoOptionError:
        write_config('300', 'Dock', 'terminal-size')
        return 300

def get_git_size():
    try:
        con = config.getint('Dock', 'git-size')
        return con
    except configparser.NoOptionError:
        write_config('300', 'Dock', 'git-size')
        return 300

def get_directoryviewer_size():
    try:
        con = config.getint('Dock', 'directoryviewer-size')
        return con
    except configparser.NoOptionError:
        write_config('300', 'Dock', 'directoryviewer-size')
        return 300

def showCompleter():
    try:
        return config.getboolean('Python', 'ShowCompleter')
    except configparser.NoOptionError:
        write_config('False', 'Python', 'ShowCompleter')
        return False

def showDocstringpanel():
    try:
        return config.getboolean('Python', 'ShowDocStringPanel')
    except configparser.NoOptionError:
        write_config('False', 'Python', 'ShowDocStringPanel')
        return False


def is_frozen():
    return getattr(sys, "frozen", False)

def is_valid_python(path: str) -> bool:
    if platform.system() == 'Windows':
        return path and os.path.isfile(path) and path.lower().endswith("python.exe")
    elif platform.system() == 'Linux':
        return path and os.path.isfile(path) and path.lower().endswith("python")


def getInterpreter():
    try:
        con = config.get('Python', 'pythoninterpreter')
        con = fr"{con}"
        if is_valid_python(con):
            return con
        else:
            return None
    except configparser.NoOptionError:
        write_config('none', 'Python', 'pythoninterpreter')
        return None


def getDuration():
    try:
        return config.getint('Animation', 'duration')
    except configparser.NoOptionError:
        write_config('300', 'Animation', 'duration')
        return 300

def getType():
    try:
        return config.get('Animation', 'type')
    except configparser.NoOptionError:
        write_config('BezierSpline', 'Animation', 'type')
        return 'BezierSpline'


def get_IndentlineColor():
    try:
        con = config.get('Editor', 'IndentLineGuideColor')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoOptionError:
        write_config('255, 255, 255', 'Editor', 'IndentLineGuideColor')
        return 255, 255, 255

def showIndentLine():
    try:
        return config.getboolean('Editor', 'ShowIndentLineGuide')
    except configparser.NoOptionError:
        write_config('False', 'Editor', 'ShowIndentLineGuide')
        return False

def get_lineareacolor():
    try:
        con = config.get('Editor', 'LineNumberColorArea')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoOptionError:
        write_config('255, 255, 255', 'Editor', 'LineNumberColorArea')
        return 255, 255, 255


def get_linenumbercolor():
    try:
        con = config.get('Editor', 'LineNumberColor')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoOptionError:
        write_config('255, 255, 255', 'Editor', 'LineNumberColor')
        return 255, 255, 255
    
def get_activeLineColor():
    try:
        con = config.get('Editor', 'activteLineColor')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoOptionError:
        write_config('121, 192, 255', 'Editor', 'activteLineColor')
        return 121, 192, 255
    
def get_bookmarkedlineColor():
    try:
        con = config.get('Editor', 'bookmarkedlines')
        r, g, b = con.split(',')
        return int(r), int(g), int(b)
    except configparser.NoOptionError:
        write_config('255, 184, 77', 'Editor', 'bookmarkedlines')
        return 255, 184, 77