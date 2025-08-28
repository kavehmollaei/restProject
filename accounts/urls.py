from django.urls import path
from .views import sample
urlpatterns = [
    path('test/<str:category>',view=sample,name="sample_name"),
]