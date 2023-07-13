from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('getoutput',views.getoutput, name = "getoutput"),
    path('chat',views.chat,name = "chat"),
    path('login/', views.loginpage, name='login'),
    path('signup/', views.signuppage, name='signup'),
    path('logout/', views.logoutpage, name='logout'),
    path('result/', views.result_list_all),
    path('result/<int:user>', views.result_list_by_user),
    path('result/<int:user>/<int:id>', views.result_details)
    # path('result/<int:user>/<int:videoid>', views.drink_detail)
]