from django.urls import path

from accounts import views
from .views.admin_views import *
from .views.views import IndexView,IndexViewclass,RedirectFunc,RedirectToMaktab,api_post_list_view,apitestresponse,PostViewSet,CategoryModelViewSet,CategoryListAPIView, CategoryCustomViewSet
from django.views.generic import TemplateView,RedirectView
from rest_framework.routers import DefaultRouter
app_name="blog"
router=DefaultRouter()
router.register('post',viewset=PostViewSet,basename='post')
router.register('category',viewset=CategoryModelViewSet,basename='category')
urlpatterns = [
    # path('categories/', view=CategoryListAPIView.as_view(), name='category-list'),
    # path('kkk/',view=CategoryListAPIView.as_view(),name="CategoryList" )
    path("categorylist/",view=CategoryListAPIView.as_view(),name="list-category"),
    path("categoryviewset/",view=CategoryCustomViewSet.as_view({"get":"list","post":"create"}),name='CategoryCustomViewSet')
]

urlpatterns += router.urls
