# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import leancloud
from leancloud import Object
from leancloud import LeanCloudError
from leancloud import Query
from scrapy import log
from scrapy.exceptions import DropItem
from zhQuesInfo import settings
import bmemcached
import re
import redis
class QuesInfoPipeline(object):
    dbPrime = 97

    def __init__(self):
        leancloud.init(settings.APP_ID, master_key=settings.MASTER_KEY)
        # self.client1 = bmemcached.Client(settings.CACHE_SERVER_1,settings.CACHE_USER_1,settings.CACHE_PASSWORD_1)
        #
        # self.client2 = bmemcached.Client(settings.CACHE_SERVER_2,settings.CACHE_USER_2,settings.CACHE_PASSWORD_2)
        # self.client3 = bmemcached.Client(settings.CACHE_SERVER_3,settings.CACHE_USER_3,settings.CACHE_PASSWORD_3)
        self.redis1 = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_USER+':'+settings.REDIS_PASSWORD,db=1)
        self.redis3 = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_USER+':'+settings.REDIS_PASSWORD,db=3)
        pass
    def process_item(self, item, spider):

        questionId = str(item['questionId'])
        if self.redis3.get(questionId):
            pass
        else:
            questionRef =''
            try:
                tableIndex = int(self.redis1.lindex(str(questionId),1))

            except:
                try:
                    questionId = str(re.split('(\d*)\?rf=(\d*)',item['questionId'])[2])
                    tableIndex = int(self.redis1.lindex(str(questionId),1))
                    questionRef = str(re.split('(\d*)\?rf=(\d*)',item['questionId'])[1])
                except:
                    tableIndex =98
                    print questionId
            #tableIndex = int(item['dataUrlToken']) % self.dbPrime
            if tableIndex < 10:
                tableIndexStr = '0' + str(tableIndex)
            else:
                tableIndexStr = str(tableIndex)

            questionIndex = self.redis1.lindex(str(questionId),0)
            QuestionInfo = Object.extend('QuestionInfo'+tableIndexStr)
            questionInfo = QuestionInfo()

            questionInfo.set('tableIndex',tableIndex)
            questionInfo.set('questionId',item['questionId'])
            questionInfo.set('idZnonceContent',item['idZnonceContent'])
            questionInfo.set('dataUrlToken',item['dataUrlToken'])
            questionInfo.set('isTopQuestion',item['isTopQuestion'])
            questionInfo.set('tagLabelHrefList',item['tagLabelHrefList'])
            questionInfo.set('tagLabelDataTopicIdList',item['tagLabelDataTopicIdList'])
            questionInfo.set('questionTitle',item['questionTitle'])
            questionInfo.set('dataResourceId',item['dataResourceId'])
            questionInfo.set('questionAnswerNum',item['questionAnswerNum'])
            questionInfo.set('questionFollowerCount',item['questionFollowerCount'])
            questionInfo.set('questionLatestActiveTime',item['questionLatestActiveTime'])
            questionInfo.set('questionShowTimes',item['questionShowTimes'])
            questionInfo.set('topicRelatedFollowerCount',item['topicRelatedFollowerCount'])
            questionInfo.set('questionDetail',item['questionDetail'])
            questionInfo.set('relatedQuestionLinkList',item['relatedQuestionLinkList'])
            questionInfo.set('quesCommentCount',item['quesCommentCount'])
            questionInfo.set('visitsCount',item['visitsCount'])

            questionInfo.set('questionRef',questionRef)


            questionInfo.set('questionIndex',str(questionIndex))


            if item['isTopQuestion'] == 'true':
                isTopQuestion =1
            else:
                isTopQuestion =0

            p3 = self.redis3.pipeline()
            p3.incr('totalCount',1)

            p3.rpush(str(questionId),int(questionIndex),int(tableIndexStr),int(item['dataResourceId']),int(isTopQuestion)
                     ,int(item['questionFollowerCount']),int(item['questionAnswerNum']),int(item['quesCommentCount'])
                     ,int(item['questionShowTimes']),int(item['topicRelatedFollowerCount']),int(item['visitsCount']))
            p3.execute()



            try:
                questionInfo.save()
            except LeanCloudError,e:
                try:
                    questionInfo.save()

                except LeanCloudError,e:
                    print e



        DropItem()
