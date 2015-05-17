# -*- coding: utf-8 -*-
import scrapy

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request,FormRequest
from scrapy.conf import settings
from scrapy import log
from scrapy.shell import inspect_response

import leancloud

from leancloud import Object
from leancloud import LeanCloudError
from leancloud import Query

from datetime import datetime

from zhQuesInfo.items import ZhquesinfoItem




class QuesinfoerSpider(scrapy.Spider):
    name = "quesInfoer"
    allowed_domains = ["zhihu.com"]
    start_urls = (
        'http://www.zhihu.com/',
    )

    def __init__(self):
         print "Initianizing ....."
         leancloud.init('dh9dwra0dkin5zv2en2gj6jndplwnl5aqr15uv540mhzjpqp', master_key='bmblhzxwa4lww1beek9288m7tc4crio1fhahxohgsu31yai4')
         #
         Questions = Object.extend('Questions')
         question = Questions()
         #
         query = Query(Questions)
         query.exists('questionLinkHref')
         curTime = datetime.now()
         query.less_than('createdAt',curTime)
         questionNum = query.count()
         print "questionNums: %s" %str(questionNum)
         queryLimit = 500
         queryTimes = questionNum/queryLimit + 1
         self.urls = []
         for index in range(queryTimes):
            query = Query(TestQuestions)
            query.less_than('createdAt',curTime)
            query.exists('questionLinkHref')
            query.descending('createdAt')
            query.limit(queryLimit)
            query.skip(index*queryLimit)
            query.select('questionLinkHref')
            quesRet = query.find()
            for ques in quesRet:
                self.urls.append("http://www.zhihu.com"+ ques.get('questionLinkHref'))

    def start_requests(self):
        print "start_requests ing ......"
        return [Request("http://www.zhihu.com",callback = self.post_login)]

    def post_login(self,response):
        print "post_login ing ......"
        xsrfValue = response.xpath('/html/body/input[@name= "_xsrf"]/@value').extract()[0]
        return [FormRequest.from_response(response,
                                          #headers = self.headers,
                                          formdata={
                                              '_xsrf':xsrfValue,
                                              'email':'heamon8@163.com',
                                              'password':'heamon8@()',
                                              'rememberme': 'y'
                                          },
                                          dont_filter = True,
                                          callback = self.after_login
                                        #  dont_filter = True
                                          )]

    def after_login(self,response):
        print "after_login ing ....."
        #inspect_response(response,self)
        #self.urls = ['http://www.zhihu.com/question/28626263','http://www.zhihu.com/question/22921426','http://www.zhihu.com/question/20123112']
        for url in self.urls:
            yield self.make_requests_from_url(url)


    def parse(self,response):

        item =  ZhquesinfoItem()
        print "parsePage ing......"

        item['idZnonceContent'] = response.xpath('//*[@id="znonce"]/@content').extract()[0]  #right
        item['dataUrlToken'] = response.xpath('//*[@id="zh-single-question-page"]/@data-urltoken').extract()[0] #right
        item['isTopQuestion'] = response.xpath('//*[@id="zh-single-question-page"]/meta[@itemprop="isTopQuestion"]/@content').extract()[0]    #right
        item['visitsCount'] = response.xpath('//*[@id="zh-single-question-page"]/meta[@itemprop="visitsCount"]/@content').extract()[0]    #right
        try:
            item['tagLabelHrefList'] = response.xpath('//div[@id="zh-single-question-page"]//div[@class="zm-tag-editor-labels zg-clear"]/a/@href').extract()   #right
            item ['tagLabelDataTopicIdList'] = response.xpath('//div[@id="zh-single-question-page"]//div[@class="zm-tag-editor-labels zg-clear"]/a/@data-topicid').extract()   #right
        except IndexError,e:
            item['tagLabelHrefList'] = []
            item['tagLabelDataTopicIdList'] =[]
            #print e

        item['questionTitle'] = response.xpath('//div[@id="zh-question-title"]/h2/text()').extract()[0] #right

        try:
            item['questionDetail'] = response.xpath('//div[@id="zh-question-detail"]/div[@class="zm-editable-content"]/text()').extract()[0]
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


        item['questionLatestActiveTime'] = response.xpath('//*[@id="zh-single-question-page"]//span[@class="time"]/text()').extract()[0]
       # item['questionLog'] = response.xpath('//*[@id="zh-single-question-page"]/div[2]/div[5]/div/div[1]/a').extract()[0]
        item['questionShowTimes'] = int(response.xpath('//*[@id="zh-single-question-page"]/div[@class="zu-main-sidebar"]/div[last()]//div[@class="zg-gray-normal"][2]/strong[1]/text()').extract()[0])
        item['topicRelatedFollowerCount'] = int(response.xpath('//*[@id="zh-single-question-page"]/div[@class="zu-main-sidebar"]/div[last()]//div[@class="zg-gray-normal"][2]/strong[2]/text()').extract()[0])

       # item['questionFollowerCount'] = response.xpath('//*[@id="zh-question-side-header-wrap"]/div[2]/div[1]/a/strong').extract()[0]


        try:
            item['relatedQuestionLinkList'] = response.xpath('//*[@id="zh-question-related-questions"]//ul//li//a/@href').extract()     #should try
        except IndexError,e:
            item['relatedQuestionLinkList'] = []



      #  print response.status
        return item

        # for index,url in enumerate(self.urls):
        #     yield Request(url,meta = {'cookiejar':index},callback = self.parse_page)









