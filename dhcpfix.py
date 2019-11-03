from __future__ import print_function
from sys import argv, stderr
from os import system, remove
from datetime import datetime
from shutil import move
import netifaces as net

"""
Should i have this parse based off dhcp or just every few seonds.... test performance
"""

def get_current_dhcp_lease_end(dhcpfile):
    with open(dhcpfile, 'r') as dhcpFile:
        lines = dhcpFile.getlines()
        del lines[0] # get rid of that first line
        blocks = list()
        currentblock = list()
        block = False
        for line in lines:
            line = line.strip()
            if '{' in line:
                currentblock = list()
                block = True
                continue

            if '}' in line:
                # process block here
                block = False
                blocks.append(currentblock)
                continue
            if block:
                currentblock.append(line)

        return process_blocks(blocks)
    

    


def process_blocks(blocks):
    most_recent_time = datetime.fromtimestamp(0)
    most_recent_time_index = -1
    for x in range(len(blocks)):
        for line in blocks[x]:
            if 'renew' in line:
                date_time = parse_time_from_block(line)
                if most_recent_time < date_time:
                    most_recent_time = date_time
                    most_recent_time_index = x
                
    block = blocks[most_recent_time_index]
    expire_time = None
    for line in block:
        if 'expire' in line:
            expire_time = parse_time_from_block(line)
            break

    return expire_time


def parse_time_from_block(line):
    arr = line.split(' ')
    year_split = arr[2].split('/')
    hour_split = arr[3].split(':')
    date_time = datetime(year=int(year_split[0]), month=int(year_split[1]), day=int(year_split[2]), hour=int(hour_split[0]), minute=int(hour_split[1]), second=int(hour_split[2]))
    return date_time

def modify_hosts(hostname, ipaddr):
    with open('/etc/hosts', 'r') as hostsFile:
        with open('/etc/hosts-new', 'w') as writeFile:
            for line in hostsFile:
                line = line.strip()
                if hostname in line:
                    if ipaddr in line:
                        hostsFile.close()
                        remove('/etc/hosts-new')
                        return
                    line_split = line.split(' ')
                    writeFile.write('{} {} {}\n'.format(ipaddr, line_split[1], line_split[2]))
                    system('wall Changing /etc/hosts ip addr from {} to {}'.format(line_split[0], ipaddr))
                else:
                    writeFile.write('{}\n'.format(line))

    move('/etc/hosts-new', '/etc/hosts')


def main():
    if len(argv) is not 3:
        print('Invalid args', file=stderr)
    else:
        interface = argv[1]
        hostname = argv[2]
        ip = net.ifaddresses(interface)[net.AF_INET][0]['addr']
        modify_hosts(hostname, ip)

if __name__ == '__main__':
    main()        
        
