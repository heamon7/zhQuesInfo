# -*- coding: utf-8 -*-

# Scrapy settings for zhQuesInfo project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'zhQuesInfo'

SPIDER_MODULES = ['zhQuesInfo.spiders']
NEWSPIDER_MODULE = 'zhQuesInfo.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'zhQuesInfo (+http://www.yourdomain.com)'

# APP_ID_S = '8scc82ncveedyt6p8ilcz2auzoahzvpu2y800m5075f9flp9'
# MASTER_KEY_S = '06vseo6z44ummz0fgv0u6no7vnzqr4fbob0y2mxz6cv47p92'
APP_NAME = 'zhQuesInfo4'
APP_ID = 'jtr6r6qumh71o20btpgpldxfhyxhsireb4vmne7tzh87ln3a'
MASTER_KEY = 'zq38zjgdz98riq6fq46hqb7xdq0d9j425oxq5rd0ztt0bby3'

#
# CACHE_SERVER_1 = 'aa41ddf13b914084.m.cnbjalinu16pub001.ocs.aliyuncs.com:11211'
# CACHE_USER_1 = 'aa41ddf13b914084'
# CACHE_PASSWORD_1 = 'Zhihu7771'
#
# CACHE_SERVER_2 = 'b2954ece3d1647b8.m.cnbjalinu16pub001.ocs.aliyuncs.com:11211'
# CACHE_USER_2 = 'b2954ece3d1647b8'
# CACHE_PASSWORD_2 = 'Zhihu7772'
#
# CACHE_SERVER_3 = '73670ac267c941e6.m.cnbjalinu16pub001.ocs.aliyuncs.com:11211'
# CACHE_USER_3 = '73670ac267c941e6'
# CACHE_PASSWORD_3 = 'Zhihu7773'


REDIS_HOST = 'f57567e905c811e5.m.cnbja.kvstore.aliyuncs.com'
REDIS_PORT = '6379'
REDIS_USER = 'f57567e905c811e5'
REDIS_PASSWORD = 'Zhihu777r'

HBASE_HOST='localhost'

DOWNLOAD_TIMEOUT = 700

CONCURRENT_REQUESTS = 70
CONCURRENT_REQUESTS_PER_DOMAIN = 70

LOG_LEVEL = 'INFO'
ITEM_PIPELINES = {
    'zhQuesInfo.pipelines.QuesInfoPipeline': 300,
   # 'zhihut.pipelines.SecondPipline': 800,
}

DEFAULT_REQUEST_HEADERS = {
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, sdch',
           'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-TW;q=0.2',
           'Connection': 'keep-alive',
           'Host': 'www.zhihu.com',
           'Referer': 'http://www.zhihu.com/',

}

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36'

SPIDER_MIDDDLEWARES = {
    'scrapy.contrib.spidermiddleware.httperror.HttpErrorMiddleware':300,
}

DUPEFILTER_CLASS = 'zhQuesInfo.custom_filters.SeenURLFilter'


#AJAXCRAWL_ENABLED = True
