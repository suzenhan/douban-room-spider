# douban-room-spider

豆瓣爬虫找房，支持以下功能

1. 新房源邮件提醒
2. 错误邮件报警
3. 过滤相似房源

## 安装
pip3 install -r requirement.txt

## 邮件配置

```
# config.py文件

mail = {
    'sender': 'xxx@163.com',
    'host': 'smtp.163.com',
    'receivers': ['xxx@163.com'],
    'password': 'password',
    'subject_prefix': '豆瓣爬虫租房'
}
```

## 运行
python3 main.py