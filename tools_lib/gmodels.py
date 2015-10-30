# -*- coding:utf-8 -*-

from django.db import models


class BaseModel(models.Model):
    """
    基类模型
    """
    create_time = models.DateTimeField(auto_now_add=True, db_column="create_time")
    update_time = models.DateTimeField(auto_now=True, db_column="update_time")
    deleted = models.NullBooleanField(default=False, db_column="deleted")

    class Meta:
        abstract = True

    @classmethod
    def create(cls, **kwargs):
        kwargs['deleted'] = False
        return cls.objects.create(**kwargs)

    @classmethod
    def get(cls, **kwargs):
        kwargs['deleted'] = False
        try:
            return cls.objects.get(**kwargs)
        except:
            return None

    @classmethod
    def filter(cls, **kwargs):
        kwargs['deleted'] = False
        return cls.objects.filter(**kwargs)