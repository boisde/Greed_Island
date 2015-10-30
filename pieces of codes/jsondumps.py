#!/usr/bin/env python
# coding:utf-8

import json

d = {"url": "http://www.123feng.com:8885/deliver-app/middle-team-check-available-delivers/?mid_leader_id=7754317&date=2015-10-31&name=刘玉波", "cover": "", "thumbnail": "", "title": "明日出勤人员统计表"}
# d = str(d)
# if hasattr(d, 'isoformat'):
#     d = d.isoformat()
dj = json.dumps(d)
json.loads(dj)