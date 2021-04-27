import sys
import io
import subprocess


def execute_python_code(code):
    """Execute given code, save stdin and stdout in variable and return it"""
    out = io.StringIO()
    sys.stdout = out

    try:
        exec(code)
    except Exception as error:
        print(error)

    value = out.getvalue()
    if not value or value.isspace():
        return 'No output'
    return value
