# -*- coding: utf-8 -*-
#!/usr/bin/python
##-------------------------------------------------------------------
## File : queryhost.py
## Description :
## --
## Created : <2017-01-01>
## Updated: Time-stamp: <2017-07-12 11:35:30>
##-------------------------------------------------------------------
import sys

# ssh actions
import paramiko

# parse json output
import json

def ssh_queryhost(arg_list):
    [server, username, ssh_port, ssh_key_file, key_passphrase, role, pid_file, log_file] = arg_list
    try:
        # https://raw.githubusercontent.com/DennyZhang/devops_public/tag_v6/python/node_usage/node_usage.py
        ssh_command = "python /usr/sbin/node_usage.py"
        if pid_file is not None:
            ssh_command = "%s --pid_file %s" % (ssh_command, pid_file)
        if log_file is not None:
            ssh_command = "%s --log_file %s" % (ssh_command, log_file)
        
        info_dict = ssh_query_node(server, username, ssh_port, ssh_key_file, key_passphrase, ssh_command)
        summary = "[Summary] Host: %s(%s)" % (info_dict['hostname'], info_dict['ipaddress_eth0'])
        if role is not None:
            summary = "%s Role(%s)" % (summary, role)
            
        details = get_node_detail(info_dict)
        return (summary, details)
    except:
        details = "Unexpected on server: %s error: %s" % (server, sys.exc_info()[0])
        return ("Error", details)

def get_host_ip(host_query_string, hostname_ip_dict):
    host_ip = ""
    err_msg = ""
    if host_query_string in hostname_ip_dict:
        host_ip = hostname_ip_dict[host_query_string]
    else:
        matched_ip_list = []
        matched_hostname_list = []
        for hostname in hostname_ip_dict.keys():
            if host_query_string in hostname:
                matched_hostname_list.append(hostname)
                matched_ip_list.append(hostname_ip_dict[hostname])
        matched_count = len(matched_ip_list)
        if matched_count == 1:
            host_ip = matched_ip_list[0]
        else:
            if matched_count == 0:
                err_msg = "No matched hostnames. Current nodes are: %s" % \
                          ",".join(sorted(hostname_ip_dict.keys()))
            else:
                err_msg = "%d matched hostnames. Please choose one:\n%s" % \
                          (matched_count, "  \n".join(sorted(matched_hostname_list)))
    return (host_ip, hostname, err_msg)

################################################################################
# TODO: move to common library
def ssh_query_node(server, username, ssh_port, ssh_key_file, key_passphrase, ssh_command):
    import logging
    logging.getLogger("paramiko").setLevel(logging.WARNING)

    # print("Run ssh_command in %s: %s" % (server, ssh_command))
    output = ""
    info_dict = {}

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    key = paramiko.RSAKey.from_private_key_file(ssh_key_file, password=key_passphrase)
    ssh.connect(server, username=username, port=ssh_port, pkey=key)
    stdin, stdout, stderr = ssh.exec_command(ssh_command)
    output = "\n".join(stdout.readlines())
    ssh.close()
    # print("output: %s" % (output))
    info_dict = json.loads(output)
    return info_dict

def get_node_detail(info_dict):
    details = "RAM Usage: %s\nDisk Usage: %s\nCPU Load: %s\n" % \
              (info_dict['ram']['used_percentage'], info_dict['disk']['used_percentage'], \
               info_dict['cpu_load'])

    if "process_status" in info_dict:
        details = "%s\n%s" % (details, info_dict['process_status'])

    if "tail_log_file" in info_dict:
        details = "%s\n%s" % (details, info_dict['tail_log_file'])

    return details
##-------------------------------------------------------------------
## File : queryhost.py ends
