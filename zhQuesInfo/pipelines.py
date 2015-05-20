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

class QuesInfoPipeline(object):
    dbPrime = 97
    questionInfoList =[]

    def __init__(self):
        leancloud.init(settings.APP_ID, master_key=settings.MASTER_KEY)
        self.client = bmemcached.Client(settings.CACHE_SERVER,settings.CACHE_USER,settings.CACHE_PASSWORD)

        pass
    def process_item(self, item, spider):
        if self.client.get(item['questionId']):
            pass
        else:
            tableIndex = int(item['dataUrlToken']) % self.dbPrime
            if tableIndex < 10:
                tableIndexStr = '0' + str(tableIndex)
            else:
                tableIndexStr = str(tableIndex)
            QuestionInfo = Object.extend('QuestionInfo'+tableIndexStr)
            questionInfo = QuestionInfo()

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

            self.questionInfoList.append(int(tableIndex))
            if item['isTopQuestion'] == 'true':
                self.questionInfoList.append(1)
            else:
                self.questionInfoList.append(0)

            self.questionInfoList.append(int(item['dataResourceId']))
            self.questionInfoList.append(int(item['questionAnswerNum']))
            self.questionInfoList.append(int(item['questionFollowerCount']))
            self.questionInfoList.append(int(item['quesCommentCount']))

            self.client.set(str(item['questionId']),self.questionInfoList,0)
            self.client.incr('totalCount',1)


            try:
                questionInfo.save()
            except LeanCloudError,e:
                try:
                    questionInfo.save()

                except LeanCloudError,e:
                    print e



        DropItem()
