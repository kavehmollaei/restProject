from django.shortcuts import render
from django.http import HttpResponse
from time import sleep
# Create your views here.
from modelTamrin.celery import app


@app.task
def my_task():
    sleep(10)
    open('test.txt','w').close()


def home(request):
    print("fdfffff")
    my_task.delay()

    return HttpResponse("Hello")

