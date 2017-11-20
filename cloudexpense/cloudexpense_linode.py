#!/usr/bin/python
##-------------------------------------------------------------------
## File : cloudexpense_linode.py
## Author : Denny <https://www.dennyzhang.com/contact>
## Description :
## --
## Created : <2017-05-22>
## Updated: Time-stamp: <2017-11-13 11:00:55>
##-------------------------------------------------------------------
# TODO: move to python common library
import os, sys, json
import requests
import subprocess
import re

def quit_if_empty(string, err_msg):
    if string is None or string == '':
        raise Exception("Error: string is null or empty. %s" % (err_msg))

def string_in_pattern(string, patterns):
    if patterns == '' or patterns is None:
        return False

    pattern_list = patterns.split(",")
    for pattern in pattern_list:
        if re.search(pattern, string) is not None:
            return True
    return False

################################################################################
def linode_get_price(cloud_token):
    url = "https://api.linode.com/?api_key=%s&api_action=avail.linodeplans" % (cloud_token)
    price_dict = {}
    r = requests.get(url)
    if r.status_code != 200:
        print("Error to call rest api. response: %s" % (r.text))
        sys.exit(1)
    response_json = r.json()
    for d in response_json['DATA']:
        price_dict[str(d['PLANID'])] = d['PRICE']
    return price_dict

def linode_get_ip(cloud_token):
    url = "https://api.linode.com/?api_key=%s&api_action=linode.ip.list" % (cloud_token)
    ip_dict = {}
    r = requests.get(url)
    if r.status_code != 200:
        print("Error to call rest api. response: %s" % (r.text))
        sys.exit(1)
    response_json = r.json()
    for d in response_json['DATA']:
        ip_dict[str(d['LINODEID'])] = d['IPADDRESS']
    return ip_dict

def linode_list_vm(cloud_token, skip_vm_patterns):
    price_map = linode_get_price(cloud_token)
    ip_map = linode_get_ip(cloud_token)
    url = "https://api.linode.com/?api_key=%s&api_action=linode.list" % (cloud_token)
    r = requests.get(url)
    if r.status_code != 200:
        print("Error to call rest api. response: %s" % (r.text))
        sys.exit(1)
    response_json = r.json()
    vm_list = []
    tmp_list = []
    total_price = 0
    for d in response_json['DATA']:
        if string_in_pattern(d["LABEL"], skip_vm_patterns):
            continue
        total_price += float(price_map[str(d["PLANID"])])
        tmp_list.append([str(d["LINODEID"]), d["LABEL"], \
                              ip_map[str(d["LINODEID"])], str(price_map[str(d["PLANID"])])])
    # sort by label
    tmp_list = sorted(tmp_list, key=lambda x: x[1])
    # generate output
    vm_list.append("{0:16} {1:25} {2:20} {3:10}".\
                   format('LINODEID', 'LABEL', 'IPADDRESS', 'Price'))

    for d in tmp_list:
        vm_list.append("{0:16} {1:25} {2:20} {3:10}".\
                       format(d[0], d[1], d[2], d[3]))
    return (total_price, vm_list)

# TODO: list linode volume and extra cost
################################################################################
## File : cloudexpense_linode.py ends
