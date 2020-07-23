#!/usr/bin/env python3
import os
import subprocess
import sys
from multiprocessing import Process
from multiprocessing import set_start_method

# Usage: (1) ./gen-ffmpeg-sh.py 1 10 local foreground
# (2) ./gen-ffmpeg-sh.py 1 100 remote daemon


if __name__ == "__main__":
    # 1. Global configurations of ingest server
    conf = dict(
        local={
            "input_flv_file": "~/transcoder-testing/test-with-timer.flv",
            "rtmp_server_domain": "127.0.0.1"
        },
        remote={
            "input_flv_file": "test-with-timer.flv",
            "rtmp_server_domain": "127.0.0.1"
        }
    )
    which_env = str(sys.argv[3]) if len(sys.argv) >= 4 else 'remote'
    input_flv_file = conf[which_env]['input_flv_file']
    rtmp_server_domain = conf[which_env]['rtmp_server_domain']

    # 2. take in args from command line
    start_id = int(sys.argv[1]) if len(sys.argv) >= 2 else 1
    end_id = int(sys.argv[2]) if len(sys.argv) >= 3 else 1
    daemon = '' if len(sys.argv) >= 5 and (str(sys.argv[4]) != 'daemon') else '&'

    # 3. generate command line
    buf = []
    for i in range(start_id, end_id + 1):
        line = "ffmpeg -stream_loop 2 -re -i {input_flv_file} " \
               "-f flv -c:v copy -c:a aac -strict -2 -maxrate 4M " \
               "rtmp://{rtmp_server_domain}/live/dlivetestdlivetestdlivetestdlive_dlivetest-{i} {daemon}\n".format(
                input_flv_file=input_flv_file, rtmp_server_domain=rtmp_server_domain, i=i, daemon=daemon)
        buf.append(line)

    sh_file_name = "ffmpeg-%d-%d.sh" % (start_id, end_id)
    with open(sh_file_name, "w+") as f:
        for l in buf:
            f.write(l)

    print(sh_file_name)
    for l in buf:
        print(l[:-1])

    os.system("chmod +x %s" % sh_file_name)

    # pool = Pool(processes=16)
    # pool.map(f, list(range(start_id,end_id+1)))

    # with Pool(8) as p:
    #     print(p.map(f, list(range(start_id,end_id+1))))
    #     p.close()

    # jobs = []
    # for i in range(start_id, end_id+1):
    #     p = multiprocessing.Process(target=f, args=(i,))
    #     jobs.append(p)
    #     p.start()

    # for i in range(start_id, end_id + 1):
    #     p = Process(target=f, args=(i,))
    #     p.start()
    #     p.join()
