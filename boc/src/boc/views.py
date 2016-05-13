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

from desktop.lib.django_util import render as grender
from django.shortcuts import render
from models import *
from django.http import HttpResponse, Http404
#from impala.dbapi import connect
from django.views.decorators.csrf import csrf_exempt
import time, os, sys, json, datetime
import pandas as pd
#from hbase_query import hbase_query


# conn = connect('192.168.1.222', port=10000, auth_mechanism='PLAIN', user='hive')
# c = conn.cursor()

def index(request):
    return grender('index.mako', request, dict(date=datetime.datetime.now()))


def management(request):
    return grender('management.mako', request, dict(date=datetime.datetime.now()))


def query(request, query_subcate_id):
    # if a == -1: a=1 else: a=a
    query_subcate_id = (query_subcate_id == -1 and 1 or query_subcate_id)

    # get all sub cates
    cates_stack = [(i.name, [(j.name, j.id) for j in i.querysubcate_cate.all()]) for i in QueryCate.objects.all()]
    try:
        current_query = QuerySubCate.objects.get(pk=query_subcate_id)
    except QuerySubCate.DoesNotExist:
        raise Http404("No id = %s matches the given query" % query_subcate_id)
    conditions = json.loads(current_query.condition_types).items()

    context = {
        'cates_stack': cates_stack,
        'current_cate_id': query_subcate_id,
        'current_cate_name': current_query.name,
        'conditions': conditions,
    }

    return render(request, 'index.html', context)


@csrf_exempt
def get_hive(request):
    fd_id_no_new = request.POST.get('a.fd_id_no_new', "")
    # fd_cus_name = request.POST.get('a.fd_cus_name', "")
    date_begin = '19010101' #request.POST.get('date_begin', "19010101").replace('-', '')
    date_end = '20161231' #request.POST.get('date_end', time.strftime('%Y%m%d')).replace('-', '')
    print '!!!!!!!!!!!!!!!!! %s' % date_begin
    print '!!!!!!!!!!!!!!!!! %s' % date_end

    # fd_new_no = request.POST.get('c.fd_new_no', None)
    # dtbl_act_no = request.POST.get('t.dtbl_act_no', None)
    # dtbl_proc_seq = request.POST.get('t.dtbl_proc_seq', None)
    # fd_id_no_new_like = request.POST.get('a.fd_id_no_new_like', None)
    # fd_cus_name_like = request.POST.get('a.fd_cus_name_like', None)
    # fd_new_no_like = request.POST.get('c.fd_new_no_like', None)
    # dtbl_act_no_like = request.POST.get('t.dtbl_act_no_like', None)
    # dtbl_proc_seq_like = request.POST.get('t.dtbl_proc_seq_like', None)


    # print params
    # res = sqlparse.parse(s.lower())
    # kv = []
    # for token in filter(lambda x: type(x) == sqlparse.sql.Where, res[0].tokens):
    #     kv.extend(re.findall('([^\s]+)\s*=\s*([^\s]+)', token.value))
    def like_producer(x):
        if x[2] == 'true':
            return "%s like '%%%s%%'" % (x[0], x[1])
        else:
            return "%s='%s'" % (x[0], x[1])

    #
    bt = time.time()

    res = hbase_query(fd_id_no_new.strip(), sdate=date_begin, edate=date_end)

    et = time.time()

    print "query estime %f " % (et - bt)

    # names: 导出到excel中的header,一共13列,但是我看你下午给我看的res输出中,只有12列,你看下,要对应起来
    names = u"证件号,姓名,旧线交易账号,对应新线账号,交易日期,交易序号,交易货币,交易网点号,交易终端,交易代码,借贷别,交易金额,账户余额"
    # names = u"证件号,姓名,旧线交易账号,对应新线账号,交易序号,交易货币,交易网点号,交易终端,交易代码,借贷别,交易金额,账户余额,交易日期"
    # names = u"交易网点号,对应新线账号,交易终端,交易货币,交易序号,交易日期,旧线交易账号,账户余额,证件号,交易代码,借贷别,姓名,交易金额"
    columns_list = ["fd_id_no_new", "fd_cus_name", "dtbl_act_no", "fd_new_no", "dtbl_txn_date", "dtbl_proc_seq",
                    "dtbl_cuu_code", "dtbl_txn_sdn", "dtbl_txn_trm", "dtbl_txn_code", "dtbl_db_cr", "dtbl_txn_amt",
                    "dtbl_new_bal"]

    # 文件名使用timestamp
    filename = 'his_%s.xlsx' % int(time.time())
    # 如果是下午你给我看的那个Demo形式的返回: [{"dtbl_txn_sdn": "4680002", "fd_new_no": "00000580752282158", "dtbl_txn_trm": "02", "dtbl_db_cr": "C", "dtbl_cuu_code": "01", "dtbl_proc_seq": "00081768", "dtbl_act_no": "4680002010100009837900", "dtbl_new_bal": "732.0\n", "dtbl_txn_code": "1002", "rowkey": "439999999990008834_20000927_1454391008", "fd_cus_name": "\u82cf\u4ef2\u6c11\u3000\u3000", "dtbl_txn_amt": "732.0"}, {"dtbl_txn_sdn": "4701512", "fd_new_no": "00000580752282158", "dtbl_txn_trm": "01", "dtbl_db_cr": "D", "dtbl_cuu_code": "01", "dtbl_proc_seq": "00014386", "dtbl_act_no": "4680002010100009837900", "dtbl_new_bal": "232.0\n", "dtbl_txn_code": "1200", "rowkey": "439999999990008834_20001115_1454391008", "fd_cus_name": "\u82cf\u4ef2\u6c11\u3000\u3000", "dtbl_txn_amt": "500.0"}]
    # 就这可这样初始化DataFrame,且header已经写明,但是为了输出到excel的header中显示中文,可以使用m.columns替换
    m = pd.DataFrame(res)
    # 替换header
    # m.columns = names.split(',')
    col_chinese = {'dtbl_txn_sdn': u'交易网点号', 'fd_new_no': u'对应新线账号', 'dtbl_txn_trm': u'交易终端',
                   'dtbl_cuu_code': u'交易货币', 'dtbl_proc_seq': u'交易序号', 'dtbl_txn_date': u'交易日期',
                   'dtbl_act_no': u'旧线交易账号', 'dtbl_new_bal': u'账户余额', 'fd_id_no_new': u'证件号',
                   'dtbl_txn_code': u'交易代码', 'dtbl_db_cr': u'借贷别', 'fd_cus_name': u'姓名',
                   'dtbl_txn_amt': u'交易金额'}
    try:
        col_ordered = sorted(res[0].keys())
        true_col = []
        for c in col_ordered:
            true_col.append(col_chinese[c])
        m.columns = true_col
        # 初始化excel文件, 保存在项目根目录下的 boc/static
        w = pd.ExcelWriter(os.path.join('boc/static/%s' % filename))
        # 写入
        m.to_excel(w, index=False)
        w.save()
    except Exception, err:
        pass
    # 返回文件名
    print "write excel task time %f" % (time.time() - et)
    return HttpResponse(json.dumps({'data': res,'excel_id': filename}), content_type='application/json' )
    # return HttpResponse( "{'data': %s }" % res,mimetype='application/json')
