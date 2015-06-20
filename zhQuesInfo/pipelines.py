# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import leancloud
# from leancloud import Object
# from leancloud import LeanCloudError
# from leancloud import Query
from scrapy import log
from scrapy.exceptions import DropItem
from zhQuesInfo import settings
import bmemcached
import re
import redis
import happybase

class QuesInfoPipeline(object):
    # dbPrime = 97

    def __init__(self):
        # leancloud.init(settings.APP_ID, master_key=settings.MASTER_KEY)
        # self.client1 = bmemcached.Client(settings.CACHE_SERVER_1,settings.CACHE_USER_1,settings.CACHE_PASSWORD_1)
        #
        # self.client2 = bmemcached.Client(settings.CACHE_SERVER_2,settings.CACHE_USER_2,settings.CACHE_PASSWORD_2)
        # self.client3 = bmemcached.Client(settings.CACHE_SERVER_3,settings.CACHE_USER_3,settings.CACHE_PASSWORD_3)
        # self.redis1 = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_USER+':'+settings.REDIS_PASSWORD,db=1)
        self.redis2 = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_USER+':'+settings.REDIS_PASSWORD,db=2)
        connection = happybase.Connection(settings.HBASE_HOST)
        self.questionTable = connection.table('question')
        pass
    def process_item(self, item, spider):

        questionId = str(item['questionId'])
        # if self.redis2.get(questionId):
        #     pass
        # if 0:
        #     pass
        # else:
            # questionRef =''
        # questionIndex = self.redis1.lindex(str(questionId),0)

        # try:
        #     tableIndex = int(self.redis1.lindex(str(questionId),1))
        #
        # except:
        #     try:
        #         questionId = str(re.split('(\d*)\?rf=(\d*)',item['questionId'])[2])
        #         tableIndex = int(self.redis1.lindex(str(questionId),1))
        #         questionRef = str(re.split('(\d*)\?rf=(\d*)',item['questionId'])[1])
        #     except:
        #         tableIndex =98
        #         print questionId
        # #tableIndex = int(item['dataUrlToken']) % self.dbPrime
        # if tableIndex < 10:
        #     tableIndexStr = '0' + str(tableIndex)
        # else:
        #     tableIndexStr = str(tableIndex)
        #
        #
        # QuestionInfo = Object.extend('QuestionInfo'+tableIndexStr)
        # questionInfo = QuestionInfo()

        try:
            self.questionTable.put(str(questionId),{'detail:idZnonceContent':str(item['idZnonceContent']),
                                           'detail:dataUrlToken':str(item['dataUrlToken']),
                                           'detail:isTopQuestion':str(item['isTopQuestion']),
                                           'detail:tagLabelHrefList': str(item['tagLabelHrefList']),
                                           'detail:tagLabelDataTopicIdList': str(item['tagLabelDataTopicIdList']),
                                           'detail:questionTitle': item['questionTitle'].encode('utf-8'),
                                           'detail:dataResourceId': str(item['dataResourceId']),
                                           'detail:quesAnswerNum': str(item['questionAnswerNum']),
                                           'detail:quesFollowerCount': str(item['questionFollowerCount']),
                                           'detail:quesLatestActiveTime': str(item['questionLatestActiveTime']),
                                           'detail:quesShowTimes': str(item['questionShowTimes']),
                                           'detail:topicRelatedFollowerCount': str(item['topicRelatedFollowerCount']),
                                           'detail:quesDetail': item['questionDetail'].encode('utf-8'),
                                           'detail:relatedQuesLinkList': str(item['relatedQuestionLinkList']),
                                           'detail:quesCommentCount': str(item['quesCommentCount']),
                                           'detail:visitsCount': str(item['visitsCount'])})


            isTopQuestion = 1 if item['isTopQuestion'] == 'true' else 0
            p2 = self.redis2.pipeline()
            p2.lpush(str(questionId)
                     # ,int(questionId)
                     ,int(item['dataResourceId'])
                     ,int(isTopQuestion)
                     ,int(item['questionFollowerCount'])
                     ,int(item['questionAnswerNum'])
                     ,int(item['quesCommentCount'])
                     ,int(item['questionShowTimes'])
                     ,int(item['topicRelatedFollowerCount'])
                     ,int(item['visitsCount']))
            p2.ltrim(str(questionId),0,7)
            p2.execute()
        except Exception,e:
            print e
            print questionId
    DropItem()


        # questionInfo.set('tableIndex',tableIndex)

        # questionInfo.set('questionId',item['questionId'])
        # questionInfo.set('idZnonceContent',item['idZnonceContent'])
        # questionInfo.set('dataUrlToken',item['dataUrlToken'])
        # questionInfo.set('isTopQuestion',item['isTopQuestion'])
        # questionInfo.set('tagLabelHrefList',item['tagLabelHrefList'])
        # questionInfo.set('tagLabelDataTopicIdList',item['tagLabelDataTopicIdList'])
        # questionInfo.set('questionTitle',item['questionTitle'])
        # questionInfo.set('dataResourceId',item['dataResourceId'])
        # questionInfo.set('questionAnswerNum',item['questionAnswerNum'])
        # questionInfo.set('questionFollowerCount',item['questionFollowerCount'])
        # questionInfo.set('questionLatestActiveTime',item['questionLatestActiveTime'])
        # questionInfo.set('questionShowTimes',item['questionShowTimes'])
        # questionInfo.set('topicRelatedFollowerCount',item['topicRelatedFollowerCount'])
        # questionInfo.set('questionDetail',item['questionDetail'])
        # questionInfo.set('relatedQuestionLinkList',item['relatedQuestionLinkList'])
        # questionInfo.set('quesCommentCount',item['quesCommentCount'])
        # questionInfo.set('visitsCount',item['visitsCount'])
        #
        # questionInfo.set('questionRef',questionRef)
        #
        #
        # questionInfo.set('questionIndex',str(questionIndex))





        #
        #
        # try:
        #     questionInfo.save()
        # except LeanCloudError,e:
        #     try:
        #         questionInfo.save()
        #
        #     except LeanCloudError,e:
        #         print e



