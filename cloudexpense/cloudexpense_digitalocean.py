#!/usr/bin/python
##-------------------------------------------------------------------
## File : cloudexpense_digitalocean.py
## Author : Denny <denny@dennyzhang.com>
## Description :
## --
## Created : <2017-05-22>
## Updated: Time-stamp: <2017-07-11 21:55:44>
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
    pattern_list = patterns.split(",")
    for pattern in pattern_list:
        if re.search(pattern, string) is not None:
            return True
    return False

################################################################################
def digitalocean_list_vm(cloud_token, skip_vm_patterns, max_droplets_count = 500):
    # max_droplets_count: max fetched vm count
    url = 'https://api.digitalocean.com/v2/droplets?page=1&per_page=%s' \
                                                          % (max_droplets_count)
    headers = {'Content-Type': 'application/json', \
               'Authorization': "Bearer %s" % (cloud_token)}
    r = requests.get(url, headers = headers)
    if r.status_code != 200:
        print("Error to call rest api. response: %s" % (r.text))
        sys.exit(1)
    response_json = r.json()
    vm_list = []
    tmp_list = []
    total_price = 0
    for d in response_json['droplets']:
        if string_in_pattern(d["name"], skip_vm_patterns):
            continue
        total_price += float(d["size"]["price_monthly"])
        tmp_list.append([str(d["id"]), d["name"], d["networks"]["v4"][0]["ip_address"], \
                         str(d["size"]["price_monthly"])])
    # sort by hostname
    tmp_list = sorted(tmp_list, key=lambda x: x[1])
    # generate output
    vm_list.append("{0:16} {1:20} {2:20} {3:10}".\
                   format('ID', 'Name', 'IP', 'Price'))

    for d in tmp_list:
        vm_list.append("{0:16} {1:20} {2:20} {3:10}".\
                       format(d[0], d[1], d[2], d[3]))
    return (total_price, vm_list)

def digitalocean_list_volumes(cloud_token, skip_volumes_patterns):
    url = 'https://api.digitalocean.com/v2/volumes'
    headers = {'Content-Type': 'application/json', \
               'Authorization': "Bearer %s" % (cloud_token)}

    r = requests.get(url, headers = headers)
    if r.status_code != 200:
        print("Error to call rest api. response: %s" % (r.text))
        sys.exit(1)
    response_json = r.json()
    volume_list = []
    tmp_list = []
    total_price = 0
    for d in response_json['volumes']:
        if string_in_pattern(d["name"], skip_volumes_patterns):
            continue
        # 2017-05-09T17:59:03Z -> 2017-05-09
        created_at = d["created_at"][0:10]
        size_gigabytes = d["size_gigabytes"]
        # TODO: 10 GB -> $1
        price = int(size_gigabytes) * 0.1
        total_price += price
        tmp_list.append([d["name"], created_at, size_gigabytes, price])
    # sort by hostname
    tmp_list = sorted(tmp_list, key=lambda x: x[1])
    # generate output
    volume_list.append("{0:16} {1:25} {2:5} {3:10}".\
                   format('Name', 'Created At', 'GB', 'Price'))

    for d in tmp_list:
        volume_list.append("{0:16} {1:25} {2:5} {3:10}".\
                       format(d[0], d[1], d[2], d[3]))
    return (total_price, volume_list)
## File : cloudexpense_digitalocean.py ends
