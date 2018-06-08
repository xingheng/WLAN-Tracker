import subprocess
from distutils.spawn import find_executable

from ..builtin import get_logger, F

logger = get_logger(__file__, F('.'))


def ping(hostname):
    try:
        executable = find_executable('ping')

        if executable is None:
            logger.error('command not found: ping!')
            return False, None, None

        cmd = executable + ' -c 1 -t 1 ' + hostname
        p = subprocess.Popen(['/bin/sh', '-c', cmd],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ret_code = p.wait()
        str_output = p.stdout.read()
        str_error = p.stderr.read()

        return ret_code == 0, str_output, str_error
    except Exception as e:
        logger.error(e)

    return False, None, None


def get_ip_from_ping_result(output):
    text = output.splitlines()[0]
    start = text.index("(")
    end = text.index(")")

    if start >= 0 and end >= 0 and end >= start:
        return text[start + 1:end]

    return None
