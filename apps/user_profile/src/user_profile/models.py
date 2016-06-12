# encoding: utf-8
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

from django.db.models import IntegerField, FloatField, Model, BooleanField


# 按月交易
class Trading(Model):
    cid = IntegerField(primary_key=True)
    amount = FloatField(help_text=u'交易额,正盈负亏')
    balance = FloatField(help_text=u'截至上月最后一天各账户总余额')
    ATMCnt = IntegerField(help_text=u'ATM交易次数')
    ATMAmt = FloatField(help_text=u'ATM交易额')
    netbankCnt = IntegerField(help_text=u'网上银行次数')
    netbankAmt = FloatField(help_text=u'网上银行额')
    counterCnt = IntegerField(help_text=u'柜台交易次数')
    counterAmt = FloatField(help_text=u'柜台交易额')
    wechatCnt = IntegerField(help_text=u'微信交易次数')
    wechatAmt = FloatField(help_text=u'微信交易额')
    mobileCnt = IntegerField(help_text=u'手机银行交易次数')
    mobileAmt = FloatField(help_text=u'手机银行交易额')
    RMBAmount = FloatField(help_text=u'人民币交易额')
    DollarAmt = FloatField(help_text=u'美元交易额')
    inAccountCnt = IntegerField(help_text=u'发生交易收入账户数')
    outAccountCnt = IntegerField(help_text=u'发生交易支出账户数')
    purchaseCnt = IntegerField(help_text=u'截至上月购买理财产品次数')
    productExpireCnt = IntegerField(help_text=u'本月理财产品到期数')