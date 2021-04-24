import sys
import io


def execute_python_code(code):
    out = io.StringIO()
    sys.stdout = out

    try:
        exec(code)
    except Exception as error:
        print(error)
    return out.getvalue()
