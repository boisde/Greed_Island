# -*- coding:utf-8 -*-
# 统一的时区处理类

import pytz
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse
from dateutil import tz
from dateutil.relativedelta import relativedelta
from django.utils.timezone import utc
from django.utils.timezone import localtime
from django.utils.timezone import now
from django.utils.timezone import is_naive
from django.utils.timezone import get_default_timezone


if __name__ == "__main__":
    from django.conf import settings
    settings.configure(USE_TZ=True, TIME_ZONE='Asia/Shanghai')


class TimeZone(object):
    # <DstTzInfo 'Asia/Shanghai' LMT+8:00:00 STD>
    # actual is <DstTzInfo 'Asia/Shanghai' LMT+8:06:00 STD>
    DEFAULT_TIMEZONE = get_default_timezone()
    UTC_DATE_TIME_PATTEN = '%Y-%m-%dT%H:%M:%SZ'
    DEFAULT_DATE_TIME_PATTEN='%Y-%m-%dT%H:%M:%S+08:00'

    @classmethod
    def naive_to_aware(cls, naive_datetime, tz=DEFAULT_TIMEZONE):
        """
        非时区datetime对象转换为带时区属性的datetime对象
        :param naive_datetime:
        :param tz:
        :return:
        """
        # return +08:06
        # return naive_datetime.replace(tzinfo=tz)

        # return +08:00
        return tz.localize(naive_datetime)

    @classmethod
    def datetime_to_timezone(cls, d, tz=utc):
        if is_naive(d):
            # change to local aware datetime
            d = cls.naive_to_aware(d)
        return localtime(d, timezone=tz)

    @classmethod
    def datetime_to_utc(cls, d):
        """

        :param d:
        :return:
        """
        return cls.datetime_to_timezone(d, tz=utc)

    @classmethod
    def utc_to_local(cls, utc_datetime):
        return cls.utc_to_timezone(utc_datetime)

    @staticmethod
    def utc_to_timezone(utc_datetime, tz=DEFAULT_TIMEZONE):
        if is_naive(utc_datetime):
            utc_datetime = utc_datetime.replace(tzinfo=utc)
        return localtime(utc_datetime, timezone=tz)

    @staticmethod
    def utc_now():
        return now()

    @classmethod
    def local_now(cls):
        return cls.DEFAULT_TIMEZONE.localize(datetime.now())

    @staticmethod
    def increment_months(cur_datetime, n=1):
        assert n >= 0
        return cur_datetime + relativedelta(months=n)

    @staticmethod
    def decrement_months(cur_datetime, n=1):
        assert n >= 0
        return cur_datetime - relativedelta(months=n)

    @staticmethod
    def increment_seconds(cur_datetime, n=1):
        assert n >= 0
        return cur_datetime + relativedelta(seconds=n)

    @staticmethod
    def decrement_seconds(cur_datetime, n=1):
        assert n >= 0
        return cur_datetime - relativedelta(seconds=n)

    @staticmethod
    def increment_hours(cur_datetime, n=1):
        assert n >= 0
        return cur_datetime + relativedelta(hours=n)

    @staticmethod
    def decrement_hours(cur_datetime, n=1):
        assert n >= 0
        return cur_datetime - relativedelta(hours=n)

    @staticmethod
    def month_range(year, month, tz=utc):
        assert year >= 0
        assert 12 >= month >= 1
        start_date = datetime(year, month, 1)
        end_date = TimeZone.increment_months(start_date)
        return TimeZone.datetime_to_timezone(start_date, tz), TimeZone.datetime_to_timezone(end_date, tz)

    @classmethod
    def datetime_to_str(cls, d):
        return d.strftime(cls.UTC_DATE_TIME_PATTEN)

    @staticmethod
    def str_to_datetime(d_str):
        dt = parse(d_str)
        if dt.tzinfo != tz.tzutc():
            dt -= dt.tzinfo._offset
            dt = dt.replace(tzinfo=tz.tzutc())
        return dt

    @classmethod
    def date_to_str(cls, d):
        return d.strftime("%Y-%m-%d")

    @classmethod
    def str_to_date(cls, d_str):
        return parse(d_str)

    @staticmethod
    def increment_days(cur_datetime, d=1):
        assert d >= 0
        return cur_datetime + timedelta(days=d)

    @staticmethod
    def decrement_days(cur_datetime, d=1):
        assert d >= 0
        return cur_datetime - timedelta(days=d)

    @staticmethod
    def day_range(year=0, month=0, day=0, tz=utc, local_day=None):
        # 传入的日期是本地时区
        if local_day:
            year, month, day = local_day.year, local_day.month, local_day.day
        assert year >= 0
        assert 12 >= month >= 1
        assert 31 >= day >= 1
        start_datetime = datetime(year, month, day)
        end_datetime = TimeZone.increment_days(start_datetime)
        return TimeZone.datetime_to_timezone(start_datetime, tz), TimeZone.datetime_to_timezone(end_datetime, tz)

    # 返回传入日期的当天起始时间
    @staticmethod
    def transfer_datetime_to_beginning(cur_datetime):
        return cur_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

    # date转datetime，datetime是时区无关的
    @classmethod
    def date_to_datetime(cls, d):
        # 如果是字符串则先进行转化
        if type(d) in (str, unicode):
            d = cls.str_to_date(d)
        return datetime(d.year, d.month, d.day)

    @staticmethod
    def datetime_to_date(dt):
        return dt.date()

    @staticmethod
    def format_to_sql_datetime(d):
        return d.strftime('%Y-%m-%d %H:%M:%S')


if __name__ == "__main__":
    local_now = datetime.now()
    print 'local_time: %s' % TimeZone.naive_to_aware(local_now, pytz.timezone(pytz.country_timezones('cn')[0]))
    print 'local_time: %s' % TimeZone.naive_to_aware(local_now)
    print 'utc_time: %s' % TimeZone.datetime_to_utc(local_now)
    print 'utc_time_str: %s' % TimeZone.datetime_to_str(TimeZone.datetime_to_utc(local_now))
    print 'utc_now: %s' % TimeZone.utc_now()
    print 'local_now: %s' % TimeZone.local_now()

    print 'first in 2014-08 in utc: %s' % TimeZone.datetime_to_utc(datetime(2014, 8, 1))
    print 'last  in 2014-08 in utc: %s' % TimeZone.datetime_to_utc(datetime(2014, 9, 1))

    local_d1 = datetime(2014, 9, 15, 23, 22, 10)
    assert TimeZone.naive_to_aware(local_d1) == TimeZone.utc_to_local(TimeZone.datetime_to_utc(local_d1))

    print '2013-12: (%s~%s)' % (TimeZone.month_range(2013, 12))
    print '2014-01: (%s~%s)' % (TimeZone.month_range(2014, 1))

    print '2014-01-01: (%s~%s)' % (TimeZone.day_range(2014, 1, 1))
    print '2013-12-31: (%s~%s)' % (TimeZone.day_range(2013, 12, 31))
    print '2012-03-01: (%s~%s)' % (TimeZone.day_range(2012, 3, 1))
    print '2014-03-01: (%s~%s)' % (TimeZone.day_range(2014, 3, 1))
