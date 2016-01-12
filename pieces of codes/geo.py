#!/usr/bin/env python
# coding:utf-8

from map_api import get_location_coordinates

lat, lng = get_location_coordinates(dict(city="杭州市",district="",street="万塘路258号杭州师范大学"))
print ("%s, %s" % (lng, lat))
lat, lng = get_location_coordinates(dict(city="杭州市",district="西湖区",street="万塘路258号杭州师范大学"))
print ("%s, %s" % (lng, lat))
lat, lng = get_location_coordinates(dict(city="杭州市",district="西湖区",street="万塘路258号"))
print ("%s, %s" % (lng, lat))

