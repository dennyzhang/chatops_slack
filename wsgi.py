#!/usr/bin/python
##-------------------------------------------------------------------
## File : wsgi.py
## Author : Denny <denny@dennyzhang.com>
## Description :
## --
## Created : <2017-06-02>
## Updated: Time-stamp: <2017-06-02 11:51:58>
##-------------------------------------------------------------------
from chatops import application
from chatops import start_app

if __name__ == "__main__":
    start_app(application)
## File : wsgi.py ends
