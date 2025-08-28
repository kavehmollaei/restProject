from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
# Create your views here.

def sample(request,category):
    return HttpResponse(f"Showing products in category: {category}")




