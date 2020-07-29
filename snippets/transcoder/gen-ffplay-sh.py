#!/usr/bin/env python3
import os
import subprocess
import sys
from multiprocessing import Process
from multiprocessing import set_start_method

# Usage: (1) ./gen-ffplay-sh.py 1 10 local
# (2) ./gen-ffplay-sh.py 1 100 remote


if __name__ == "__main__":
    # 1. Global configurations of ingest server
    conf = dict(
        local={
            "rtmp_server_domain": "127.0.0.1"
        },
        remote={
            "rtmp_server_domain": "ingest-b0.inner.dlivecdn.com"
        }
    )
    which_env = str(sys.argv[3]) if len(sys.argv) >= 4 else 'remote'
    rtmp_server_domain = conf[which_env]['rtmp_server_domain']

    # 2. take in args from command line
    start_id = int(sys.argv[1]) if len(sys.argv) >= 2 else 1
    end_id = int(sys.argv[2]) if len(sys.argv) >= 3 else 1
    daemon = '' if len(sys.argv) >= 5 and (str(sys.argv[4]) != 'daemon') else '&'

    # 3. generate command line
    buf = []
    for i in range(start_id, end_id + 1):
        line = "ffplay -i " \
               "rtmp://{rtmp_server_domain}/live/dlivetestdlivetestdlivetestdlive_dlivetest-{i} {daemon}\n".format(
                rtmp_server_domain=rtmp_server_domain, i=i, daemon=daemon)
        buf.append(line)

    sh_file_name = "ffplay-%d-%d.sh" % (start_id, end_id)
    with open(sh_file_name, "w+") as f:
        for l in buf:
            f.write(l)

    print(sh_file_name)
    for l in buf:
        print(l[:-1])

    os.system("chmod +x %s" % sh_file_name)
