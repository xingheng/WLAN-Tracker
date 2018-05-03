#!/usr/bin/env python

import subprocess
import distutils.spawn
import tempfile


def substring(source, prefix, suffix):
    start = source.index(prefix)
    end = source.index(suffix)

    if start >= 0 and end >= 0 and end > start:
        return source[start + len(prefix): end]

    return None


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


def nmap(hostname):
    try:
        executable = distutils.spawn.find_executable('nmap')

        if executable is None:
            print('nmap is missing in the envionment paths!')
            return None

        temp_file = tempfile.NamedTemporaryFile('rw')

        cmd = '%s -sn %s -oG %s' % (executable, hostname, temp_file.name)
        p = subprocess.Popen(['/bin/sh', '-c', cmd],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ret_code = p.wait()

        if ret_code != 0:
            print p.stdout.read()
            print p.stderr.read()
            return None

        temp_file.seek(0)
        content = temp_file.read()

        # # Nmap 7.40 scan initiated Thu May  3 22: 45: 59 2018 as: / usr/local/bin/nmap - sn - oG / var/folders/dz/4w2fbhf95c58vt8mxr4y8gpr0000gr/T/tmp3gV4h9 192.168.31.1/24
        # Host: 192.168.31.1 (XiaoQiang)	Status: Up
        # Host: 192.168.31.41 ()	Status: Up
        # Host: 192.168.31.42 ()	Status: Up
        # Host: 192.168.31.57 ()	Status: Up
        # Host: 192.168.31.79 ()	Status: Up
        # Host: 192.168.31.133 ()	Status: Up
        # # Nmap done at Thu May  3 22:46:02 2018 -- 256 IP addresses (6 hosts up) scanned in 2.59 seconds

        ips = filter(lambda x: x.endswith('Status: Up'), content.splitlines())
        ips = map(lambda x: substring(x, "Host:", "(").strip(), ips)

        temp_file.close()
        return ips
    except Exception, e:
        print(e)

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

            ip = substring(output, "(", ")")
            mac = substring(output, "at ", " on")

            return True, ip, mac
    except Exception, e:
        print(e)

    return False, None, None
