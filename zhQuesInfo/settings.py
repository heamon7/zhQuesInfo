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

APP_ID_S = '8scc82ncveedyt6p8ilcz2auzoahzvpu2y800m5075f9flp9'
MASTER_KEY_S = '06vseo6z44ummz0fgv0u6no7vnzqr4fbob0y2mxz6cv47p92'

APP_ID = 'ttejmt8637gjvkkynoto8tjmlaeemgqwz5z1n1vl0k7xt03t'
MASTER_KEY = '1gt3rdfqz0yomemzlke9wpyoqhi1v7z2sf1k7oy6s2tdo36y'

CACHE_SERVER_1 = 'd69c4508ccc94dc4.m.cnbjalinu16pub001.ocs.aliyuncs.com:11211'
CACHE_USER_1 = 'd69c4508ccc94dc4'
CACHE_PASSWORD_1 = 'Zhihucache1'

CACHE_SERVER_S = '7030b81da1324743.m.cnbjalinu16pub001.ocs.aliyuncs.com:11211'
CACHE_USER_S = '7030b81da1324743'
CACHE_PASSWORD_S = 'Zhihucache2'

CACHE_SERVER = '92a2b309a9f145d2.m.cnbjalinu16pub001.ocs.aliyuncs.com:11211'
CACHE_USER = '92a2b309a9f145d2'
CACHE_PASSWORD = 'Zhihucache3'

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
