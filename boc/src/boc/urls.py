from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
# Licensed to Cloudera, Inc. under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  Cloudera, Inc. licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


urlpatterns = patterns('boc',
    url(r'^$', 'views.index'),
    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^get_hive', 'boc.views.get_hive', name='get_hive'),
    url(r'^query$', 'views.query', name='query'),
)

