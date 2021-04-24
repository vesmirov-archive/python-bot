import sys
import io


def execute_python_code(code):
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
