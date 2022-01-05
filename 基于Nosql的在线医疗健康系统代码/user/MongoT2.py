# -*- coding: utf-8 -*-
# @Time    : 2021/6/22 10:37
# @Author  : JokerTong
# @File    : MongoT2.py
import pymongo
import csv
from bson.code import Code
import random
import time


def connection():
    # 建立连接
    client = pymongo.MongoClient("localhost", 27017)
    # 指定数据库
    db = client['nosql']
    # 指定集合
    return db


db = connection()
article = db["article"]
doctor = db["doctor"]
comment = db["comment"]


def insertArticle(id, title, type, date, content):
    mydict = {"_id": id, "title": title, "type": type, "date": date, "content": content}
    article.insert_one(mydict)


def insertDoctor(id, doc_id, name, articles, position, speciality, hospital, department, stars, register_time):
    mydict = {"_id": id, "doc_id": id, "name": name, "position": position, "stars": stars, "department": department,
              "hospital": hospital, "speciality": speciality, "register_time": register_time, "articles": articles}
    doctor.insert_one(mydict)


def insertComment(id, date, user_name, content, belong):
    mydict = {"_id": id, "date": date, "user_name": user_name, "content": content, "belong": belong}
    comment.insert_one(mydict)


def insertDoctors():  # 批量插入医生
    #     for i in range(0,4):
    #         id="ObjectID('au{}')".format(i+1)
    #         names=["贾国葆","谢于鹏","罗惜绍","郑明华"]
    #         positions=["副主任医师","主任医师","医师","主任医师"]
    #         specialities=["胃食管反流病",
    #                     "擅长成人打鼾，睡眠呼吸暂停，烟草依赖，哮喘，慢阻肺，肺结节，肺癌，肺炎，支气管炎，咳嗽等诊疗",
    #                     "擅长子宫平滑肌瘤 卵巢肿瘤 子宫内膜息肉 宫颈疾病 女性内分泌失调 痛经 阴道炎 下腹痛 流产等各种妇科疾病的诊治",
    #                     "从事肝病临床工作13年，主攻方向为重型肝炎、肝衰竭的治疗，擅长病毒性肝炎、脂肪肝、肝硬化、酒精肝、自身免疫性肝病及肝癌靶向治疗"]

    #         department=["消化内科","呼吸科","妇科","感染科"]
    #         articles=[["ObjectID('a1')"],["ObjectID('a2')","ObjectID('a3')"],["ObjectID('a4')"],["ObjectID('a5')","ObjectID('a6')"]]
    #         hospitals=["温州医科大学附属第一医院","温州医科大学附属第一医院","温州医科大学附属第一医院","温州医科大学附属第一医院"]

    with open(r'doctor.csv', 'r', encoding='UTF-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        i = 0
        article_count = article.count()
        count_list = range(1, article_count + 1)
        for each in reader:
            i = i + 1
            id = "ObjectID(au{})".format(i + 1)
            name = each["name"]
            position = each['position']
            speciality = each['speciality']
            department = each['department']
            hospital = each['hospital']
            stars = 0

            num = random.randint(0, 2)  # 随机分配文章（一个作者最多写了两篇文章）
            if (len(count_list) - num > 1):
                if (num == 1):
                    article_rank = count_list[-article_count]
                    articles = "Object(a{})".format(article_rank)
                    article_count = article_count - 1
                elif (num == 2):
                    article_rank1 = count_list[-article_count]
                    article_rank2 = count_list[-article_count + 1]
                    articles = ["Object(a{})".format(article_rank1), "Object(a{})".format(article_rank2)]
                    article_count = article_count - 2
                else:
                    articles = []
            elif (len(count_list) == 1):
                article_rank = count_list[-article_count]
                articles = "Object(a{})".format(article_rank)
                article_count = article_count - 1
            else:
                artciles = []

            a1 = (2012, 1, 1, 0, 0, 0, 0, 0, 0)  # 随机产生时间
            a2 = (2021, 6, 21, 23, 59, 59, 0, 0, 0)
            start = time.mktime(a1)
            end = time.mktime(a2)
            t = random.randint(start, end)
            date_touple = time.localtime(t)
            register_time = time.strftime("%Y-%m-%d", date_touple)

            insertDoctor(id, id, name, articles, position, speciality, hospital, department, stars, register_time)


def insertArticles():  # 批量插入文章
    with open(r'articles.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        i = 0
        for each in reader:
            i = i + 1
            id = "ObjectID(a{})".format(i)

            title = each['文本']
            title = title.strip()
            title = title.split(" ")
            if (len(title) > 1):
                title = title[0]

            type1 = "医学常识"
            type2 = '走出亚健康'
            type3 = '医疗建设'
            num = random.randint(1, 3)
            if (num % 3 == 0):
                type = type1
            elif (num % 3 == 1):
                type = type2
            else:
                type = type3

            date = each['发布时间']
            date = date.split('：')[1]

            content = each["正文"]
            content = content.rstrip()

            insertArticle(id, title, type, date, content)


def insertComments():  # 随机生成评论 批量插入
    for i in range(1, 105):
        id = "ObjectID(c{})".format(i)

        num = random.randint(1, 101)  # 评论属于哪篇文章
        belong = "ObjectID('a{}')".format(num)

        a1 = (2015, 1, 1, 0, 0, 0, 0, 0, 0)  # 随机产生时间
        a2 = (2021, 6, 21, 23, 59, 59, 0, 0, 0)
        start = time.mktime(a1)
        end = time.mktime(a2)
        t = random.randint(start, end)
        date_touple = time.localtime(t)
        date = time.strftime("%Y-%m-%d %H:%M:%S", date_touple)

        count = random.randint(1, 51)  # 随机生成评论的用户
        user_name = "tty小号{}".format(count)

        # 随机生成评论内容
        textlist = ["好", "很好", "写得非常好", "支持一下", "请问能具体联系一下医生吗?", "有没有试过的说说可不可靠？",
                    "写得一般般", "这个医生还是挺厉害的", "佩服佩服", "希望这种文章越来越多"]
        randnum = random.randint(1, 10)
        text = textlist[i % randnum]

        insertComment(id, date, user_name, text, belong)


def commentsOfArticle(id):  # 根据文章的id 从时间的新到旧显示该文章所有的评论
    belong = "ObjectID('{}')".format(id)
    comments = comment.find({"belong": belong}).sort([("date", -1)])
    return comments


def findArticleByDoctor(id):  # 根据医生id查询所写的文章
    id = "ObjectID('{}')".format(id)
    doctorid = doctor.find_one({"_id": id})
    doctor_articles_id = doctorid["articles"]
    articles_name_list = []
    for each in doctor_articles_id:
        articles_name = article.find_one({'_id': each})['title']
        articles_name_list.append(articles_name)
    return articles_name_list


insertDoctors()
# insertArticles()
