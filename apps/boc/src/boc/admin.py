# encoding: utf-8
from django.contrib import admin
from boc.models import QueryCate, QuerySubCate, QueryHistory


# admin.site.register(QueryHistory)
admin.site.register(QueryCate)
admin.site.register(QuerySubCate)


# 一下模块是hue在admin自带的, 取消之
from django.contrib.auth.models import Group, User
admin.site.unregister(User)
admin.site.unregister(Group)

from axes.models import AccessAttempt, AccessLog
admin.site.unregister(AccessAttempt)
admin.site.unregister(AccessLog)

from beeswax.models import QueryHistory as QH
from beeswax.models import SavedQuery, Session
admin.site.unregister(QH)
admin.site.unregister(SavedQuery)
admin.site.unregister(Session)

from desktop.models import DocumentPermission, DocumentTag, Document
admin.site.unregister(DocumentPermission)
admin.site.unregister(DocumentTag)
admin.site.unregister(Document)

from django_openid_auth.models import Association, Nonce, UserOpenID
admin.site.unregister(Association)
admin.site.unregister(Nonce)
admin.site.unregister(UserOpenID)

from jobsub.models import JobDesign
admin.site.unregister(JobDesign)

from search.models import Collection
admin.site.unregister(Collection)

from django.contrib.sites.models import Site
admin.site.unregister(Site)