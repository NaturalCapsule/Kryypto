from configparser import ConfigParser


# config = configparser.ConfigParser()




config = ConfigParser()
config.read('config/configuration.cfg')

# config['Settings']['database_host'] = 'new_host.com'
# config['Settings']['user'] = 'admin_user'

# with open('config/configuration.ini', 'w') as configfile:
#     config.write(configfile)

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
    # return config.get('Python', 'class')
    con = config.get('Python', 'class')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_python_function():
    # return config.get('Python', 'function')
    con = config.get('Python', 'function')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_python_keyword():
    # return config.get('Python', 'keyword')
    con = config.get('Python', 'keyword')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

# def get_python_comment():
#     con = config.get('Python', 'comment')
#     r, g, b = con.split(',')
#     return int(r), int(g), int(b)

def get_python_argument():
    # return config.get('Python', 'argument')
    con = config.get('Python', 'argument')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_python_builtin():
    # return config.get('Python', 'buitin')
    con = config.get('Python', 'builtin')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

# def get_python_number():
#     # return config.get('Python', 'number')
#     con = config.get('Python', 'number')
#     r, g, b = con.split(',')
#     return int(r), int(g), int(b)

# def get_python_bracket():
#     # return config.get('Python', 'bracket')
#     con = config.get('Python', 'bracket')
#     r, g, b = con.split(',')
#     return int(r), int(g), int(b)

# def get_python_punctuation():
#     # return config.get('Python', 'punctuation')
#     con = config.get('Python', 'punctuation')
#     r, g, b = con.split(',')
#     return int(r), int(g), int(b)

# def get_python_string():
#     # return config.get('Python', 'string')
#     con = config.get('Python', 'string')
#     r, g, b = con.split(',')
#     return int(r), int(g), int(b)



def get_config_comment():
    # return config.get('Config', 'comment')
    con = config.get('Config', 'comment')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_config_number():
    # return config.get('Config', 'number')
    con = config.get('Config', 'number')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_config_string():
    # return config.get('Config', 'string')
    con = config.get('Config', 'string')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_config_section():
    # return config.get('Config', 'section')
    con = config.get('Config', 'section')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_config_option():
    # return config.get('Config', 'option')
    con = config.get('Config', 'option')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_config_bracket():
    # return config.get('Config', 'bracket')
    con = config.get('Config', 'bracket')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)


def get_json_string():
    # return config.get('Json', 'string')
    con = config.get('Json', 'string')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_json_comment():
    # return config.get('Json', 'comment')
    con = config.get('Json', 'comment')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)
    
def get_json_boolean():
    # return config.get('Json', 'boolean')
    con = config.get('Json', 'boolean')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)
    
def get_json_number():
    # return config.get('Json', 'number')
    con = config.get('Json', 'number')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_json_bracket():
    # return config.get('Json', 'bracket')
    con = config.get('Json', 'bracket')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_json_curlyBracket():
    # return config.get('Json', 'curlyBracket')
    con = config.get('Json', 'curlyBracket')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)


def get_css_string():
    # return config.get('Css', 'string')
    con = config.get('Css', 'string')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_css_comment():
    # return config.get('Css', 'comment')
    con = config.get('Css', 'comment')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_css_hexcolor():
    con = config.get('Css', 'hex-color')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)


def get_css_property():
    # return config.get('Css', 'property')
    con = config.get('Css', 'property')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_css_bracket():
    # return config.get('Css', 'bracket')
    con = config.get('Css', 'bracket')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_css_number():
    # return config.get('Css', 'number')
    con = config.get('Css', 'number')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_css_class():
    # return config.get('Css', 'class')
    con = config.get('Css', 'class')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_css_none():
    # return config.get('Css', 'none')
    con = config.get('Css', 'none')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)


# def get_markdown_string():
#     return config.get('MarkDown', 'string')


def get_markdown_comment():
    # return config.get('MarkDown', 'comment')
    con = config.get('MarkDown', 'comment')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)


def get_markdown_number():
    # return config.get('MarkDown', 'number')
    con = config.get('MarkDown', 'number')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)


def get_markdown_backtick():
    # return config.get('MarkDown', 'backtick')
    con = config.get('MarkDown', 'backtick')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_markdown_bracket():
    # return config.get('MarkDown', 'bracket')
    con = config.get('MarkDown', 'bracket')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_markdown_strikeThrough():
    # return config.get('MarkDown', 'strikeThrough')
    con = config.get('MarkDown', 'strikeThrough')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_markdown_equal():
    # return config.get('MarkDown', 'equal')
    con = config.get('MarkDown', 'equal')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)



def get_markdown_line():
    # return config.get('MarkDown', 'line')
    con = config.get('MarkDown', 'line')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)
    
def get_markdown_header1():
    # return config.get('MarkDown', 'header1')
    con = config.get('MarkDown', 'header1')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)


def get_markdown_header2():
    # return config.get('MarkDown', 'header2')
    con = config.get('MarkDown', 'header2')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)


def get_markdown_header3():
    con = config.get('MarkDown', 'header3')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_markdown_header4():
    # return config.get('MarkDown', 'header4')
    con = config.get('MarkDown', 'header4')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)


def get_markdown_header5():
    # return config.get('MarkDown', 'header5')
    con = config.get('MarkDown', 'header5')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_markdown_header6():
    # return config.get('MarkDown', 'header6')
    con = config.get('MarkDown', 'header6')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_markdown_italicBold():
    # return config.get('MarkDown', 'italicBold')
    con = config.get('MarkDown', 'italicBold')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)



def get_markdown_italic():
    # return config.get('MarkDown', 'italic')
    con = config.get('MarkDown', 'italic')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)

def get_markdown_bold():
    con = config.get('MarkDown', 'bold')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)
    
    # return config.get('MarkDown', 'bold')

def get_markdown_blockQotes():
    con = config.get('MarkDown', 'blockQotes')
    r, g, b = con.split(',')
    return int(r), int(g), int(b)


    # return config.get('MarkDown', 'blockQotes')

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

def write_fontSize(font_size):
    # config.write([''])
    config['Appearance']['FontSize'] = str(font_size)
    with open ('config/configuration.cfg', 'w', encoding = 'utf-8') as configfile:
        config.write(configfile)

def get_fontSize():
    return config.getint('Appearance', 'FontSize')