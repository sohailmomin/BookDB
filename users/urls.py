from django.urls import path,re_path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('',views.user_list,name='user_list'),
    re_path(r'^(?P<username>[-\w]+)/$',views.user_detail,name='user_detail'),
    path('user/follow',views.user_follow,name='user_follow'),
    path('dashboard/dashboard/',views.dashboard,name='dashboard'),
]