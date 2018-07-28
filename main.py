#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import difflib
import logging
import json
import os
import sys
import random
import time
import traceback

from lxml import etree
import requests

import config
from init_logger import init_logger
from mail import send_mail, add_error_log_mail_handler


logger = logging.getLogger(__name__)

system = config.mail['subject_prefix']
groups = config.groups
locations = config.locations
receive_mail_addresses = config.mail['receivers']
exclude_words = config.exclude_words

rooms_filepath = '/tmp/douban_rooms.json'


class DoubanSpider(object):

    default_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/61.0.3163.100 Safari/537.36',
    }

    search_url = 'http://www.douban.com/group/search'
    search_required_params = dict(cat=1013, sort='time')

    def get_room_url_title_list(self, group_id, query):
        params = dict(group=group_id, q=query, **self.search_required_params)
        response = requests.get(
            url=self.search_url, params=params,
            headers=self.default_headers
        )
        if response.status_code != 200:
            logger.error(
                '查询房子接口失败 url: {} rsp: {}'.format(self.search_url, response)
            )

        root = etree.HTML(response.text)
        xpath = '//table[@class="olt"]//a[@title]'
        link_nodes = root.xpath(xpath)
        for node in link_nodes:
            yield node.get('href'), node.get('title')

    def get_room_desc_div(self, url):
        response = requests.get(url=url)
        if response.status_code != 200:
            logger.error('获取房子接口失败, url: {} rsp: {}'.format(url, response))

        root = etree.HTML(response.content)
        xpath = '//div[@class="topic-content clearfix"]'
        try:
            div_element = root.xpath(xpath)[0]
            return etree.tostring(div_element).decode()
        except:
            logger.error('获取房子接口失败, url: {} rsp: {} {}'.format(url, response, traceback.format_exc()))


class Diff(object):

    def __init__(self, new_dicts):
        self.filepath = rooms_filepath
        self.old_dicts = self._load_old_items_from_disk()
        self.new_dicts = new_dicts

        self._save_items_to_disk({**self.old_dicts, **self.new_dicts})

    def get_added_items(self):
        # 第一次创建旧文件不提醒
        if not self.old_dicts:
            return
        old_titles = list(set(self.old_dicts.values()))
        added_titles = []
        for url, title in self.new_dicts.items():
            # 根据字符串相似度来选出新帖子
            if not difflib.get_close_matches(title, old_titles + added_titles, cutoff=0.6):
                added_titles.append(title)
                yield url, title

    def _load_old_items_from_disk(self):
        if not os.path.isfile(self.filepath):
            return {}
        return json.load(open(self.filepath))

    def _save_items_to_disk(self, new_dicts):
        f = open(self.filepath, 'w')
        f.write(json.dumps(new_dicts, indent=4, ensure_ascii=False))
        f.flush()
        f.close()


def get_all_group_rooms():
    for group_id, group_name in groups:
        for location in locations:
            logger.info('获取豆瓣小组:{} with 地点 {}'.format(group_name, location))
            room_list = DoubanSpider().get_room_url_title_list(group_id, location)
            for url, title in room_list:
                if not any([x in title for x in exclude_words]):
                    yield url, title
            time.sleep(random.randint(10, 30))


def get_new_rooms():
    rooms_dict = dict(get_all_group_rooms())
    added_rooms = Diff(rooms_dict).get_added_items()
    return added_rooms


def send_room_mail(room_url, room_title):
    room_desc_div = DoubanSpider().get_room_desc_div(room_url)
    content = '''
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    </head>
    <body>
        <a href="{url}">原文链接</a>
        {div}
    </body>
</html>
'''.format(url=room_url, div=room_desc_div)
    
    send_mail(
        to=receive_mail_addresses,
        subject=room_title,
        content=content,
        type='html',
        system=system
    )


def monitor_rooms():
    while True:
        new_rooms = get_new_rooms()
        for url, title in new_rooms:
            send_room_mail(url, title)
            time.sleep(5)
        time.sleep(60 * random.randint(10, 30))


if __name__ == '__main__':

    add_error_log_mail_handler(logger, system)

    try:
        monitor_rooms()
    except:
        logger.error('程序异常终止', traceback.format_exc())
