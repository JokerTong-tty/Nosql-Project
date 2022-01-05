from django.shortcuts import render, HttpResponse
from django.http import HttpResponse, JsonResponse
from .neo_demo.chatbot_graph import ChatBotGraph
import datetime
import pymongo

client = pymongo.MongoClient("10.132.221.201", 27017)
db = client['nosql']
handler = ChatBotGraph()
print('准备就绪')


def chat(request):
    return render(request, 'answer/chat.html')


# Create your views here.
def get_answer(request, question):
    print(question)
    answer = handler.chat_main(question)
    print(answer)
    print('*' * 50)
    timespend = {
        'timespend': datetime.datetime.now(),
        'answer': answer
    }
    col = db['answer']
    col.insert_one({'question': question, 'answer': answer,
                    'username': request.session.get('username'),
                    'ask_time': datetime.datetime.now()})
    response = JsonResponse(timespend)
    return response
