import trollius
from trollius import From
import time
import requests

@trollius.coroutine
def greet_every_two_seconds(loop):
    time0 = time.time()
    # yield From(trollius.sleep(2))
    # print('Hello World[%s]' % (time.time() - time1))
    # loop = trollius.get_event_loop()
    future1 = loop.run_in_executor(None, requests.get, 'http://www.stackoverflow.com')
    future2 = loop.run_in_executor(None, requests.get, 'http://www.yinwang.org/')
    future3 = loop.run_in_executor(None, requests.get, 'http://www.haiyun.me/')
    response1 = yield From(future1)
    time1 = time.time()
    print("[yield resp1] since=[%s]" % int((time1-time0)*1000))
    response2 = yield From(future2)
    # time1 = time.time() - time1
    # print("[yield resp2] since=[%s]" % time1)
    # print(response1.text[:10])
    # print(response2.text[:10])
    time2 = time.time()
    print("[yield resp2] since=[%s]" % (int((time2-time1)*1000)))

    response3 = yield From(future3)
    time3 = time.time()
    print("[yield resp3] since=[%s]" % (int((time3-time2)*1000)))


time_all = time.time()
loop = trollius.get_event_loop()
loop.run_until_complete(greet_every_two_seconds(loop))
time_all = time.time() - time_all
print("[all-async] since=[%s]\n" % int(time_all*1000))




def normal():
    time0 = time.time()
    # yield From(trollius.sleep(2))
    # print('Hello World[%s]' % (time.time() - time1))
    # loop = trollius.get_event_loop()
    response1 = requests.get('http://www.stackoverflow.com')
    time1 = time.time()
    print("[N_yield resp1] since=[%s]" % int((time1-time0)*1000))
    response2 = requests.get('http://www.yinwang.org/')
    # time1 = time.time() - time1
    # print("[yield resp2] since=[%s]" % time1)
    # print(response1.text[:10])
    # print(response2.text[:10])
    time2 = time.time()
    print("[N_yield resp2] since=[%s]" % (int((time2-time1)*1000)))
    response3 = requests.get('http://www.haiyun.me/')
    time3 = time.time()
    print("[N_yield resp3] since=[%s]" % (int((time3-time2)*1000)))

time_all = time.time()
normal()
time_all = time.time() - time_all
print("[all-serical] since=[%s]\n" % int(time_all*1000))


