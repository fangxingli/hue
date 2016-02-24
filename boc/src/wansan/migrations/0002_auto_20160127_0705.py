# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wansan', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='querycate',
            name='createtime',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='querysubcate',
            name='createtime',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
