# -*- coding: utf-8 -*-
# easy_install peewee
from peewee import *
import dateutil.parser
import datetime
import time


db = SqliteDatabase('twitter_stream.sqlite')


class Twitte(Model):
    createAt = DateTimeField(index=True)
    idStr = CharField(index=True)
    contents = CharField()

    class Meta:
        database = db


def AppendTwitte(item):
    row = Twitte(createAt=dateutil.parser.parse(item['created_at']),
                 idStr=item['id_str'],
                 contents=item['text'])
    row.save()


def GetTwitteHistogram(start_date, end_date, interval_sec):
    start_date = dateutil.parser.parse(start_date)
    end_date = dateutil.parser.parse(end_date)
    interval_sec = int(interval_sec)
    ret = []
    tmpdate = start_date
    while tmpdate < end_date:
        data = (
            tmpdate.strftime('%Y-%m-%d %H:%M:%S'),
            Twitte.select().where(
                (Twitte.createAt >= tmpdate) &
                (Twitte.createAt < tmpdate + datetime.timedelta(seconds=interval_sec))
            ).count()
        )
        ret.append(data)
        tmpdate = tmpdate + datetime.timedelta(seconds=interval_sec)
    return ret


def GetTwittes(start_date, end_date):
    start_date = dateutil.parser.parse(start_date)
    end_date = dateutil.parser.parse(end_date)
    return Twitte.select().where(
                (Twitte.createAt >= start_date) &
                (Twitte.createAt < end_date)
    )
