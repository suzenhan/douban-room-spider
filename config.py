# -*- coding: utf-8 -*-


mail = {
    'sender': 'xxx@163.com',
    'host': 'smtp.163.com',
    'receivers': ['xxx@qq.com'],
    'password': 'password',
    'subject_prefix': '豆瓣爬虫租房'
}

groups = [
    (26926, '北京租房豆瓣'),
    (279962, '北京租房（非中介）'),
    (262626, '北京无中介租房（寻天使投资）'),
    (35417, '北京租房'),
    (56297, '北京个人租房 （真房源|无中介）'),
    (257523, '北京租房房东联盟(中介勿扰) '),
]

locations = ('西二旗', '安宁庄', '小米', '上地', '龙泽', '永泰庄', '清河')

exclude_words = ('求租')
