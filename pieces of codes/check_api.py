#!/usr/bin/env python
# coding:utf-8

# optparse is Python 2.3 - 2.6, deprecated in 2.7
# For 2.7+ use http://docs.python.org/library/argparse.html#module-argparse
from optparse import OptionParser
import requests
import json
import signal

# Exit statuses recognized by Nagios
UNKNOWN = -1
OK = 0
WARNING = 1
CRITICAL = 2

# Template for reading parameters from commandline
parser = OptionParser()
parser.add_option("-m", "--message", dest="message", default='passed', help="A message to print after OK - ")
(options, args) = parser.parse_args()

# INIT
core = "http://10.0.0.234:5555"
ag = "http://10.0.0.240:5556"
urls = [
    # 风先生 #
    ("GET", core + "/staff/token/a30b36d7ebe553bcccc795e67ebe5c3c", {}),
    # ("GET", "/staff_info/get_one/user/21186", {}),
    # ("GET", "/staff_info/get_user_ids/deliver_team/0/0/50", {}),
    # ("GET", "/staff_info/get_basics/deliver_team/0/0/1", {}),
    # ("GET", "/staff_org/get_one/user_id/7740959", {}),
    # ("GET", "/staff_org/get_user_ids/level/0/0/50", {}),
    # ("GET", "/staff_org/get_basics/level/0/0/50", {}),
    # ("POST", "/staff_info", {}),
    # ("POST", "/staff_info/user/0/delete", {}),
    # ("POST", "/staff_info/user/0/update", {}),
    # ("POST", "/staff_org", {}),
    # ("POST", "/staff_org/user_id/0/delete", {}),
    # ("POST", "/staff_org/user_id/0/unbind", {}),
    # ("GET", "/staff_org/get_one/user_id/0", {}),
    # ("GET", "/staff_org/get_user_ids/level/0/0/50", {}),
    # ("GET", "/staff_org/get_basics/level/0/0/50", {}),
    ("POST", core + "/staff_join/org_info",
     {"filter_col": ["user"], "org_kn": [], "org_kvs": [], "info_kn": ["user"], "info_kvs": [[7749772]],
      "which_page": 0, "each_fetch": 1}),
    # API Gateway #
    ("GET", ag + "/staff/app/news?count=6&page=1&status=3", {},
     {"Authorization": "token 0b3d4a5819526224f60592cffd2c1ed6"}),
    ("POST", ag + "/staff/cloud/news", {"title": "dddd风课堂：硬汉也要学防暑", "body": "风先生们，夏日挑战来袭，一定要注意防暑防晒，身体好才能多送单！",
                                        "image_id": "a1a5b8136fb625e6ca26fed442d56547",
                                        "link": "http://nr.123feng.com/?p=2403",
                                        "top_image_id": "dd21f2714125d228d7226640a8862be3",
                                        "to_city_code": "330100000000", "to_level": "2,3,4", "to_type": 1,
                                        "news_type": 2}, {"Authorization": "token 0b3d4a5819526224f60592cffd2c1ed6"}),
    ("PATCH", ag + "/staff/cloud/news/18", {"status": 1},{"Authorization": "token 0b3d4a5819526224f60592cffd2c1ed6"}),
]
total, ok_cnt, err_cnt, timeout_cnt = len(urls), 0, 0, 0


def handler(signum, frame):
    # print "timeout %f" % time.time()
    raise UserWarning("end of time")


# Register the signal function handler
signal.signal(signal.SIGALRM, handler)

for url in urls:
    try:
        # Define a timeout in seconds
        signal.alarm(2)
        if url[0] == "GET":
            r = requests.get(url[1], params=url[2], headers=url[3] if len(url) == 4 else None)
        elif url[0] in ("POST", "PATCH"):
            headers = {'content-type': 'application/json'}
            headers.update(url[3] if len(url) == 4 else {})
            r = requests.request(str(url[0]).lower(), url[1], data=json.dumps(url[2]), headers=headers)
        else:
            total -= 1
            r = None
    except UserWarning:
        timeout_cnt += 1
    else:
        print "[%s] [%s]: [%d] [%s]" % (url[0], url[1], r.status_code, r.text[:20])
        if r.status_code == 200:
            ok_cnt += 1
        else:
            err_cnt += 1

# Return output to nagios
# Using the example -m parameter parsed from commandline
pass_rate = float(ok_cnt) / total
if 0.8 < pass_rate < 0.9:
    print 'WARN - (%d/%d) failed, (%d/%d) timed out.' % (err_cnt, total, timeout_cnt, total)
    raise SystemExit, WARNING
elif pass_rate <= 0.8:
    print 'CRITICAL - (%d/%d) failed, (%d/%d) timed out.' % (err_cnt, total, timeout_cnt, total)
    raise SystemExit, CRITICAL
else:
    print 'OK - (%d/%d) %s, (%d/%d) failed, (%d/%d) timed out.' % (ok_cnt, total, options.message, err_cnt, total,
                                                                   timeout_cnt, total)
    raise SystemExit, OK
