# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QueryCate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=16)),
                ('createtime', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuerySubCate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=16)),
                ('comment', models.CharField(max_length=64)),
                ('createtime', models.DateTimeField()),
                ('sql', models.CharField(max_length=2048)),
                ('parent_cate', models.ForeignKey(to='wansan.QueryCate')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
