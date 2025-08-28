from django.urls import path
from .views.admin_views import *
from .views.views import IndexView,IndexViewclass,RedirectFunc,RedirectToMaktab,api_post_list_view,apitestresponse,PostList,PostDetail,PostViewSet,CategoryModelViewSet
from django.views.generic import TemplateView,RedirectView
from rest_framework.routers import DefaultRouter
app_name="blog"
router=DefaultRouter()
router.register('post',viewset=PostViewSet,basename='post')
router.register('category',viewset=CategoryModelViewSet,basename='category')
urlpatterns = [

    path('mypost/',view=index,name="index"),
    path('mypostlist',view=PostListView.as_view(),name="mypostlist"),
    path('mypost/<int:pk>',view=mypostdetailview.as_view(),name="mypostdetail"),
    path('ticket/',view=ticket,name='ticket')
]

# urlpatterns += router.urls
# urlpatterns = [
#       # path('post/',view=PostList.as_view(),name="api-post-list"),
#       path('postapi/',view=apitestresponse,name="api-test"),
#       # path('post/<int:id>/',view=PostDetail.as_view(),name="post-details"),
#       path('post/',view=PostViewSet.as_view({'get':'list'}),name='post-list'),
#       path('post/<int:id>/',view=PostViewSet.as_view({'get':'retrieve'}),name='post-list')

# #     path('fbv',view=IndexView,name="func-test-view"),
# #     # path('cbv/',TemplateView.as_view(template_name='index.html',extra_context={'name':"kaveh"})),
# #     path('cbv/',view=IndexViewclass.as_view(),name="IndexViewClass"),
# #     # path('go-to-cbv',RedirectView.as_view(pattern_name="blog:IndexViewClass"),name="gotocvb")
# #     # path('go-to-cbv',view=RedirectFunc,name="redirect")
# #     path('go-to-maktab/<int:pk>',view=RedirectToMaktab.as_view(),name='redirectto maktab')
# ]