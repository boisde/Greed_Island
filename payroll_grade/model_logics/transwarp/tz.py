#!/usr/bin/env python
# coding:utf-8
import re
import datetime

_TIMEDELTA_ZERO = datetime.timedelta(0)

# timezone as UTC+8:00, UTC-10:00
_RE_TZ = re.compile('^([\+\-])([0-9]{1,2})\:([0-9]{1,2})$')

class UTC(datetime.tzinfo):
    """
    A UTC tzinfo object.

    >>> tz0 = UTC('+00:00')
    >>> tz0.tzname(None)
    'UTC+00:00'
    >>> tz8 = UTC('+8:00')
    >>> tz8.tzname(None)
    'UTC+8:00'
    >>> tz7 = UTC('+7:30')
    >>> tz7.tzname(None)
    'UTC+7:30'
    >>> tz5 = UTC('-05:30')
    >>> tz5.tzname(None)
    'UTC-05:30'
    >>> import datetime
    >>> u = datetime.datetime.utcnow().replace(tzinfo=tz0)
    >>> l1 = u.astimezone(tz8)
    >>> l2 = u.replace(tzinfo=tz8)
    >>> d1 = u - l1
    >>> d2 = u - l2
    >>> d1.seconds
    0
    >>> d2.seconds
    28800
    """

    def __init__(self, utc):
        utc = str(utc.strip().upper())
        mt = _RE_TZ.match(utc)
        if mt:
            minus = mt.group(1)=='-'
            h = int(mt.group(2))
            m = int(mt.group(3))
            if minus:
                h, m = (-h), (-m)
            self._utcoffset = datetime.timedelta(hours=h, minutes=m)
            self._tzname = 'UTC%s' % utc
        else:
            raise ValueError('bad utc time zone')

    def utcoffset(self, dt):
        return self._utcoffset

    def dst(self, dt):
        return _TIMEDELTA_ZERO

    def tzname(self, dt):
        return self._tzname

    def __str__(self):
        return 'UTC tzinfo object (%s)' % self._tzname

    __repr__ = __str__

# 常用时区
UTC_0, UTC_8 = UTC('+00:00'), UTC('+08:00')
# 常用日期时间定义
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"


def utc_8_now():
    now = datetime.datetime.utcnow().replace(tzinfo=UTC_0).astimezone(UTC_8).strftime(DATETIME_FORMAT)
    return now


def utc_now():
    now = datetime.datetime.utcnow().replace(tzinfo=UTC_0).strftime(DATETIME_FORMAT)
    return now


def n_days_before(n):
    n = int(n)
    now = datetime.datetime.utcnow().replace(tzinfo=UTC_0).astimezone(UTC_8)
    days = datetime.timedelta(days=n)
    n_day_before = now - days
    return n_day_before.strftime(DATETIME_FORMAT)


def check_interval(date_str, days):
    past_date = datetime.datetime.strptime(date_str, DATE_FORMAT).date()
    days = int(days)
    from_date = datetime.date.fromordinal(datetime.date.today().toordinal() - days)
    now = datetime.datetime.utcnow().replace(tzinfo=UTC_0).astimezone(UTC_8).date()
    if from_date <= past_date <= now:
        return True
    else:
        return False


def last_month():
    last_day = (datetime.datetime.utcnow().replace(tzinfo=UTC_0).astimezone(UTC_8).replace(day=1)-datetime.timedelta(days=1))
    first_day = last_day.replace(day=1)
    return (last_day-first_day).days+1, first_day.strftime(DATE_FORMAT), last_day.strftime(DATE_FORMAT)

