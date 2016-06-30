#!/usr/bin/env python
# encoding: utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

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
from os.path import abspath, split, join
import strategy


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
    username = deal[deal.idno == int(userid)].head(1).name.values[0]

    m = deal[deal.idno == int(userid)].groupby('ct').apply(lambda x: pd.Series({
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
        attr_names, attr_weights, max_attr_pie = strategy.deals_pca(users, 50000)
        print '------------------------ %s' % str(attr_names)
        context = {
            'pname': m[m.pcode == pcode].pname.values[0],
            'user_infos': users[users.bal + users.bal_std >= 50000].to_dict('record'),
            'attr_names': attr_names,
            'attr_weights': json.dumps(attr_weights),
            'max_attr_pie': max_attr_pie,
            'max_attr': attr_names[0],
            'max_attr_w': attr_weights[0],
            'user_percent': 100*round(len(users[users.apply(lambda x: x['bal']+x['bal_std'] >= 50000, axis=1)])/float(len(users)), 3)
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
