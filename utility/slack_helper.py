#!/usr/bin/python
##-------------------------------------------------------------------
## File : slack_helper.py
## Author : Denny <contact@dennyzhang.com>
## Description :
## --
## Created : <2017-05-22>
## Updated: Time-stamp: <2017-09-04 18:52:05>
##-------------------------------------------------------------------
import sys
from flask import make_response
from flask import request
import requests, json

################################################################################
def verify_slack_token(http_method, allowed_token_list):
    token = ''
    if http_method == 'GET':
        token = request.args.get('token', '')
    elif http_method == 'POST':
        token = request.values['token']
    else:
        raise Exception("Error: unsupported http_method(%s)" % (http_method))

    if token not in allowed_token_list:
        content = "Error: invalid token(%s)" % (token)
        raise Exception(content)
    return None

def verify_slack_username(http_method, api_method, method_acl_userlist):
    user_name = ''
    if http_method == 'GET':
        user_name = request.args.get('user_name', '')
    elif http_method == 'POST':
        user_name = request.values['user_name']
    else:
        raise Exception("Error: unsupported http_method(%s)" % (http_method))

    if "*" in method_acl_userlist:
        super_name_list = method_acl_userlist["*"]
        if user_name in super_name_list:
            return None

    if api_method in method_acl_userlist:
        allowed_user_list = method_acl_userlist[api_method]
        if user_name not in allowed_user_list:
            content = "Error: user(%s) not allowed to call api_method(%s)" % \
                      (user_name, api_method)
            raise Exception(content)

    return None

def response_content(summary, details):
    content = '''{
    \"text\": \"%s\",
    \"attachments\": [
        {
            \"text\":\"%s\"
        }
    ]
}''' % (summary, details)
    resp = make_response(content, 200)
    resp.headers['Content-type'] = 'application/json; charset=utf-8'
    return resp

def get_response_url(http_method):
    response_url = ''
    if http_method == 'GET':
        response_url = request.args.get('response_url', '')
    elif http_method == 'POST':
        response_url = request.values['response_url']
    else:
        raise Exception("Error: unsupported http_method(%s)" % (http_method))
    if response_url == '':
        raise Exception("Error: fail to get response_url from the http request")
    return response_url

def slack_send_delay_response(para_list):
    response_url = para_list[0]
    function = para_list[1]
    arg_list = para_list[2]
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    # print "arg_list: %s" % (arg_list)
    # TODO: better implementation
    (summary, details) = function(arg_list)
    m = {"text": summary, "attachments": [{"text": details}]}
    json_response = json.dumps(m)
    payload = json.loads(json_response)
    # TODO: remove this
    print("payload: %s" % (str(payload)))
    requests.post(response_url, data=json.dumps(payload), headers=headers)
## File : slack_helper.py ends
