from django.shortcuts import render, HttpResponse, redirect, reverse
from django.http import HttpResponse, JsonResponse
import pymongo
import redis
import numpy as np

conn = redis.StrictRedis(db=5, host='10.132.221.201', decode_responses=True)
client = pymongo.MongoClient("10.132.221.201", 27017)
db = client['nosql']


def index(request):
    col = db['answer']
    questions = list(
        col.find({}, {"_id": 0, 'ask_time': 1, "question": 1, 'answer': 1}).sort('ask_time', -1).limit(
            10))
    doctor_col = db['doctor']
    article_col = db['article']
    doctors = list(
        doctor_col.find().sort('register_time', -1).limit(
            8))
    #  获取推荐文章
    best_articles = get_best_articles(request)
    articles = []
    for article_id in best_articles:
        articles.append(article_col.find_one({'article_id': article_id}))
    # 获取热门文章
    hots = []
    hot_li = list(conn.zscan('hot'))
    hot_ids = [i[0] for i in hot_li[1][::-1][0:3]]
    for article_id in hot_ids:
        hots.append(article_col.find_one({'article_id': article_id}))
    context = {
        'questions': questions,
        'doctors': doctors,
        'articles': articles,
        'hots': hots,
    }
    return render(request, 'user/index.html', context=context)


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)
        if username and password:
            col = db['user']
            result = list(col.find({'username': username}, {"_id": 0, "password": 1}))
            if result:
                if password == result[0]['password']:
                    request.session['username'] = username
                    return redirect(reverse('user:index'))
                else:
                    print('密码错误')
                    request.session['username'] = ''
                    return render(request, 'user/login.html')
            else:
                print('用户名不存在')
                request.session['username'] = ''
                return render(request, 'user/login.html')
    return render(request, 'user/login.html')


def star_doctor(request, doctor_id):
    '''
    当前用户关注医生的事件
    :param request:
    :param doctor_id:
    :return:
    '''
    username = request.session.get('username')
    stars_list = conn.lrange(f'{username}:stars', 0, conn.llen(f'{username}:stars'))
    if doctor_id in stars_list:
        print('已经关注')
        response = JsonResponse({'flag': 0})
        return response
    else:
        conn.lpush(f"{username}:stars", doctor_id)
        # TODO mongodb中医生的关注量 + 1
        doctor_col = db['doctor']
        tmp = doctor_col.find_one({'_id': doctor_id})
        star = tmp['stars']
        star = int(star) + 1
        print('关注成功:', doctor_id)
        doctor_col.update_one({'_id': doctor_id}, {'$set': {'stars': star}})
        response = JsonResponse({'flag': 1})
        return response


def list_star(request):
    '''
    返回当前用户的关注医生列表
    :param request:
    :return:
    '''
    doctor_col = db['doctor']
    username = request.session.get('username')
    list_len = conn.llen(f"{username}:stars")
    doc_id_list = conn.lrange(f"{username}:stars", 0, list_len)

    doctors = []
    for doc_id in doc_id_list:
        doctors.append(doctor_col.find_one({'doc_id': doc_id}))
    print(doc_id_list)
    return render(request, 'user/star_doctors.html', context={'doctors': doctors})


def register(request):
    return render(request, 'user/register.html')


# 余弦相似度计算
def cos_sim(a, b):
    a_norm = np.linalg.norm(a)
    b_norm = np.linalg.norm(b)
    cos = np.dot(a, b) / (a_norm * b_norm)
    return cos


def get_best_articles(request):
    username = request.session.get('username')
    if not username:
        username = 'tty'
    # 指定数据库
    col = db['user']
    # 获取用户打分列表
    user_keys = [i['username'] + ':score' for i in list(col.find({}, {'_id': 0, 'username': 1}))]
    # 获取文章总数
    article_number = conn.get('article_num')
    li = [0 for i in range(int(article_number))]
    # 建立当前用户打分表
    now_user = f'{username}:score'
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
    return best_articles


def article(request, id):
    article_col = db['article']
    article = article_col.find_one({'_id': id})
    context = {
        'article': article,
        'hot': int(conn.get(f'{id}:hot'))

    }
    return render(request, 'user/single(1).html', context=context)
