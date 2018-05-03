#!/usr/bin/env python

import subprocess
import distutils.spawn

def ping(hostname):
    try:
        executable = distutils.spawn.find_executable('ping')

        if executable is None:
            print('ping is missing in the envionment paths!')
            return False, None, None

        cmd = executable + ' -c 1 -t 1 ' + hostname
        p = subprocess.Popen(['/bin/sh', '-c', cmd],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ret_code = p.wait()
        str_output = p.stdout.read()
        str_error = p.stderr.read()

        return ret_code == 0, str_output, str_error
    except Exception, e:
        print(e)

    return False, None, None


def get_ip_from_ping_result(output):
    text = output.splitlines()[0]
    start = text.index("(")
    end = text.index(")")

    if start >= 0 and end >= 0 and end >= start:
        return text[start + 1:end]

    return None


def arp(hostname):
    try:
        executable = distutils.spawn.find_executable('arp')

        if executable is None:
            print('arp is missing in the envionment paths!')
            return False, None, None

        cmd = executable + " -n " + hostname
        p = subprocess.Popen(['/bin/sh', '-c', cmd], stdout=subprocess.PIPE)

        if p.wait() == 0:
            output = p.stdout.read()

            # sample output:
            # 1) ? (10.128.2.33) at 10:40:f3:7e:e1:86 on en0 ifscope [ethernet]
            # 2) 10.128.2.33 (10.128.2.33) at 10:40:f3:7e:e1:86 on en0 ifscope [ethernet]
            # 3) 10.128.2.77 (10.128.2.77) -- no entry
            # 4) ? (10.128.2.77) -- no entry

            def substring(prefix, suffix):
                start = output.index(prefix)
                end = output.index(suffix)

                if start >= 0 and end >= 0 and end > start:
                    return output[start + len(prefix): end]

                return None

            ip = substring("(", ")")
            mac = substring("at ", " on")

            return True, ip, mac
    except Exception, e:
        print(e)

    return False, None, None
