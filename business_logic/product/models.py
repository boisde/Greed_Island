#!/usr/bin/env python
# coding:utf-8
from __future__ import unicode_literals
from mongoengine import (Document, StringField, IntField, ListField, DictField)


class Category(Document):
    name = StringField(comment='品类名')
    hs_code = StringField()
    seq_num = IntField(comment='同一级类目中自己的顺序, 从1开始')

    ancestor = ListField(comment='存放到达这个类目的路径category')
    parent = DictField()

    meta = []

    @classmethod
    def parse_from_json_list(cls):
        src = [
            {
                'name': '1_category_A',
                'hs_code': '001',
                'seq_num': 1,
                'children': [
                    {
                        'name': '2_category_AX',
                        'hs_code': '001',
                        'seq_num': 1,
                    },
                    {
                        'name': '2_category_AY',
                        'hs_code': '002',
                        'seq_num': 2,
                    },
                    {
                        'name': '2_category_AZ',
                        'hs_code': '002',
                        'seq_num': 3,
                    },
                ]
            },
            {
                'name': '1_category_B',
                'hs_code': '002',
                'seq_num': 2,
                'children': [
                    {
                        'name': '2_category_BX',
                        'hs_code': '001',
                        'seq_num': 1,
                    },
                    {
                        'name': '2_category_BY',
                        'hs_code': '002',
                        'seq_num': 2,
                    },
                    {
                        'name': '2_category_BZ',
                        'hs_code': '002',
                        'seq_num': 3,
                    },
                ]
            },
            {
                'name': '1_category_C',
                'hs_code': '003',
                'seq_num': 3,
                'children': [
                    {
                        'name': '2_category_CX',
                        'hs_code': '001',
                        'seq_num': 1,
                    },
                    {
                        'name': '2_category_CY',
                        'hs_code': '002',
                        'seq_num': 2,
                    },
                    {
                        'name': '2_category_CZ',
                        'hs_code': '002',
                        'seq_num': 3,
                    },
                ]
            }
        ]

        ancestor = []
        parent = {}
        for c in src:
            # dump
            
            pass
