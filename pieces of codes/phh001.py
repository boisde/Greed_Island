#!/usr/bin/env python
# coding:utf-8
import json
from map_api import get_location_coordinates
with open("/Users/chenxinlu/Developer/Greed_Island/pieces of codes/phh001.json", 'r') as f:
    d = json.loads(f.read())
    d = d["result"]
    data = [(i["district"], i["addr"]) for i in d]

pt = []
for i, d in enumerate(data):
    print(i)
    precise, confidence, lng, lat = get_location_coordinates(dict(city="杭州市",district=d[0].encode('utf-8'),street=d[1].encode('utf-8')))
    pt.append(dict(pt=[lng, lat], precise=precise, confidence=confidence, addr=d[1].encode('utf-8')))

with open("/Users/chenxinlu/Developer/Greed_Island/pieces of codes/phh001.js", 'w') as f:
    f.write("var addrs = [")
    for i in xrange(len(pt)):
        it = pt[i]
        f.write("{\"pt\":%s, \"addr\":\"%s\", \"confidence\":%s, \"precise\":%s}" % (str(it['pt']), it['addr'], it['confidence'], it['precise']))
        if i != len(data) - 1:
            f.write(',\n')
    f.write("];")
