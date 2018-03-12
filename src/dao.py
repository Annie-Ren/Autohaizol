#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_base_test_cases(db, module_name):
    return db.query("select * from test_case where module_name = %(module_name)s", module_name=module_name)


def set_base_test_case(db, test_id, test_status, test_message):
    return db.insert("insert into test_result(result_status, result_message, test_id,"
                      "test_time) values(%(status)s, %(message)s, %(test_id)s, CURRENT_TIMESTAMP)",
                      status=test_status, message=test_message, test_id=test_id)
