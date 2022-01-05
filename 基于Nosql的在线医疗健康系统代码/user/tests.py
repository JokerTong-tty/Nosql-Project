from django.test import TestCase
import datetime
import redis
import numpy as np
import pymongo

conn = redis.StrictRedis(db=5, host='10.132.221.201', decode_responses=True)
client = pymongo.MongoClient("localhost", 27017)
# 指定数据库
db = client['nosql']


# 余弦相似度计算
def cos_sim(a, b):
    a_norm = np.linalg.norm(a)
    b_norm = np.linalg.norm(b)
    cos = np.dot(a, b) / (a_norm * b_norm)
    return cos


# 初始化热度
def init_hot():
    for i in range(20):
        hot = np.random.randint(100, 1000)
        conn.zadd('hot', {f'ObjectID(a{i})': hot})
        # conn.set(f'ObjectID(a{i}):hot', hot)


# print(conn.lrange('zqq:stars', 0, conn.llen('zqq:stars')))


def insert_score():
    conn.hset('tty:score', 'ObjectID(a1)', 4.5)
    conn.hset('tty:score', 'ObjectID(a2)', 5)
    # conn.hset('tty:score', 'ObjectID(a3)', 3.5)
    conn.hset('tty:score', 'ObjectID(a4)', 2)
    # conn.hset('tty:score', 'ObjectID(a5)', 5)

    conn.hset('zqq:score', 'ObjectID(a1)', 4.5)
    # conn.hset('zqq:score', 'ObjectID(a2)', 5)
    conn.hset('zqq:score', 'ObjectID(a3)', 3.5)
    conn.hset('zqq:score', 'ObjectID(a6)', 5)
    conn.hset('zqq:score', 'ObjectID(a7)', 5)
    conn.hset('zqq:score', 'ObjectID(a8)', 4)
    # conn.hset('zqq:score', 'ObjectID(a4)', 2)
    # conn.hset('zqq:score', 'ObjectID(a5)', 5)

    # conn.hset('xzq:score', 'ObjectID(a1)', 4.5)
    conn.hset('xzq:score', 'ObjectID(a2)', 2)
    # conn.hset('xzq:score', 'ObjectID(a3)', 3.5)
    # conn.hset('xzq:score', 'ObjectID(a4)', 2)
    conn.hset('xzq:score', 'ObjectID(a5)', 5)

    # conn.hset('dlrb:score', 'ObjectID(a1)', 4.5)
    # conn.hset('dlrb:score', 'ObjectID(a2)', 5)
    conn.hset('dlrb:score', 'ObjectID(a3)', 4)
    conn.hset('dlrb:score', 'ObjectID(a4)', 5)
    conn.hset('dlrb:score', 'ObjectID(a5)', 5)


def 推荐():
    # 指定数据库
    col = db['user']
    # 获取用户打分列表
    user_keys = [i['username'] + ':score' for i in list(col.find({}, {'_id': 0, 'username': 1}))]
    # 获取文章总数
    article_number = conn.get('article_num')
    li = [0 for i in range(int(article_number))]
    # 建立当前用户打分表
    now_user = 'tty:score'
    now_keys = conn.hkeys(now_user)
    now_li = li.copy()
    for now_key in now_keys:
        score = float(conn.hget(now_user, now_key))
        index = int(now_key[-2]) - 1
        now_li[index] = score
        now_array = np.array(now_li)

    # 建立所有用户打分表
    best_user = 0
    best_cos = 0
    best_articles = []
    for user_key in user_keys:
        if user_key == now_user:
            continue
        tmp_li = li.copy()
        tmp_keys = conn.hkeys(user_key)
        for tmp_key in tmp_keys:
            tmp_score = float(conn.hget(user_key, tmp_key))
            tmp_index = int(tmp_key[-2]) - 1
            tmp_li[tmp_index] = tmp_score
            tmp_array = np.array(tmp_li)
        tmp_cos = cos_sim(now_array, tmp_array)
        if tmp_cos > best_cos:
            best_cos = tmp_cos
            best_user = user_key
            best_articles = tmp_keys
        print(user_key, tmp_cos)
    # 获取最佳用户
    print(best_articles)


lis = list(conn.zscan('hot'))
print([i[0] for i in lis[1][::-1][0:3]])
article_col = db['article']
article = article_col.find_one({'_id': 'ObjectID(a1)'})
print(article)
