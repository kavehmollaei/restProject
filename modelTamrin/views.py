from django.shortcuts import render
from django.http import HttpResponse
from time import sleep
# Create your views here.
from modelTamrin.celery import app
from modelTamrin.tasks import add


@app.task
def my_task():
    sleep(10)
    open('test.txt','w').close()


def home(request):
    print("fdfffff")
    my_task.delay()
    result=add.delay(10,20)
    print(result.status)
    print(result.ready())
    print(result.get())
    print(result.status)
    


    return HttpResponse("Hello")

