#!/usr/bin/python
##-------------------------------------------------------------------
## File : chatops.py
## Author : Denny <denny@dennyzhang.com>
## Description :
## --
## Created : <2017-05-22>
## Updated: Time-stamp: <2017-07-12 14:36:29>
##-------------------------------------------------------------------
import sys, os
from flask import Flask, request, make_response
# get current function name
import inspect
# parse json output
import json
# slack actions
from slackclient import SlackClient

# slack delayed messages
import threading
import time

import logging
log_file = "/var/log/%s.log" % (os.path.basename(__file__).rstrip('\.py').rstrip('\.pyc'))
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())
############################################################
from config import *

# TODO: better way to include module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'utility')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'cloudexpense')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'queryhost')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'clusterusage')))

from slack_helper import verify_slack_token, verify_slack_username, response_content
from slack_helper import get_response_url, slack_send_delay_response

from cloudexpense import cloudexpense
from queryhost import ssh_queryhost, get_host_ip
from clusterusage import ssh_query_cluster_usage

################################################################################
application = Flask(__name__)

################################################################################
# TODO: use multi-threading instead of multi-processing
from multiprocessing import Process

import queue

slack_task_queue = queue.Queue()
num_worker_threads = 3

def worker():
    ## Read from the queue
    while True:
        # Read from the queue and do nothing
        item = slack_task_queue.get()
        print("reader get: item: %s" % (item))
        func_name = item[0]
        arg_list = item[1]
        func_name(arg_list)
        slack_task_queue.task_done()

threads = []
for i in range(num_worker_threads):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

################################################################################
@application.route("/chathelp", methods=['GET', 'HEAD'])
def help():
    print("queue: %s, Queue size: %d" % (slack_task_queue, slack_task_queue.qsize()))
    summary = "DevOps ChatOps via Slack Commands. All commands starts with /chat*"
    content_text = '''- /chatclusterusage: Overall resource usage, and summary by role.
- /chatcloudexpense: Show cloud bills across different cloud providers.
- /chatqueryhost [substring of hostname]: Query host without manual ssh.
- /chathelp: Current online help usage
'''
    return response_content(summary, content_text)

# Query monthly cost using DigitalOcean, Linode or Azure
@application.route("/chatcloudexpense", methods=['GET'])
def chatcloudexpense():
    try:
        verify_slack_token('GET', ALLOWED_TOKEN_LIST)
        verify_slack_username('GET', inspect.stack()[0][3], METHOD_ACL_USERLIST)

        response_url = get_response_url('GET')
        arg_list = [DIGITALOCEAN_TOKEN, LINODE_TOKEN, SKIP_VM_PATTERNS, SKIP_VOLUMES_PATTERNS]
        item = [slack_send_delay_response, [response_url, cloudexpense, arg_list]]
        slack_task_queue.put(item)
        print("queue: %s, Queue size: %d" % (slack_task_queue, slack_task_queue.qsize()))
        summary = "OK, got it"
        details = "On the way"
        return response_content(summary, details)
    except Exception as e:
        return response_content("Error!", e)

# Query host status
@application.route("/chatqueryhost", methods=['GET'])
def chatqueryhost():
    try:
        verify_slack_token('GET', ALLOWED_TOKEN_LIST)
        verify_slack_username('GET', inspect.stack()[0][3], METHOD_ACL_USERLIST)

        response_url = get_response_url('GET')
        host_query_string = request.args.get('text', '').strip()

        hostname_ip_dict = {}
        (server, hostname, err_msg) = get_host_ip(host_query_string, hostname_ip_dict)
        if err_msg != '':
            summary = "Ops. Fail to get what you need"
            details = err_msg
            return response_content(summary, details)
        else:
            (role, pid_file, log_file) = (None, None, None)
            
            username = "root"
            ssh_port = 2702

            arg_list = [server, username, ssh_port, SSH_KEY_FILE, KEY_PASSPHRASE, role, pid_file, log_file]
            item = [slack_send_delay_response, [response_url, ssh_queryhost, arg_list]]
            slack_task_queue.put(item)
            print("queue: %s, Queue size: %d" % (slack_task_queue, slack_task_queue.qsize()))
            summary = "OK, got it"
            details = "On the way"
            return response_content(summary, details)
    except Exception as e:
        return response_content("Error!", e)

# Current hardware resource usage, like Disk, RAM, CPU
@application.route("/chatclusterusage", methods=['GET'])
def chatclusterusage():
    try:
        verify_slack_token('GET', ALLOWED_TOKEN_LIST)
        verify_slack_username('GET', inspect.stack()[0][3], METHOD_ACL_USERLIST)

        (server_list, role_dict) = ([], {})
        username = "root"
        ssh_port = 2702
        response_url = get_response_url('GET')
        arg_list = [server_list, role_dict, username, ssh_port, SSH_KEY_FILE, KEY_PASSPHRASE]
        item = [slack_send_delay_response, [response_url, ssh_query_cluster_usage, arg_list]]
        slack_task_queue.put(item)
        print("queue: %s, Queue size: %d" % (slack_task_queue, slack_task_queue.qsize()))
        summary = "OK, got it"
        details = "On the way"
        return response_content(summary, details)
    except Exception as e:
        return response_content("Error!", e)

# List alerts of monitoring system
@application.route("/chatjavadebug", methods=['POST'])
def chatjavadebug():
    try:
        # TODO: get service name
        content = "TODO to be implemented"
        resp = make_response(content, 200)
        resp.headers['Content-type'] = 'application/json; charset=utf-8'
        return resp
    except Exception as e:
        return response_content("Error!", e)

# List alerts of monitoring system
@application.route("/chatproductionalerts", methods=['GET'])
def chatproductionalerts():
    try:
        verify_slack_token('GET', ALLOWED_TOKEN_LIST)
        verify_slack_username('GET', inspect.stack()[0][3], METHOD_ACL_USERLIST)

        content = '''{
    \"text\": \"Nagios alerts: 2 critical, 3 warning.\",
    \"attachments\": [
        {
            \"text\":\"Criticals:

prod-app-01 check_app_mem  30m29s
prod-app-02 check_app_pid  10m29s

prod-es-16 check_elasticsearch_slow_query 8h17m9s
prod-es-17 check_elasticsearch_slow_query 20h17m9s
prod-es-17 check_elasticsearch_slow_query 2d20h17m9s
\"
        }
    ]
}'''
        resp = make_response(content, 200)
        resp.headers['Content-type'] = 'application/json; charset=utf-8'
        return resp
    except Exception as e:
        return response_content("Error!", e)

def start_app(application):
    application.debug = True
    server_port = 8081
    # KEY_PASSPHRASE = os.environ.get('KEY_PASSPHRASE')
    # if KEY_PASSPHRASE is None:
    #     logging.error("ERROR: KEY_PASSPHRASE is not given via environment variables.")
    #     sys.exit(1)

    application.run(host="0.0.0.0", port=int(server_port))
    
if __name__ == '__main__':
    start_app(application)
## File : chatops.py ends
