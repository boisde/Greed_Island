#!/usr/bin/env python
# coding:utf-8
import unittest
import requests_mock

import os, sys
sys.path.insert(1, os.path.join(os.path.dirname(__file__), os.pardir))
from grade import PayrollGradeLogic


class TestStaffOrg(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_grade_man(self):
        with requests_mock.mock() as m:
            pass