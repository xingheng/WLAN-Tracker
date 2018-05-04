#!/usr/bin/env python

import os
import re
import subprocess
import tempfile
from distutils.spawn import find_executable
from sys import platform


def substring(source, prefix, suffix):
    start = source.index(prefix)
    end = source.index(suffix)

    if start >= 0 and end >= 0 and end > start:
        return source[start + len(prefix): end]

    return None


def ping(hostname):
    '''
    unused
    '''
    try:
        executable = find_executable('ping')

        if executable is None:
            print('command not found: ping!')
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
        executable = find_executable('nmap')

        if executable is None:
            print('command not found: nmap!')
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
        executable = find_executable('arp')

        if executable is None:
            print('command not found: arp!')
            return False, None, None

        cmd = executable + " -n " + hostname
        p = subprocess.Popen(['/bin/sh', '-c', cmd],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
        else:
            print p.stderr.read()
    except Exception, e:
        print(e)

    return False, None, None


def ip_neighbor(hostname):
    '''
    linux only
    '''
    try:
        executable = find_executable('ip')

        if executable is None:
            print('command not found: ip!')
            return False, None, None

        cmd = "%s neighbor show to %s" % (executable, hostname)
        p = subprocess.Popen(['/bin/sh', '-c', cmd],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if p.wait() == 0:
            output = p.stdout.read()

            if len(output) <= 0:
                return False, None, None

            # sample output:
            # 192.168.3.105 dev eth0 lladdr 00:e0:4c:68:1a:f9 STALE

            ip = re.search(
                r'((2[0-5]|1[0-9]|[0-9])?[0-9]\.){3}((2[0-5]|1[0-9]|[0-9])?[0-9])', output, re.I).group()
            mac = re.search(
                r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})', output, re.I).group()

            return True, ip, mac
        else:
            print p.stderr.read()
    except Exception, e:
        print(e)

    return False, None, None


def get_neighbor_address(hostname):
    is_linux = platform.startswith('linux')
    return ip_neighbor(hostname) if is_linux else arp(hostname)


def get_local_mac_addresses():
    '''
    Inspired from
    https://www.raspberrypi-spy.co.uk/2012/06/finding-the-mac-address-of-a-raspberry-pi/
    '''

    addresses = []

    try:
        for root, dirs, files in os.walk('/sys/class/net'):
            for dir in dirs:
                path = '/'.join((root, dir, 'address'))
                with open(path) as f:
                    addresses.append(f.read().strip())
    except Exception, e:
        print e

    return addresses


def _get_local_ip_addresses_linux():
    try:
        executable = find_executable('hostname')

        if executable is None:
            print('command not found: hostname!')
            return False, None, None

        cmd = executable + " --all-ip-addresses"
        p = subprocess.Popen(['/bin/sh', '-c', cmd],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if p.wait() == 0:
            output = p.stdout.read()
            return output.split(' ')
        else:
            print p.stderr.read()
    except Exception, e:
        print(e)

    return None


def _get_local_ip_addresses_macos():
    '''
    https://coderwall.com/p/pozgig/get-local-ip-address-on-os-x-from-terminal
    '''
    try:
        executable = find_executable('ifconfig')

        if executable is None:
            print('command not found: ifconfig!')
            return False, None, None

        cmd = executable + \
            " | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}'"
        p = subprocess.Popen(['/bin/sh', '-c', cmd],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if p.wait() == 0:
            output = p.stdout.read()
            return output.split(' ')
        else:
            print p.stderr.read()
    except Exception, e:
        print(e)

    return None


def get_local_ip_addresses():
    if platform.startswith('linux'):
        return _get_local_ip_addresses_linux()
    elif platform == 'darwin':
        return _get_local_ip_addresses_macos()
    else:
        assert("not implement!")

    return None
