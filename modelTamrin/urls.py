from django.urls import path,include
from modelTamrin import views


urlpatterns = [
    path('tamrin/',view=views.home)
]