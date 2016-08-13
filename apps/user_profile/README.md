
## 数据处理部分
1 数据生成
2 预处理(无效数据等) 
3 量化(定量,以后提供ETL工具可配置) 
4 部分卷积计算(以后使用数据流调度工具)
5 建立数据集市(暂定使用HBase，可考虑使用{userid,timestamp}来确定一行记录，但Happybase还不支持 scan with timestamp)

## 数据可视化部分
1 整体UI设计
2 数据集市使用哪些chart展示n
3 界面实现与调试





## 思路
### 以用户为中心
#### 用户交易趋势(预测)
- 分渠道: ATM 网银 等
- 分流入流出:
- 分资金种类
- 分网点
- 分账户
#### 用户交易关系图谱

### 以产品为中心
- 对比理财产品的购买人群分类,趋势
- 每个理财产品的购买人群,趋势
### 交易总览
日(周月)交易额(分渠道)


## 使用KMeans分类, 聚为5类

## 理财产品分析模块
理财产品分析模块目前基于虚拟的客户的交易数据和理财产品数据, 其中
1. 客户交易数据在 deal.csv 中, 包括2w个交易记录
2. 理财产品数据在 summary.csv 中, 包括一共27个理财产品

模块主Views处理函数在views.financial中, 主要列出所有理财产品以及针对单个理财产品的处理
对每个理财产品点击进入后, 进入相关达标人群页面主要处理函数在views.user_financial_status中
主要推荐理财人群算法也在views.user_financial_status中,主要包括
1. 影响理财产品达标因素(现给出具体实现, 考虑使用PCA?)
2. 影响理财产品达标因素权重排序(同上)
3. 个人存款达标筛选, 两种情况: 存款已达标, 存款未达标但存款标准差+存款已达标

另外, 在客户详细列表中, 有客户近期详细交易信息, 有交易趋势, 包括
1. 消费支出渠道最多计数和总额
2. 收入渠道最多计数和总额
这两项是我考虑后加入的, 大家集思广益,各抒己见
