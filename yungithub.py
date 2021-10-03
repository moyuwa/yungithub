#!/usr/bin/env python
# coding=utf-8
# python version 3.7
# 使用github api 监控 关键字 动态


import time, logging
import requests

# requests.packages.urllib3.disable_warnings()
#
# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s %(levelname)s %(module)s/%(funcName)s:%(message)s',
#                     datefmt='%Y-%m-%d-%X',
#                     # filename=os.getcwd() + '/mp_main.log',
#                     # filemode='a'
#                     )
zzzq = ["大陆", "中共", "谋杀", "黑产", "博彩", "毒", "赌", "色情", ]


class mpgithub():
    def __init__(self, qkeys=[]):
        self._session = requests.session()
        self._get_sleep = 1  # 未经身份验证的请求，速率限制使您每分钟最多可以进行10个请求
        self._qkeys = qkeys

    # 自定义邮件内容
    def mail_text(self, k, _news=[]):
        print("{} to mailtext count: {}".format(k, len(_news)))
        # mailtext = u'%sGitHub%s\n' % ('=' * 3, '=' * 3)
        mailtext = u'<h1>{}</h1><ul>'.format(k)
        for tmps_ in _news:
            # tmps_ = eval(n)
            if len(tmps_['description']) > 1024:
                tmps_['description'] = tmps_['description'][0:1024]
            madd = True
            for zz in zzzq:
                if zz in tmps_['description']:  # 测试时发现有些zz敏感的东西，过滤一下
                    madd = False
                    break
            if madd:
                mailtext += u"<li>{},<a href='{}'>{}</a>,{}</li>".format(
                    # tmps_['language'],
                    # tmps_['stargazers_count'],
                    tmps_['updated_at'],
                    tmps_['html_url'],
                    tmps_['full_name'],
                    tmps_['description'])
        mailtext += "</ul>"
        return mailtext

    def run(self):
        mail_list = ""
        for k in self._qkeys:
            time.sleep(self._get_sleep)
            _list = self.get_github_control(k)
            mail_list += self.mail_text(k, _list)
        return mail_list

    def get_github_control(self, qkey=''):
        print("get_github_control serach: " + qkey)
        github_search_appi = 'https://api.github.com/search/repositories?q='
        gurl = github_search_appi + '%s&sort=updated&order=desc&page=%d&per_page=50' % (
            qkey, 1)  # 搜索存储库每页最多返回100个结果
        _list = self.get_github_page(gurl)
        return _list

    # 从api返回的json中提取指定元素
    def get_github_page(self, gurl):
        _gjson = self._session.get(gurl, verify=False, timeout=(5, 10)).json()  # 获取返回的json字符串
        _list = []  # 提取json信息
        _items = _gjson['items']
        for g in _items:
            tmps_ = {}
            # 取出需要的参数值，重新构造字典
            # tmps_['node_id'] = g['node_id']
            tmps_['full_name'] = g['full_name']
            tmps_['html_url'] = g['html_url']
            tmps_['description'] = str(g['description']).replace('\"', '').replace('\'', '')
            tmps_['created_at'] = g['created_at']
            tmps_['updated_at'] = g['updated_at']
            tmps_['stargazers_count'] = g['stargazers_count']
            tmps_['language'] = g['language']
            _list.append(tmps_)
        return _list


if __name__ == '__main__':
    try:
        _f = mpgithub(['cve-20'])
        print(_f.run())
    except Exception as e:
        print(e)
