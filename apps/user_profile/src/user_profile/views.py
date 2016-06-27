#!/usr/bin/env python
# encoding: utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf8')
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

from django.shortcuts import render
from city import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from happybase import Connection, ConnectionPool
from collections import Counter
import random
import itertools
import pandas as pd
import numpy as np
from django.shortcuts import render_to_response
from desktop.lib.django_util import render
import datetime, json
from os.path import (abspath, split, join)

idtags = ['84629', '159968', '125276', '74060', '182696', '83387', '220097', '161372', '226048', '225945', '165289',
          '200932', '69819', '157521', '49095', '112197', '179285', '44127', '160487', '127470', '37595', '198220',
          '146841', '181243', '76342', '169645', '155555', '54329', '133093', '12704', '171872', '222049', '20368',
          '104444', '156604', '198953', '195739', '30519', '176936', '55222', '167404', '120727', '149562', '102182',
          '92112', '64519', '142435', '30670', '25284', '169549', '81399', '80594', '80619', '108577', '37989', '88021',
          '87141', '69081', '187789', '111020', '81628', '24049', '179468', '124672', '34505', '95410', '123967',
          '171608', '185251', '190431', '64290', '169066', '192856', '52523', '21613', '176384', '225337', '212356',
          '2041', '161151', '167519', '5571', '141438', '166740', '191196', '111976', '148392', '219679', '213756',
          '131830', '122040', '160315', '56409', '72589', '96578', '225906', '225908', '127522', '98989', '189783',
          '115996', '12447', '21684', '52728', '12443', '82407', '122699', '167460', '45205', '89157', '12335',
          '124873', '61248', '122547', '80878', '137161', '177289', '44542', '19336', '84827', '92326', '200849',
          '10565', '186660', '14141', '81862', '78889', '171454', '195677', '140506', '120769', '166442', '206749',
          '37319', '170488', '168648', '40112', '225574', '164341', '39550', '52356', '40365', '67196', '17944',
          '79393', '239', '141341', '17823', '139810', '210033', '218654', '201260', '159051', '183708', '104186',
          '93405', '153112', '154326', '142503', '104619', '212988', '153297', '168514', '18024', '15565', '185545',
          '61196', '2123', '113038', '189855', '113036', '136599', '220473', '157406', '81879', '106488', '77973',
          '104114', '166706', '77976', '191675', '89544', '73658', '168271', '128004', '197556', '130505', '127395',
          '75157', '21270', '34491', '29561', '198595', '111730', '109218', '67970', '121510', '63798', '44720',
          '87773', '15293', '136931', '135488', '186539', '221279', '141158', '6241', '219529', '134056', '117705',
          '55620', '190284', '214798', '43347', '88314', '197522', '159381', '225898', '180287', '61591', '106060',
          '210925', '133492', '175451', '204434', '73155', '3844', '194942', '133653', '206413', '5334', '177374',
          '41647', '77766', '112169', '56592', '74797', '1483', '92884', '113969', '53312', '155918', '20193', '175359',
          '166247', '55225', '83381', '56502', '176258', '157190', '147147', '26697', '19841', '63997', '64501',
          '40210', '72070', '168559', '224921', '58561', '3918', '61786', '42438', '64986', '77629', '119523', '172804',
          '124669', '171297', '56345', '120131', '128467', '144610', '167509', '211718', '164710', '126229', '39851',
          '169275', '200070', '31986', '120545', '93852', '185578', '224580', '86086', '172112', '154929', '221238',
          '133871', '39301', '217347', '182972', '42488', '162434', '28316', '102321', '61397', '193845', '158051',
          '206580', '64335', '49251', '10395', '191623', '76145', '80361', '208265', '113397', '82149', '90880',
          '93770', '203773', '25913', '31388', '184878', '207983', '2029', '225828', '196066', '189033', '74530',
          '155683', '19084', '200910', '188036', '86262', '186058', '185610', '4161', '182123', '214879', '110930',
          '224564', '77978', '103931', '136573', '168913', '60970', '115034', '200359', '93093', '208161', '116805',
          '65709', '62624', '110239', '171856', '138970', '7667', '95110', '192198', '11796', '204760', '96071',
          '83216', '121175', '69012', '93444', '163973', '120201', '21647', '140781', '124371', '184290', '46626',
          '42680', '54112', '161588', '173751', '176135', '45236', '74146', '144620', '24255', '61875', '28420',
          '156129', '11460', '225142', '944', '122631', '45229', '110799', '222633', '37503', '80949', '100462', '5755',
          '52549', '149009', '89414', '176008', '15197', '61901', '92520', '138537', '97554', '10614', '177518',
          '136927', '167022', '129928', '85411', '188074', '38932', '45761', '189175', '23468', '87993', '191178',
          '217691', '70410', '21469', '13868', '109177', '137518', '55748', '26535', '110099', '224138', '130966',
          '28124', '102605', '65005', '223999', '16129', '84516', '215997', '153776', '133500', '198600', '66445',
          '81512', '92932', '182720', '21512', '115903', '149545', '142494', '87390', '115755', '33300', '22096',
          '55631', '168566', '181135', '78562', '142552', '60529', '54852', '222237', '123885', '183196', '4634',
          '7793', '198917', '26988', '143157', '45249', '27515', '122202', '18755', '178069', '738', '72226', '79562',
          '27509', '69129', '93869', '212803', '37204', '206187', '3722', '209901', '49840', '134231', '180726',
          '180722', '154955', '166826', '216541', '139188', '41281', '50469', '96950', '111594', '14014', '13185',
          '182048', '46683', '26515', '66598', '77252', '118950', '92366', '184230', '39209', '117919', '105600',
          '213069', '113127', '12219', '167407', '55175', '120348', '196659', '192790', '168618', '55212', '41065',
          '126263', '180354', '56485', '196106', '111525', '126960', '69044', '162517', '127866', '74672', '171693',
          '138366', '41803', '151810', '49800', '78464', '36077', '3989', '350', '213462', '65132', '15722', '12921',
          '10815', '71074', '32709', '124165', '150064', '120440', '191448', '114661', '80735', '179605', '59642',
          '194504', '129430', '115765', '192936', '195728', '149677', '172918', '58002', '189802', '137845', '64712',
          '200538', '18804', '137333', '56742', '72157', '8142', '140799', '173723', '42691', '61989', '186863',
          '123104', '186869', '161675', '168766', '174054', '42365', '11103', '14748', '90521', '109906', '166868',
          '184637', '55951', '76173', '166865', '111499', '135459', '67943', '4893', '5152', '163987', '129867',
          '217107', '188363', '134406', '169312', '109882', '167633', '12426', '17144', '7312', '190302', '4419',
          '82851', '84138', '198621', '143400', '125605', '38272', '62821', '224190', '94431', '99055', '19149',
          '103917', '31086', '187934', '3264', '190223', '160305', '200657', '194085', '212942', '113219', '7265',
          '128518', '217217', '50507', '89105', '214456', '71813', '19748', '158284', '142738', '159688', '129167',
          '166515', '166699', '72277', '130306', '128844', '67003', '107489', '172897', '98755', '86320', '130780',
          '214425', '82095', '13042', '18910', '45201', '56667', '202622', '143246', '136774', '63606', '25386',
          '177074', '149288', '121872', '204707', '225115', '124829', '56200', '98728', '93573', '67528', '165259',
          '52511', '125797', '4249', '97078', '119188', '66514', '187891', '165793', '63786', '110821', '25847',
          '186597', '210647', '125897', '199099', '137488', '28294', '127679', '5165', '125577', '126376', '48638',
          '114559', '97409', '63809', '191161', '17176', '9212', '100682', '159526', '75242', '121288', '219346',
          '116270', '208362', '31376', '193062', '155123', '105613', '102482', '189729', '204513', '167412', '225706']
# conn = Connection('192.168.2.41')
pool = ConnectionPool(size=5, host='192.168.2.41')
'''
user_t = conn.table('haodou')
keys_t = conn.table('tag_search_keys')
id2tokens_t = conn.table('id2tokens') #id-标签对应表
favs_t = conn.table('favs_by_time') #key: time, column: token, value: [w1, w2, w3, ...]
user_tags_t = conn.table('haodou_user_tags') # 用户标签库
goods_t = conn.table('haodou_goods')
td_w_t = conn.table('td_w') # tag_date_weight
ud_w_t = conn.table('ud_w') # user_date_weight
'''

current_tag = ''
country_index = [u'中国', u'加拿大', u'美国', u'日本', u'澳大利亚']

token2tag = {
    u'人民币': 'code_01',
    u'存入': 'cr_C',
    u'取出': 'cr_D',
    u'高频': 'freq',
    u'中频': 'freq',
    u'低频': 'freq',
    u'大额': 'big_trading',
    u'中额': 'mid_trading',
    u'小额': 'light_trading',
    u'ATM交易': 'trm_02',
    u'网上交易': 'trm_01'
}
tag2token = { v:k for k,v in token2tag.items() }

def index(request):
    return render('tag_search.mako', request, dict(date=datetime.datetime.now()))


def tag_search(request):
    return render('tag_search.mako', request, dict(date=datetime.datetime.now()))


def tag_heat(request):
    return render('tag_heat.mako', request, dict(date=datetime.datetime.now()))


def relationship(request):
    return render('relationship.mako', request, dict(date=datetime.datetime.now()))


def user_detail(request):
    global current_tag
    userid = request.GET.get("userid", '-1')
    with pool.connection() as conn:
        ud_w_t = conn.table('ud_w')
        u = { k.split('_')[1]:v for k,v in ud_w_t.scan(row_prefix=userid) }

    # res = [ i for i in id2tokens_t.scan(row_start='10000', row_stop='11100') if i[0] in idtags ]
    # goods = [ i[1] for i in goods_t.scan() ]
    # tags = map(lambda x: random.choice(res)[1]['word:'], range(20))
    # fit_goods = map(lambda x: { k.split(':')[1]:v for k,v in random.choice(goods).items() }, range(6))

    finical_map = {
        'counter': u'柜面',
        'kxt': u'快信通',
        'mobile': u'手机银行',
        'netbank': u'网银',
        'wechat': u'微信'
    }
    fit_goods = pd.read_csv(join(split(abspath(__file__))[0], 'finical.csv'), sep='\t')
    fit_goods['ternimal'] = fit_goods[['mobile', 'wechat', 'counter', 'kxt', 'netbank']].apply(lambda x: ','.join([ v for k,v in finical_map.items() if x.get(k, 0)==1 ]), axis=1 )
    user_info = pd.read_csv(join(split(abspath(__file__))[0], 'user_info'))
    rand_user = random.choice(user_info.to_dict('record'))

    current_tags = [ i.decode('utf8') for i in current_tag.split(',')]

    tags = current_tags + list(set(token2tag.keys())-set(current_tags))[-2:]

    context = {
        'username': rand_user.get('names', '王小二'),
        'email': rand_user.get('email', 'wangxiaoer@163.com'),
        'phone': rand_user.get('phone', '18983747246'),
        'last_login': rand_user.get('regtime', '2015-03-01'),
        'reg_time': rand_user.get('lasttime', '2008-01-03'),
        'tags': tags, #list(np.random.choice(token2tag.keys(), 3)), #[u'高频', u'人民币', u'小额']
        'fit_goods': fit_goods.sample(random.randint(1,4)).to_dict('record')
    }
    return render_to_response('user_profile/user_detail.html', context)


@csrf_exempt
def les_miserables(request):
    return HttpResponse(content=open(join(split(abspath(__file__))[0], 'les-miserables1.gexf')).read(), content_type="xml")


@csrf_exempt
def city_service(request):
    key, value = int(request.POST.get('key', -1)), request.POST.get('value', '')
    if key == 0 and value == u'中国':  # country == china
        return HttpResponse(json.dumps({'provinces': PROVINCE_DICT.values()}), content_type='application/json')
    elif key == 1:  # province
        return HttpResponse(json.dumps({'cities': CITY.get(value.encode('utf8'), {})}), content_type='application/json')
    return HttpResponse(json.dumps({'error': 'GG'}), content_type='application/json')


@csrf_exempt
def tag_query(request):
    include_tags = request.POST.get('include_tags')
    exclude_tags = request.POST.get('exclude_tags')

    global current_tag
    current_tag = include_tags
    # tags = user_tags_t.row('%s_2016-03-03' % include_tags.split(',')[0], ['tags:weight'])
    with pool.connection() as conn:
        td_w_t = conn.table('td_w')
        tags = td_w_t.row('%s_20110530' % token2tag[include_tags.split(',')[0]], ['deal'])
    pdf = pd.DataFrame([ (k.split(':')[1], float(v)) for k,v in tags.items() ], columns=['userid', 'v'])
    mins, maxs = pdf.v.min(), pdf.v.max()
    pdf['tag_value'] = pdf.v.apply(lambda x: '{0:.2f}%'.format((x-mins)/maxs*100) )

    return HttpResponse(json.dumps({
        # 'data': [ {'userid': i[1], 'tag_value': i[2] } for i in json.loads(tags['tags:weight']) ]
        'data': pdf[['userid', 'tag_value']][~pdf.tag_value.str.contains('0.00%')].sort_values(by='tag_value', ascending=False).to_dict('record')
    }), content_type='application/json')


@csrf_exempt
def include_tags_search(request):
    key = request.POST.get('word', '')
    with pool.connection() as conn:
        keys_t = conn.table('tag_search_keys')
        ret = [v['key:'] for k, v in keys_t.scan(row_prefix=key.encode("utf8"), limit=10)]
    print ' '.join(ret)
    return HttpResponse(json.dumps({'data': ret}), content_type='application/json')


@csrf_exempt
def user_financial_status(request):
    userid = request.POST.get('userid', -1)

    deal = pd.read_csv(join(split(abspath(__file__))[0], 'deal.csv'), sep=',')
    username = deal[deal.idno==int(userid)].head(1).name.values[0]

    m = deal[deal.idno==int(userid)].groupby('ct').apply(lambda x: pd.Series({
                'deal_cnt': len(x),
                'deal_sum': x.bal.sum()
        })).sort_index().tail(10).reset_index()

    if len(m) > 0:
        mlist = m.to_dict('list')

        return HttpResponse(json.dumps({
            'name': username,
            'status': u'资金流出趋势',
            'idno': userid,
            'date_series': mlist['ct'],
            'cnt_series': [ round(i, 1) for i in mlist['deal_cnt'] ],
            'sum_series': [ round(i, 2) for i in mlist['deal_sum'] ],
            'cnt_mean': round(np.array(mlist['deal_cnt']).mean(), 1),
            'cnt_std': round(np.array(mlist['deal_cnt']).std(), 1),
            'sum_mean': round(np.array(mlist['deal_sum']).mean(), 1),
            'sum_std': round(np.array(mlist['deal_sum']).std(), 1),
            'cnt_max': max(mlist['deal_cnt']),
            'sum_max': max(mlist['deal_sum']),
        }), content_type='application/json')
    else:
        return HttpResponse(json.dumps({}), content_type='application/json')


@csrf_exempt
def financial(request, pcode=None):
    finical_map = {
        'counter': u'柜面',
        'kxt': u'快信通',
        'mobile': u'手机银行',
        'netbank': u'网银',
        'wechat': u'微信'
    }
    m = pd.read_csv(join(split(abspath(__file__))[0], 'finical.csv'), sep='\t')
    m['channel'] = m[['mobile', 'wechat', 'counter', 'kxt', 'netbank']].apply(lambda x: ','.join([ v for k,v in finical_map.items() if x.get(k, 0)==1 ]), axis=1 )

    ret = m[['pcode', 'pname', 'days', 'profits', 'money', 'channel', 'risk', 'sdate', 'edate', 'intsdate', 'expdate']].to_dict('record')

    # 单个理财产品处理
    if pcode:
        users = pd.read_csv(join(split(abspath(__file__))[0], 'summary.csv'), sep=',')
        context = {
            'pname': m[m.pcode==pcode].pname.values[0],
            'user_infos': users[users.bal + users.bal_std >= 50000].to_dict('record')
        }
        return render_to_response('user_profile/finicial_detail.html', context)
    else:
        context = {
            'financial_goods': ret
        }
        return render_to_response('user_profile/hot_statis.html', context)


@csrf_exempt
def recently_hot_tags(request):
    start = request.POST.get('sdate', '2016-01-12')
    end = request.POST.get('edate', '2016-01-18')
    flag = request.POST.get('flag', 'hotbit')
    # 时间距离
    ds = [i.strftime('%Y-%m-%d') for i in pd.date_range(start, end)]
    # 每天标签点击量
    with pool.connection() as conn:
        favs_t = conn.table('favs_by_time')
        tss = [favs_t.row(i, ['token']) for i in ds]
    # 按标签点击量从大到小排序取前10, 提取出haodou_mobile.Tag中的标签
    ret = [sorted(i.items(), key=lambda x: -len(x[1]))[:10] for i in tss]
    if flag == 'hotbit':
        # 提取标签ID
        c = [[j[0].split(':')[1] for j in i] for i in ret]
        # 保留时间段中标签出现量大于2的
        lt2words = [i[0] for i in filter(lambda x: x[1] > 1, Counter(itertools.chain(*c)).items())]
        ws = [[j for j in i if j in lt2words] for i in c]
        m = pd.DataFrame([dict(zip(i, range(1, len(i) + 1))) for i in ws], index=ds).fillna(0)
        col, row = zip(*list(itertools.product(range(len(ds)), range(len(lt2words)))))
        with pool.connection() as conn:
            id2tokens_t = conn.table('id2tokens')
            words = [id2tokens_t.row(i)['word:'] for i in list(m.keys())]
        context = {
            'data': zip(col, row, np.ravel(m.astype(int))),
            'ds': ds,
            'words': words
        }
    else:
        pass
    return HttpResponse(json.dumps(context), content_type='application/json')
