# douban-room-spider

豆瓣爬虫找房，支持以下功能

1. 新房源邮件提醒
2. 错误邮件报警
3. 过滤相似房源

## 安装
pip3 install -r requirement.txt

## config.py配置

```py

mail = {
    'sender': 'xxx@163.com',
    'host': 'smtp.163.com',
    'receivers': ['xxx@163.com'],
    'password': 'password',
    'subject_prefix': '豆瓣爬虫租房'
}

# 数字为小组首页的url
groups = [
    (26926, '北京租房豆瓣'),
    (279962, '北京租房（非中介）'),
    (262626, '北京无中介租房（寻天使投资）'),
    (35417, '北京租房'),
    (56297, '北京个人租房 （真房源|无中介）'),
    (257523, '北京租房房东联盟(中介勿扰) '),
]

# 要查找的地方
locations = ('西二旗', '安宁庄', '小米', '上地', '龙泽', '永泰庄', '清河')

# 按标题过滤这些帖子
exclude_words = ('求租')
```

## 运行
需要在后台一直运行，每半小时爬取一次，爬取到新房源有邮件提醒

```
nohup python3 main.py &>> /tmp/douban_spider.log
```