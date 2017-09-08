#!/usr/bin/python
##-------------------------------------------------------------------
## File : wsgi.py
## Author : Denny <contact@dennyzhang.com>
## Description :
## --
## Created : <2017-06-02>
## Updated: Time-stamp: <2017-09-04 18:52:04>
##-------------------------------------------------------------------
from chatops import application
from chatops import start_app

if __name__ == "__main__":
    start_app(application)
## File : wsgi.py ends
