# encoding: utf-8
from django.db import models
from django.contrib.auth.models import User


# 查询大类
#   -cateid
#   -name
#   -createby
#   -createtime
class QueryCate(models.Model):
    name = models.CharField(max_length=16)
    created_by = models.ForeignKey(User)
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
    name = models.CharField(max_length=16, help_text=u'查询场景名')
    parent_cate = models.ForeignKey(QueryCate, related_name="querysubcate_cate", help_text=u'查询大类')
    created_by = models.ForeignKey(User, related_name="querysubcate_user", help_text=u'创建用户')
    comment = models.CharField(max_length=64, help_text=u'查询场景说明')
    createtime = models.DateTimeField(auto_now_add=True, help_text=u'创建时间')
    sql = models.CharField(max_length=2048, help_text=u'创建SQL')
    type = models.IntegerField(null=False, help_text=u'类型(Hive or Hbase)')
    columns = models.CharField(max_length=1024, help_text=u'存储到HBase中的列名, JSON格式')
    column_names = models.CharField(max_length=1024, help_text=u'供展示用列名(中文), JSON格式')
    conditions = models.CharField(max_length=128, help_text=u'查询条件列(取columns中的值)')
    condition_types = models.CharField(max_length=512, help_text=u'查询条件列显示控件属性(比如,input控件还是Date picker控件)')
    sorted = models.CharField(max_length=32, help_text=u'按哪列排序')

    def __unicode__(self):
        return self.name


class QueryHistory(models.Model):
    query_time = models.DateTimeField(auto_now_add=True)
    query_by = models.ForeignKey(User, related_name="queryhistory_user")
    query = models.ForeignKey(QuerySubCate, related_name="queryhistory_query")
    query_begin = models.DateTimeField()
    query_end = models.DateTimeField()


