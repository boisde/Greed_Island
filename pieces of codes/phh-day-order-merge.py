#!/usr/bin/env python
# coding:utf-8

import time
from map_api import get_location_coordinates

d = []
with open("/Users/chenxinlu/Developer/Greed_Island/pieces of codes/phh-day-order-raw-DAY1.csv", 'r') as f:
    l = f.readline()
    while l:
        a = l.split(',')
        d.append(a)
        l = f.readline()
data = [(i[0], i[1][:-1]) for i in d]

pt = []
N = 500
s1, s2, s3 = set(), set(), set()
fin = {}
for i, d in enumerate(data):
    print(i)
    precise, confidence, lng, lat = get_location_coordinates(dict(city="杭州市", district=d[0], street=d[1]))
    if precise == 0 and confidence == 0 and lng == 0 and lat == 0:
        time.sleep(60)

    pt.append(dict(pt=[lng, lat], precise=precise, confidence=confidence, addr=d[1]))
    x = "%s %s" % (lng, lat)
    if x in s3:
        fin[str(x)] += 1
    elif x in s2:
        s2.remove(x)
        s3.add(x)
        fin[str(x)] = 3
    elif x in s1:
        s1.remove(x)
        s2.add(x)
        fin[str(x)] = 2
    else:
        s1.add(x)
        fin[str(x)] = 1


with open("/Users/chenxinlu/Developer/Greed_Island/pieces of codes/phh-day-order-raw.csv", 'a') as f:
    for j in xrange(len(pt)):
        it = pt[j]
        try:
            addr = unicode(it['addr'], encoding='utf-8').encode('utf-8')
        except:
            addr = "Unicode error"
        f.write("%s,%s %s,%s,%s\n" % (addr, it['pt'][0], it['pt'][1], it['confidence'], it['precise']))


# with open("/Users/chenxinlu/Developer/Greed_Island/pieces of codes/phh-day1-merge.csv", 'w') as f:
#     for k, cnt in fin.iteritems():
#         f.write("%s,%s\n" % (k, cnt))

with open("/Users/chenxinlu/Developer/Greed_Island/pieces of codes/phh-day-order-fin.csv", 'w') as f:
    for k, cnt in fin.iteritems():
        if cnt >= 3:
            cash = 3 * cnt
        elif cnt == 2:
            cash = 4 * cnt
        elif cnt == 1:
            cash = 5
        else:
            cash = 0
        f.write("%s,%s,%s\n" % (k, cnt, cash))
