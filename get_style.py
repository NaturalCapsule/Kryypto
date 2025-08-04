from config import get_stylefile


def get_css_style():
    try:
        with open(get_stylefile()) as f:
            return f.read()

    except FileNotFoundError:
        with open('config/style.css') as f:
            return f.read()
