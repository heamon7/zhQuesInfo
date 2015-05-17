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

class QuesInfoPipeline(object):
    def __init__(self):
        leancloud.init('dh9dwra0dkin5zv2en2gj6jndplwnl5aqr15uv540mhzjpqp', master_key='bmblhzxwa4lww1beek9288m7tc4crio1fhahxohgsu31yai4')
        pass
    def process_item(self, item, spider):
         TestQuestionInfo = Object.extend('TestQuestionInfo')
         questionInfo = TestQuestionInfo()
         try:
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
            questionInfo.save()
         except LeanCloudError,e:
             print e



         DropItem()
