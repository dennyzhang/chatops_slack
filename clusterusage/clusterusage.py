# -*- coding: utf-8 -*-
#!/usr/bin/python
##-------------------------------------------------------------------
## File : clusterusage.py
## Description :
## --
## Created : <2017-01-01>
## Updated: Time-stamp: <2017-07-12 16:04:54>
##-------------------------------------------------------------------
# ssh actions
import sys
import paramiko

# parse json output
import json

# multiple threading for a list of ssh servers
import queue

import threading

def ssh_query_cluster_usage(arg_list):
    try:
        [server_list, role_dict, username, ssh_port, ssh_key_file, key_passphrase] = arg_list
        if server_list == []:
            return ("No matched servers", "Nothing to show")

        summary = ""
        details = ""
        sum_ram_used_gb = 0
        sum_ram_total_gb = 0
        sum_disk_used_gb = 0
        sum_total_disk_gb = 0
        info_list = ssh_query_node_list(server_list, username, ssh_port, ssh_key_file, key_passphrase)

        # Check error status
        for (server, info_dict, error) in info_list:
            if error is not None:
                return ("Error", error)

        server_dict = {}
        hostname_server_dict = {}
        # TODO: improve the output summary
        for (server, info_dict, status) in info_list:
            hostname = info_dict['hostname']
            hostname_server_dict[hostname] = server
            sum_disk_used_gb += float(info_dict['disk']['used_gb'])
            sum_total_disk_gb += float(info_dict['disk']['total_gb'])
            sum_ram_used_gb += float(info_dict['ram']['ram_used_gb'])
            sum_ram_total_gb += float(info_dict['ram']['ram_total_gb'])
            server_dict[server] = {'hostname': hostname, \
                                   'cpu_load': info_dict['cpu_load'],
                                   'ipaddress': info_dict['ipaddress_eth0'], \
                                   'disk_used_gb': info_dict['disk']['used_gb'], \
                                   'disk_total_gb': info_dict['disk']['total_gb'], \
                                   'ram_used_gb': info_dict['ram']['ram_used_gb'], \
                                   'ram_total_gb': info_dict['ram']['ram_total_gb'], \
                                   'ram_used_percentage': info_dict['ram']['used_percentage'], \
                                   'disk_used_percentage': info_dict['disk']['used_percentage']}
        ram_usage = "{:.2f}".format(float(sum_ram_used_gb) * 100/sum_ram_total_gb) + "%"
        disk_usage = "{:.2f}".format(float(sum_disk_used_gb) * 100/sum_total_disk_gb) + "%"
        summary = "Node count: %d. Total Usage. RAM: %s(%sgb/%sgb), Disk: %s(%sgb/%sgb).\n" \
                  % (len(info_list), ram_usage, "{:.2f}".format(sum_ram_used_gb), "{:.2f}".format(sum_ram_total_gb), \
                     disk_usage, "{:.2f}".format(sum_disk_used_gb), "{:.2f}".format(sum_total_disk_gb))

        # Get role summary
        for role in sorted(role_dict.keys()):
            sum_ram_used_gb = 0
            sum_ram_total_gb = 0
            sum_disk_used_gb = 0
            sum_total_disk_gb = 0
            server_list_by_role = role_dict[role]
            for server in server_list_by_role:
                sum_disk_used_gb += float(server_dict[server]['disk_used_gb'])
                sum_total_disk_gb += float(server_dict[server]['disk_total_gb'])
                sum_ram_used_gb += float(server_dict[server]['ram_used_gb'])
                sum_ram_total_gb += float(server_dict[server]['ram_total_gb'])
            ram_usage = "{:.2f}".format(float(sum_ram_used_gb) * 100/sum_ram_total_gb) + "%"
            disk_usage = "{:.2f}".format(float(sum_disk_used_gb) * 100/sum_total_disk_gb) + "%"
            summary = "%s\n        [%s] Node count: %d. RAM: %s(%sgb/%sgb), Disk: %s(%sgb/%sgb)." \
                      % (summary, role, len(server_list_by_role), ram_usage, \
                         "{:.2f}".format(sum_ram_used_gb), "{:.2f}".format(sum_ram_total_gb), \
                     disk_usage, "{:.2f}".format(sum_disk_used_gb), "{:.2f}".format(sum_total_disk_gb))

        # get the details, sorted by server
        details = ""
        for hostname in sorted(hostname_server_dict.keys()):
            server = hostname_server_dict[hostname]
            details = "%s\nHost: %s\nIP Address: %s.\nRAM Usage: %s.\nDisk Usage: %s.\nCPU load: %s.\n" \
                      % (details, server_dict[server]['hostname'], \
                         server_dict[server]['ipaddress'], \
                         server_dict[server]['ram_used_percentage'], \
                         server_dict[server]['disk_used_percentage'],
                         server_dict[server]['cpu_load'])
        return (summary, details)
    except Exception as e:
        return ("Error", e)

################################################################################
def ssh_query_node_list(server_list, username, ssh_port, ssh_key_file, key_passphrase):
    # TODO: handle with role_dict
    info_list = []
    q = queue.Queue()

    # run ssh test in a parallel way, to avoid timeout
    for server in server_list:
        t = threading.Thread(target=ssh_query_node_queue, \
                             args = (q, server, username, ssh_port, ssh_key_file, key_passphrase))
        t.daemon = True
        t.start()

    for x in range(0, len(server_list)):
        item = q.get()
        info_list.append(item)
    return info_list

def ssh_query_node_queue(q, server, username, ssh_port, ssh_key_file, key_passphrase):
    try:
        (server, info_dict, error) = ssh_query_node(server, username, ssh_port, ssh_key_file, key_passphrase)
        q.put((server, info_dict, error))
    except Exception as e:
        q.put((server, None, e))

# TODO: move to common library
def ssh_query_node(server, username, ssh_port, ssh_key_file, key_passphrase):
    import logging
    logging.getLogger("paramiko").setLevel(logging.WARNING)
    # https://raw.githubusercontent.com/DennyZhang/devops_public/tag_v5/python/node_usage/node_usage.py
    ssh_command = "python /usr/sbin/node_usage.py"
    output = ""
    info_dict = {}
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        key = paramiko.RSAKey.from_private_key_file(ssh_key_file, password=key_passphrase)
        ssh.connect(server, username=username, port=ssh_port, pkey=key)
        stdin, stdout, stderr = ssh.exec_command(ssh_command)
        output = "\n".join(stdout.readlines())
        ssh.close()
        info_dict = json.loads(output)
        return (server, info_dict, None)
    except:
        return (server, {}, "Unexpected on server: %s error: %s" % (server, sys.exc_info()[0]))
## File : clusterusage.py ends
