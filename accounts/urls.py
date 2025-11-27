from django.urls import path
from .views import sample
from . import views
from rest_framework.authtoken.views import ObtainAuthToken

app_name= "api-v1"

urlpatterns = [
    path('test/<str:category>',view=sample,name="sample_name"),
#registration
    path("registration/",view=views.RegistrationApiView.as_view(),name="Registration"),
#logout
    path("logout/",view=views.LogoutApiView.as_view(),name="Logout"),
    path("login",view=ObtainAuthToken.as_view(),name='token-login')
# change password
# reset password
#login token
# login jwt

]