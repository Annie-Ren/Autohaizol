#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys

### env setting
# curr_dir = os.path.dirname(os.path.abspath(__file__))
# print(sys.path)
# print(os.path.abspath(__file__))
###sys.path = os.path.join(curr_dir)
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# db config here
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWD = "Asdf12345"
MYSQL_DATABASE = "aototest"


# project status here
STATUS_SUCCESS = 0
STATUS_NO_XPATH = 1
STATUS_FAILED = 2
MESSAGE_SUCCESS = "success"

TEST_TIME_SCALE = 10

# domain here
BASE_DOMAIN = "https://qa-online.haizol.com"
