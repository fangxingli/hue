# encoding: utf-8
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder


# 使用决策树分析样本属性重要性, 返回属性权重排序和max属性组成
def deals_pca(m, threshold):
    X = m[['habit', 'level', 'inout', 'freq']].copy()
    y = m.apply(lambda x: x['bal']+x['bal_std'] >= threshold, axis=1).astype('int')

    # 量化标签
    le = LabelEncoder()
    labels = {} # 保存量化标签映射
    label_map = {'habit': u'消费习惯', 'level': u'理财等级', 'inout': u'收支趋势', 'freq': u'交易频度', 'age': u'年龄段'}
    for key in ['habit', 'level', 'inout', 'freq']:
        X.loc[:, key] = le.fit_transform(X[key])
        labels[key] = le.classes_
    # 年龄量化
    X.loc[m.age.between(20, 30), 'age'] = 0
    X.loc[m.age.between(31, 40), 'age'] = 1
    X.loc[m.age.between(41, 50), 'age'] = 2
    labels['age'] = [u'20~30岁', u'31~40岁', u'41~50岁']

    clf = DecisionTreeClassifier(random_state=0, max_depth=4)
    clf.fit(X, y)
    # 获得属性影响权重排序 high->low
    sorted_weights = sorted(zip(X.keys(), clf.feature_importances_), key=lambda x: -x[1])
    sorted_label_weights = [(label_map.get(k), v) for k, v in sorted_weights]
    attr_names, attr_weights = zip(*sorted_label_weights)
    max_attr, max_weight = sorted_weights[0]
    max_attr_pie = X.loc[y == 1, max_attr].value_counts()
    return attr_names, map(lambda x: round(x, 3), attr_weights), [(labels[max_attr][k], v) for k, v in max_attr_pie.to_dict().items()]













