#!/usr/bin/env python3
import subprocess
import json

if __name__=="__main__":
    with open("playback-1.m3u8") as f:
        line = f.readline()
        while line:
            if line[0] == '#':
                pass
            else:
                # c1 = "wget %s" % line
                # return_code = subprocess.call(c1, shell=True)

                # get file name
                a = line.split('/')
                name = a[7]
                # print(name)

                # add file
                c2 = "curl -sb -i 'http://localhost:5001/api/v1/add?chunker=reed-solomon' --form 'file=@/Users/chenxinlu/Downloads/%s'" % name
                return_code = subprocess.check_output(c2, shell=True)
                # print(return_code)

                # get hash
                y = json.loads(return_code)
                # print(y["Hash"])

                # cat to another file
                l = "http://localhost:5001/api/v1/cat?arg=%s" % y["Hash"]
                print("#EXTINF:20.000,")
                print(l)

            line = f.readline()