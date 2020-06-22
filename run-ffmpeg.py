#!/usr/bin/env python3
import os
import sys
import shlex
import subprocess
# import multiprocessing
# import multiprocessing.Pool as Pool
from multiprocessing import Pool


def f(x):
    command = "ffmpeg -i /home/ubuntu/test-with-timer.flv -c:v copy -strict -2 -b:v 3M -maxrate 4M -c:a aac -f flv rtmp://ingest-b0.inner.dlivecdn.com/live/dlivetestdlivetestdlivetestdlive_dlivetest-%d &" % x
    print(command)
    # proc = subprocess.run(shlex.split(command))
    # os.system(command)
    subprocess.run(command, shell=True)


if __name__ == "__main__":
    # buf = []
    # # print(sys.argv)
    start_id = int(sys.argv[1]) if len(sys.argv)>=2 else 1
    end_id = int(sys.argv[2]) if len(sys.argv)>=3 else 5
    # for  i in range(start_id,end_id+1):
    #     line = "ffmpeg -i ~/test-with-timer.flv -c:v copy -strict -2 -b:v 3M -maxrate 4M -c:a aac -f flv rtmp://ingest-b0.inner.dlivecdn.com/live/dlivetestdlivetestdlivetestdlive_dlivetest-%d &\n" % i
    #     buf.append(line)

    # sh_file_name = "ffmpeg-%d-%d.sh" % (start_id, end_id)
    # with open(sh_file_name, "w+") as f:
    #     for l in buf:
    #         f.write(l)

    # print(sh_file_name)
    # pool = Pool(processes=16)
    # pool.map(f, list(range(start_id,end_id+1)))
    with Pool(8) as p:
        print(p.map(f, list(range(start_id,end_id+1))))
        p.close()



    # jobs = []
    # for i in range(start_id, end_id+1):
    #     p = multiprocessing.Process(target=f, args=(i,))
    #     jobs.append(p)
    #     p.start()
