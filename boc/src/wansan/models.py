# encoding: utf-8
from django.db import models


# 查询大类
#   -cateid
#   -name
#   -createby
#   -createtime
class QueryCate(models.Model):
    name = models.CharField(max_length=16)
    createtime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


# 查询子类
#   -subcateid
#   -parent_cateid
#   -name
#   -comment
#   -createby
#   -craetetime
#   -sql
class QuerySubCate(models.Model):
    name = models.CharField(max_length=16)
    parent_cate = models.ForeignKey(QueryCate)
    comment = models.CharField(max_length=64)
    createtime = models.DateTimeField(auto_now_add=True)
    sql = models.CharField(max_length=2048)
