#!/usr/bin/env python
# -*- coding:utf-8 -*-
import happybase
import sys


def hbase_query(sid, sdate='19010101', edate='20161231'):
    '''
    HBase查询，主要是针对中行对私查询的场景
    HBase表的rowKey组成形式为<fd_id_no_new>_<dtbl_txn_date>_<timestamp>
    列族名为0,列为之前查询的返回字段
    '''
    # HBase Thrift server to connect to. Leave blank for localhost
    if sys.platform == 'darwin':
        hbase_server = '192.168.1.221'
    else:
        hbase_server = 'bdt3.boc.cn'

    columns_list = ["fd_id_no_new", "fd_cus_name", "dtbl_act_no", "fd_new_no", "dtbl_txn_date", "dtbl_proc_seq",
                    "dtbl_cuu_code", "dtbl_txn_sdn", "dtbl_txn_trm", "dtbl_txn_code", "dtbl_db_cr", "dtbl_txn_amt",
                    "dtbl_new_bal"]
    names = u"证件号,姓名,旧线交易账号,对应新线账号,交易日期,交易序号,交易货币,交易网点号,交易终端,交易代码,借贷别,交易金额,账户余额"
    # Connect to server
    c = happybase.Connection(hbase_server)

    # Get the full list of tables
    # tables = c.tables()

    # 指定要查询的表名
    t = c.table('his_data')

    print sid
    print sdate
    print edate
    # For each row key
    res = []
    # 如果没有指定任何查询条件，那么查询所有身份证4301开头的前1000行
    # 否则查询特定时间段（如果没有指定，则用默认值）的前1000条记录
    if sid.strip() == '':
        hres = t.scan(row_prefix='4301', limit=200)
    else:
        b_rowkey = "%s_%s" % (sid, sdate)
        e_rowkey = "%s_%s" % (sid, edate)
        print '%s^^^^^%s' % (b_rowkey, e_rowkey)
        hres = t.scan(row_start=b_rowkey, row_stop=e_rowkey, limit=200)
    for key, data in hres:
        # 讲rowkey还原，形成fd_id_no_new和dtbl_txn_date两个字段
        # 以后rowkey只当做查询条件，不再当做字段使用。
        # ssid,cdate,tmp = key.split("_")
        # d = {"rowkey":key}

        d = {}
        # d['fd_id_no_new'] = ssid
        for col in columns_list:
            d[col] = data.get(u"info:%s" % col, sid)

        # d['dtbl_txn_date'] = cdate
        # 名字和账户余额可能是因为导入的关系，decode会报错，需要更改
        d['fd_cus_name'] = d['fd_cus_name'].decode('utf-8')


        try:
            d['dtbl_new_bal'] = float(d['dtbl_new_bal'])
        except Exception, err:
            d['dtbl_new_bal'] = 0.0
        # d['dtbl_new_bal']=d['dtbl_new_bal'].decode('utf-8')
        res.append(d)


    return res

# 430321620311351
if __name__ == '__main__':
    print hbase_query(sid='$430426681209004', sdate='20020101', edate='20021001')
