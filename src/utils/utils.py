#!/usr/bin/env python
# -*- coding: utf-8 -*-
import torndb
import config
import json


def get_mysqldb():
   return  torndb.Connection(host=config.MYSQL_HOST, user=config.MYSQL_USER,
                              password=config.MYSQL_PASSWD, database=config.MYSQL_DATABASE,
                              time_zone='+8:00', max_idle_time=2520)


def get_value_from_json(jstr, key):
    try:
        json_obj = json.loads(jstr)
        return json_obj.get(key)
    except Exception as e:
        return None


def loads_json(jstr):
    try:
        return json.loads(jstr)
    except Exception as e:
        return None



