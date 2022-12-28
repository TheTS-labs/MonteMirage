from datetime import datetime

from peewee import FloatField, Model, TextField, TimestampField

from constants import DB


class HistoricalSrcPrice(Model):
    timestamp = TimestampField(default=datetime.timestamp(datetime.now()))
    price = FloatField()
    src = TextField(default="Undefined")
    coin = TextField(default="Undefined")
    ticker = TextField(default="Undefined")

    class Meta(object):  # noqa: D106
        database = DB


class HistoricalOverview(Model):
    timestamp = TimestampField(default=datetime.timestamp(datetime.now()))
    std_between_srcs = FloatField(default=-1.0)
    mean_between_srcs = FloatField(default=-1.0)
    coin = TextField(default="Undefined")
    ticker = TextField(default="Undefined")

    class Meta(object):  # noqa: D106
        database = DB
