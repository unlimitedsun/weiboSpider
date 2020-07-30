import copy
import logging
import sys

from .writer import Writer

logger = logging.getLogger('spider.es_writer')


class EsWriter(Writer):

    def __init__(self):

       self.index_wb_user ='weibo_user'
       self.index_wb_content = 'weibo_content'

    def _info_to_es(self, index, doc_type, info_list):
        """将爬取的信息写入MongoDB数据库"""
        try:
            import elasticsearch5
        except ImportError:
            logger.warning(
                u'系统中可能没有安装es库，请先运行 pip install elasticsearch5 ，再运行程序')
            sys.exit()
        try:
            from elasticsearch5 import Elasticsearch
            client = Elasticsearch([{'host': '10.38.167.13', 'port': 9200}], timeout=3600)
            new_info_list = copy.deepcopy(info_list)
            # 判断索引是否存在
            if client.indices.exists(index=index) is not True:
                # 创建索引
                client.indices.create(index=index)

            for info in new_info_list:

                client.index(index=index, doc_type=doc_type, body=info, id=info['id'])

        except elasticsearch5.ElasticsearchException as e:
            print(e)
            sys.exit()

    def write_weibo(self, weibos):
        """将爬取的微博信息写入ES数据库"""
        weibo_list = []
        for w in weibos:
            w.user_id = self.user.id
            weibo_list.append(w.__dict__)
        self._info_to_es(self.index_wb_content, 'weibo', weibo_list)
        logger.info(u'%d条微博写入es数据库完毕', len(weibos))

    def write_user(self, user):
        """将爬取的用户信息写入ES数据库"""
        self.user = user
        user_list = [user.__dict__]
        self._info_to_es(self.index_wb_user, 'user', user_list)
        logger.info(u'%s信息写入es数据库完毕', user.nickname)
