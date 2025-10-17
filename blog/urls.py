from django.urls import path
from .views.admin_views import *
from .views.views import IndexView,IndexViewclass,RedirectFunc,RedirectToMaktab,api_post_list_view,apitestresponse,PostViewSet,CategoryModelViewSet,CategoryListAPIView
from django.views.generic import TemplateView,RedirectView
from rest_framework.routers import DefaultRouter
app_name="blog"
router=DefaultRouter()
router.register('post',viewset=PostViewSet,basename='post')
router.register('category',viewset=CategoryModelViewSet,basename='category')
urlpatterns = [
    path('categories/', view=CategoryListAPIView.as_view(), name='category-list'),
    path('kkk/',view=CategoryListAPIView.as_view(),name="CategoryList" )
]

urlpatterns += router.urls
