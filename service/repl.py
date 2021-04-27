import sys
import io
from subprocess import check_output, STDOUT, CalledProcessError


def execute_python_code(code):
    """
    Execute given python code,
    return stdin and stdout saved in variable
    """

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


def execute_bash_code(code):
    """
    Execute given bash code,
    return stdin and stdout saved in variable
    """

    try:
        output = check_output(code.split(), stderr=STDOUT)
    except CalledProcessError as exc:
        output = exc.output

    if not output or output.isspace():
        return 'No output'
    return output
