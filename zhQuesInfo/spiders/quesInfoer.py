# -*- coding: utf-8 -*-
import scrapy

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request,FormRequest
from scrapy.conf import settings
from scrapy import log
from scrapy.shell import inspect_response

import bmemcached

import leancloud

from leancloud import Object
from leancloud import LeanCloudError
from leancloud import Query

from datetime import datetime
from zhQuesInfo import settings

from zhQuesInfo.items import ZhquesinfoItem
import bmemcached
import re
import redis
import requests


class QuesinfoerSpider(scrapy.Spider):
    name = "quesInfoer"
    allowed_domains = ["zhihu.com"]
    baseUrl = "http://www.zhihu.com/question/"
    start_urls = (
        'http://www.zhihu.com/',
    )
    handle_httpstatus_list = [429,502,504]
    quesIndex =0


    def __init__(self,spider_type='Master',spider_number=0,partition=1,**kwargs):
        # self.stats = stats
        #print "Initianizing ....."
        self.redis0 = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_USER+':'+settings.REDIS_PASSWORD,db=0)
        self.spider_type = str(spider_type)
        self.spider_number = int(spider_number)
        self.partition = int(partition)
        self.email= settings.EMAIL_LIST[self.spider_number]
        self.password=settings.PASSWORD_LIST[self.spider_number]

        # self.spider_number = spider_number
        # self.spider_number = spider_number
        # leancloud.init(settings.APP_ID_S, master_key=settings.MASTER_KEY_S)
        # client1 = bmemcached.Client(settings.CACHE_SERVER_1,settings.CACHE_USER_1,settings.CACHE_PASSWORD_1)
        # client2 = bmemcached.Client(settings.CACHE_SERVER_2,settings.CACHE_USER_2,settings.CACHE_PASSWORD_2)
       # redis0 = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_USER+':'+settings.REDIS_PASSWORD,db=0)

        # self.questionIdList = redis0.hvals('questionIndex')
        # questionIdListLength = len(self.questionIdList)



    # def __init__(self,spider_type='Master',spider_number=1,emailList=['heamon8@163.com'],passwordList=['heamon8@()'],**kwargs):
    #     # self.stats = stats
    #     print "Initianizing ....."
    #     scrapyd = ScrapydAPI('http://localhost:6800')
    #
    #     # leancloud.init(settings.APP_ID_S, master_key=settings.MASTER_KEY_S)
    #     # client1 = bmemcached.Client(settings.CACHE_SERVER_1,settings.CACHE_USER_1,settings.CACHE_PASSWORD_1)
    #     # client2 = bmemcached.Client(settings.CACHE_SERVER_2,settings.CACHE_USER_2,settings.CACHE_PASSWORD_2)
    #     redis0 = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_USER+':'+settings.REDIS_PASSWORD,db=0)
    #     dbPrime = 97
    #     self.email= emailList[0]
    #     self.password=passwordList[0]
    #     self.questionIdList = redis0.hvals('questionIndex')
    #     questionIdListLength = len(self.questionIdList)
    #     if spider_type=='Master':
    #         if int(spider_number)!=1:
    #             self.questionIdList = self.questionIdList[0:1*questionIdListLength/spider_number]
    #             for index in range(1,int(spider_number)):
    #                 scrapyd.schedule('zhQuesInfo', 'quesInfoer'
    #                                  , settings='JOBDIR=/tmp/scrapy/zhihu/quesInfoer'+str(index)
    #                                  ,spider_type='Slave'
    #                                  ,spider_number=index
    #                                  ,emailList=emailList[index]
    #                                  ,passwordList=passwordList[index])

        # print "totalCount: %s\n" %str(totalCount)
        # for questionIndex in range(0,totalCount+1):
        #     self.questionIdSet.add(int(client2.get(str(questionIndex))))

        # for tableIndex in range(dbPrime):
        #     if tableIndex < 10:
        #         tableIndexStr = '0' + str(tableIndex)
        #     else:
        #         tableIndexStr = str(tableIndex)

            # Question = Object.extend('Question' + tableIndexStr)
            # query = Query(Question)
            # query.exists('questionId')
            #
            # # 避免在查询时，仍然有新的Question入库
            # # curTime = datetime.now()
            # # query.less_than('createdAt',curTime)
            #
            # questionNum = query.count()
            # print "[%s] total questionNums: %d in tableIndex: %s\n" %(datetime.now(),questionNum, tableIndexStr)
            # queryLimit = 700
            # queryTimes = questionNum/queryLimit + 1
            #
            # for index in range(queryTimes):
            #     query = Query(Question)
            #     # query.less_than('createdAt',Question)
            #     query.exists('questionId')
            #     query.descending('createdAt')
            #     query.limit(queryLimit)
            #     query.skip(index*queryLimit)
            #     query.select('questionId')
            #     query.select('tableIndex')
            #
            #     try:
            #         quesRet = query.find()
            #     except:
            #         try:
            #             quesRet = query.find()
            #         except:
            #             try:
            #                 quesRet = query.find()
            #             except:
            #                 quesRet = query.find()
            #
            #
            #     for ques in quesRet:
            #         quesInfoList =[]
            #         questionId = int(ques.get('questionId'))
            #         if questionId in self.questionIdSet :
            #             pass
            #         else:
            #
            #             client_s.incr('totalCount',1)
            #             client_s.incr('t'+tableIndexStr,1)
            #             quesInfoList.append(questionId)
            #             quesInfoList.append(int(ques.get('tableIndex')))
            #             self.questionIdSet.add(questionId)
            #             client_s.set(str(self.quesIndex),quesInfoList)
            #             self.quesIndex +=1


         # Questions = Object.extend('Questions')
         # query = Query(Questions)
         # query.exists('questionId')
         # curTime = datetime.now()
         # query.less_than('createdAt',curTime)
         #
         # questionNum = query.count()
         # print "questionNums: %s" %str(questionNum)
         # queryLimit = 500
         # queryTimes = questionNum/queryLimit + 1
         # self.urls = []
         # for index in range(queryTimes):
         #    query = Query(Questions)
         #    query.less_than('createdAt',curTime)
         #    query.exists('questionLinkHref')
         #    query.descending('createdAt')
         #    query.limit(queryLimit)
         #    query.skip(index*queryLimit)
         #    query.select('questionLinkHref')
         #    quesRet = query.find()
         #    for ques in quesRet:
         #        self.urls.append("http://www.zhihu.com"+ ques.get('questionLinkHref'))
    # @classmethod
    # def from_crawler(cls, crawler,**kwargs):
    #     return cls(crawler.stats)

    # def start_requests(self):
    #     #print "start_requests ing ......"
    #     yield Request("http://www.zhihu.com",callback = self.post_login)
    def start_requests(self):
        # self.questionIdList= range(0,123)
        # questionIdListLength =123
        self.questionIdList = self.redis0.hvals('questionIndex')
        questionIdListLength = len(self.questionIdList)

        if self.spider_type=='Master':
            log.msg('Master spider_type is '+self.spider_type,level=log.WARNING)
            if self.partition!=1:
                log.msg('Master non 1 partition is '+str(self.partition),level=log.WARNING)
                self.questionIdList = self.questionIdList[self.spider_number*questionIdListLength/self.partition:(self.spider_number+1)*questionIdListLength/self.partition]
                for index in range(1,self.partition):
                    payload ={
                        'project':settings.BOT_NAME
                        ,'spider':self.name
                        ,'spider_type':'Slave'
                        ,'spider_number':index
                        ,'partition':self.partition
                        ,'setting':'JOBDIR=/tmp/scrapy/'+self.name+str(index)
                    }
                    log.msg('Begin to request'+str(index),level=log.WARNING)
                    response = requests.post('http://'+settings.SCRAPYD_HOST_LIST[self.spider_number]+':'+settings.SCRAPYD_PORT+'/schedule.json',data=payload)
                    log.msg('Response: '+str(index)+' '+str(response),level=log.WARNING)

        elif self.spider_type =='Slave':
            log.msg('Slave spider_type is '+self.spider_type,level=log.WARNING)
            log.msg('Slave number is '+str(self.spider_number) + ' partition is '+str(self.partition),level=log.WARNING)
            if (self.partition-self.spider_number)!=1:
                self.questionIdList = self.questionIdList[self.spider_number*questionIdListLength/self.partition:(self.spider_number+1)*questionIdListLength/self.partition]
            else:
                self.questionIdList = self.questionIdList[self.spider_number*questionIdListLength/self.partition:]
        else:
            log.msg('spider_type is:'+str(self.spider_type)+'with type of '+str(type(self.spider_type)))
        #print "start_requests ing ......"
        yield Request("http://www.zhihu.com",callback = self.post_login)

    # def testScrapyd(self,response):
    #     item =  ZhquesinfoItem()
    #     log.msg('spider_type: '+str(self.spider_type)
    #             +'\nspider_number: '+str(self.spider_number)
    #             +'\npartition: '+str(self.partition)
    #             +'\nemail: '+str(self.email)
    #             +'\npassword: '+str(self.password)
    #             +'\nquestionIdList: '+str(self.questionIdList)
    #             ,level=log.WARNING)
    #     yield item


        # print "spider_type: %s\nspider_number: %s\npartition: %email: %s\npassword: %s\nquestionIdList: %s" % (self.spider_type
        #                                                                                                        ,self.spider_number
        #                                                                                                        ,self.partition
        #                                                                                                        ,self.email
        #                                                                                                        ,self.password
        #                                                                                                        ,str(self.questionIdList))



    def post_login(self,response):
        #print "post_login ing ......"
        xsrfValue = response.xpath('/html/body/input[@name= "_xsrf"]/@value').extract()[0]
        yield FormRequest.from_response(response,
                                          #headers = self.headers,
                                          formdata={
                                              '_xsrf':xsrfValue,
                                              'email':self.email,
                                              'password':self.password,
                                              'rememberme': 'y'
                                          },
                                          dont_filter = True,
                                          callback = self.after_login,
                                         #dont_filter = True
                                          )

    def after_login(self,response):
        #print "after_login ing ....."
        #inspect_response(response,self)
        #self.urls = ['http://www.zhihu.com/question/28626263','http://www.zhihu.com/question/22921426','http://www.zhihu.com/question/20123112']
        for questionId in self.questionIdList:
            yield self.make_requests_from_url(self.baseUrl +str(questionId)+'?nr=1')


    def parse(self,response):
        if response.status != 200:
#            print "ParsePage HTTPStatusCode: %s Retrying !" %str(response.status)
            yield  self.make_requests_from_url(response.url)

        else:

            item =  ZhquesinfoItem()
            #print "parsePage ing......"
            item['questionId'] = re.split('http://www.zhihu.com/question/(\d*)',response.url)[1]
            item['idZnonceContent'] = response.xpath('//*[@id="znonce"]/@content').extract()[0]  #right
            item['dataUrlToken'] = response.xpath('//*[@id="zh-single-question-page"]/@data-urltoken').extract()[0] #right
            item['isTopQuestion'] = response.xpath('//*[@id="zh-single-question-page"]/meta[@itemprop="isTopQuestion"]/@content').extract()[0]    #right
            item['visitsCount'] = int(response.xpath('//*[@id="zh-single-question-page"]/meta[@itemprop="visitsCount"]/@content').extract()[0])    #right
            try:
                item['tagLabelHrefList'] = response.xpath('//div[@id="zh-single-question-page"]//div[@class="zm-tag-editor-labels zg-clear"]/a/@href').extract()   #right
                item ['tagLabelDataTopicIdList'] = response.xpath('//div[@id="zh-single-question-page"]//div[@class="zm-tag-editor-labels zg-clear"]/a/@data-topicid').extract()   #right
            except IndexError,e:
                item['tagLabelHrefList'] = []
                item['tagLabelDataTopicIdList'] =[]
                #print e

            item['questionTitle'] = response.xpath('//div[@id="zh-question-title"]/h2/text()').extract()[0] #right

            try:
                item['questionDetail'] = response.xpath('//div[@id="zh-question-detail"]/div[@class="zm-editable-content"]/text()').extract()
                if  item['questionDetail'] :
                    item['questionDetail'] = item['questionDetail'][0]
                else:
                    item['questionDetail'] = ''
            except:
                item['questionDetail'] = response.xpath('//div[@id="zh-question-detail"]/textarea[@class="content hidden"]/text()').extract()[0]

            item['dataResourceId'] = response.xpath('//div[@id="zh-question-detail"]/@data-resourceid').extract()[0]    #right


            try:
                item['quesCommentCount'] = response.xpath('//div[@id="zh-question-meta-wrap"]//a[@name="addcomment"]/text()[2]').re('\d*')[0]   # should try
                if item['quesCommentCount']:
                    item['quesCommentCount'] = int (item['quesCommentCount'])
                else:
                    item['quesCommentCount'] = 0

            except IndexError,e:
                item['quesCommentCount'] = 0

            #item['quesCommentLink'] = response.xpath('').extract()
            try:
                item['questionAnswerNum'] = int(response.xpath('//*[@id="zh-question-answer-num"]/@data-num').extract()[0])  #right
            except IndexError,e:
                item['questionAnswerNum'] = 0

            #item['dataPageSize'] = response.xpath('//*[@id="zh-question-answer-wrap"]').extract()
            #item['pageSize'] = response.xpath('').extract()
            #item['offset'] = response.xpath('').extract()
            #item['nodeName'] = response.xpath('//*[@id="zh-question-answer-wrap"]/@nodename').extract()


            # item['dataAid'] = response.xpath('//*[@id="zh-question-answer-wrap"]/div[1]').extract()
            #
            # item['dataAtoken'] = response.xpath('').extract()
            # item['dataCreated'] = response.xpath('').extract()
            # item['dataDeleted'] = response.xpath('').extract()
            # item['dataHelpful'] = response.xpath('').extract()
            # item['dataScore'] = response.xpath('').extract()

            #item['questionFollowDataId'] = response.xpath('//*[@id="zh-question-side-header-wrap"]/button').extract()

            #item['questionFollowerLink'] = response.xpath('//*[@id="zh-question-side-header-wrap"]/div[@class="zh-question-followers-sidebar"]/div[1]/a/@href').extract()[0]
            try:
                item['questionFollowerCount'] = int(response.xpath('//*[@id="zh-question-side-header-wrap"]/div[@class="zh-question-followers-sidebar"]/div[1]/a/strong/text()').extract()[0])  #right
            except IndexError,e:
                item['questionFollowerCount'] = 0

            #item['quescommentcounttionFollowerList'] = response.xpath('//*[@id="zh-question-side-header-wrap"]/div[@class="zh-question-followers-sidebar"]/div[2]').extract()

            #item['sideSectionId'] = response.xpath('//*[@id="shameimaru-question-up-83594d68c"]').extract()


            #item['shareDataId'] = response.xpath('//*[@id="zh-question-webshare-container"]').extract()


            # item[''] = response.xpath('').extract()
            # item[''] = response.xpath('').extract()
            # item[''] = response.xpath('').extract()

            try:
                item['questionLatestActiveTime'] = response.xpath('//*[@id="zh-single-question-page"]//span[@class="time"]/text()').extract()[0]
            except:
                try:
                    item['questionLatestActiveTime'] = response.xpath('//*[@id="zh-single-question-page"]//span[@class="time"]/text()').extract()[0]
                except:
                    item['questionLatestActiveTime'] =''
                    print "Error in questionLatestActiveTime : %s" %response.url

           # item['questionLog'] = response.xpath('//*[@id="zh-single-question-page"]/div[2]/div[5]/div/div[1]/a').extract()[0]
            try:
                item['questionShowTimes'] = int(response.xpath('//*[@id="zh-single-question-page"]/div[@class="zu-main-sidebar"]/div[last()-1]//div[@class="zg-gray-normal"][2]/strong[1]/text()').extract()[0])
            except:
                item['questionShowTimes'] = int(response.xpath('//*[@id="zh-single-question-page"]/div[@class="zu-main-sidebar"]/div[last()]//div[@class="zg-gray-normal"][2]/strong[1]/text()').extract()[0])

            try:
                item['topicRelatedFollowerCount'] = int(response.xpath('//*[@id="zh-single-question-page"]/div[@class="zu-main-sidebar"]/div[last()-1]//div[@class="zg-gray-normal"][2]/strong[2]/text()').extract()[0])
            except:
                item['topicRelatedFollowerCount'] = int(response.xpath('//*[@id="zh-single-question-page"]/div[@class="zu-main-sidebar"]/div[last()]//div[@class="zg-gray-normal"][2]/strong[2]/text()').extract()[0])
           # item['questionFollowerCount'] = response.xpath('//*[@id="zh-question-side-header-wrap"]/div[2]/div[1]/a/strong').extract()[0]


            try:
                item['relatedQuestionLinkList'] = response.xpath('//*[@id="zh-question-related-questions"]//ul//li//a/@href').extract()     #should try
            except IndexError,e:
                item['relatedQuestionLinkList'] = []



          #  print response.status
            yield item

        # for index,url in enumerate(self.urls):
        #     yield Request(url,meta = {'cookiejar':index},callback = self.parse_page)




    # def closed(self,reason):
    #     #f = open('../../nohup.out')
    #     #print f.read()
    #     leancloud.init(settings.APP_ID, master_key=settings.MASTER_KEY)
    #
    #
    #     CrawlerLog = Object.extend('CrawlerLog')
    #     crawlerLog = CrawlerLog()
    #
    #     crawlerLog.set('crawlerName',self.name)
    #     crawlerLog.set('closedReason',reason)
    #     crawlerLog.set('crawlerStats',self.stats.get_stats())
    #     try:
    #         crawlerLog.save()
    #     except:
    #         pass


