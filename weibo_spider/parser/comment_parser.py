import logging
import random
from time import sleep

from .parser import Parser
from .util import handle_garbled, handle_html

logger = logging.getLogger('spider.comment_parser')


class CommentParser(Parser):
    def __init__(self, cookie, weibo_id):
        self.cookie = cookie
        self.url = 'https://weibo.cn/comment/' + weibo_id
        self.selector = handle_html(self.cookie, self.url)

    def get_long_weibo(self):
        """获取长原创微博"""
        try:
            for i in range(5):
                self.selector = handle_html(self.cookie, self.url)
                if self.selector is not None:
                    info = self.selector.xpath("//div[@class='c']")[1]
                    wb_content = handle_garbled(info)
                    wb_time = info.xpath("//span[@class='ct']/text()")[0]
                    weibo_content = wb_content[wb_content.find(':') +
                                               1:wb_content.rfind(wb_time)]
                    if weibo_content is not None:
                        return weibo_content
                sleep(random.randint(6, 10))
        except Exception:
            logger.exception(u'网络出错')
            return u'网络出错'

    def get_long_retweet(self):
        """获取长转发微博"""
        try:
            wb_content = self.get_long_weibo()
            weibo_content = wb_content[:wb_content.rfind(u'原文转发')]
            return weibo_content
        except Exception as e:
            logger.exception(e)

    def get_comments(self, is_original):
        """获取某个微博的评论"""
        comments = []
        try:
            self.selector = handle_html(self.cookie, self.url)
            if self.selector is not None:
                if is_original:
                    for c in self.selector.xpath("//div[@class='c']")[3:-2]:
                        comment = ''

                        # 发评论的用户
                        c_a = c.xpath(".//a")[0]

                        # 评论内容（可能是回复别人的评论）
                        c_span_list = c.xpath(".//span[@class='ctt']")
                        c_span_text = c.xpath(".//span[@class='ctt']/text()")

                        # 评论的赞
                        c_cc_list = c.xpath(".//span[@class='cc']")
                        c_cc_text = c_cc_list[0].xpath(".//a")[0].text if len(c_cc_list) else ""

                        if len(c_span_text) == 2 and c_span_text[0] == '回复':
                            # 回复别人的评论
                            if len(c_span_list):
                                c_span_a = c_span_list[0].xpath(".//a")[0]

                            comment = '[用户] ' + c_a.text + ' [' + c_span_text[0] + '了用户] ' + c_span_a.text[
                                                                                             1:-1] + ', 回复内容为: ' + \
                                      c_span_text[1] + ' ' + c_cc_text
                        elif len(c_span_text) == 1:
                            # 直接评论
                            comment = '[用户] ' + c_a.text + ' 评论到： ' + c_span_text[0] + ' ' + c_cc_text

                        comments.append(comment)
            return comments

        except Exception as e:
            logger.exception(e)
