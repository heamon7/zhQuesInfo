# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exceptions import DropItem
from zhQuesInfo import settings

import re
import redis
import happybase
import time
import logging

class QuesInfoPipeline(object):


    def __init__(self):

        self.redis2 = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_USER+':'+settings.REDIS_PASSWORD,db=2)
        connection = happybase.Connection(settings.HBASE_HOST)
        self.questionTable = connection.table('question')
        pass
    def process_item(self, item, spider):

        questionId = str(item['questionId'])

        isTopQuestion = 1 if item['isTopQuestion'] == 'true' else 0

        currentTimestamp = int(time.time())

        result = self.redis2.lindex(str(questionId),0)
        if result:
            recordTimestamp =result
        else:
            recordTimestamp=''

        if not recordTimestamp or (int(currentTimestamp)-int(recordTimestamp) > int(settings.UPDATE_PERIOD)):        # the latest record time in hbase
            recordTimestamp = currentTimestamp

            try:
                self.questionTable.put(str(questionId),{'detail:idZnonceContent':str(item['idZnonceContent']),
                                               'detail:dataUrlToken':str(item['dataUrlToken']),
                                               'detail:isTopQues':str(isTopQuestion),
                                               'detail:tagLabelIdList': str(item['tagLabelIdList']),
                                               'detail:tagLabelDataTopicIdList': str(item['tagLabelDataTopicIdList']),
                                               'detail:questionTitle': item['questionTitle'].encode('utf-8'),
                                               'detail:dataResourceId': str(item['dataResourceId']),
                                               'detail:quesAnswerCount': str(item['questionAnswerCount']),
                                               'detail:quesFollowerCount': str(item['questionFollowerCount']),
                                               'detail:quesLatestActiveTime': item['questionLatestActiveTime'].encode('utf-8'),
                                               'detail:quesShowTimes': str(item['questionShowTimes']),
                                               'detail:topicRelatedFollowerCount': str(item['topicRelatedFollowerCount']),
                                               'detail:quesDetail': item['questionDetail'].encode('utf-8'),
                                               'detail:relatedQuesLinkList': str(item['relatedQuestionLinkList']),
                                               'detail:quesCommentCount': str(item['quesCommentCount']),
                                               'detail:visitsCount': str(item['visitsCount'])})

            except Exception,e:
                logging.warning('Error with put questionId into hbase: '+str(e)+' try again......')
                try:
                    self.questionTable.put(str(questionId),{'detail:idZnonceContent':str(item['idZnonceContent']),
                                               'detail:dataUrlToken':str(item['dataUrlToken']),
                                               'detail:isTopQues':str(isTopQuestion),
                                               'detail:tagLabelIdList': str(item['tagLabelIdList']),
                                               'detail:tagLabelDataTopicIdList': str(item['tagLabelDataTopicIdList']),
                                               'detail:questionTitle': item['questionTitle'].encode('utf-8'),
                                               'detail:dataResourceId': str(item['dataResourceId']),
                                               'detail:quesAnswerCount': str(item['questionAnswerCount']),
                                               'detail:quesFollowerCount': str(item['questionFollowerCount']),
                                               'detail:quesLatestActiveTime': item['questionLatestActiveTime'].encode('utf-8'),
                                               'detail:quesShowTimes': str(item['questionShowTimes']),
                                               'detail:topicRelatedFollowerCount': str(item['topicRelatedFollowerCount']),
                                               'detail:quesDetail': item['questionDetail'].encode('utf-8'),
                                               'detail:relatedQuesLinkList': str(item['relatedQuestionLinkList']),
                                               'detail:quesCommentCount': str(item['quesCommentCount']),
                                               'detail:visitsCount': str(item['visitsCount'])})
                    logging.warning('tried again and successfully put data into hbase ......')
                except Exception,e:
                    logging.warning('Error with put questionId into hbase: '+str(e)+'tried again and failed')

            p2 = self.redis2.pipeline()
            p2.lpush(str(questionId)
                     # ,int(questionId)
                     ,str(item['dataResourceId'])
                     ,str(isTopQuestion)
                     ,str(item['questionFollowerCount'])

                     ,str(item['questionAnswerCount'])
                     ,str(item['quesCommentCount'])
                     ,str(item['questionShowTimes'])

                     ,str(item['topicRelatedFollowerCount'])
                     ,str(item['visitsCount'])
                     ,str(recordTimestamp))

            p2.ltrim(str(questionId),0,8)
            p2.execute()
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
