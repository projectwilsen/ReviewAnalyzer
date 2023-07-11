from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('getoutput',views.getoutput, name = "getoutput"),
    path('chat',views.chat,name = "chat"),
    path('login/', views.loginpage, name='login'),
    path('signup/', views.signuppage, name='signup'),
    path('logout/', views.logoutpage, name='logout'),
]