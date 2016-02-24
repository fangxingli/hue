# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wansan', '0002_auto_20160127_0705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='querycate',
            name='createtime',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='querysubcate',
            name='createtime',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
    ]
