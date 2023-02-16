from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home),
    path('se/',views.se),
    path('about/',views.about),
    path('user_login/',views.login_view),
    path('user_logout/',views.user_logout),
    path('login_page/',views.signup),
    path('admin_home/',views.admin_home),
    path('users_home/',views.admin_home),
    path('allow_users/',views.allow_users),
    path('message_/', views.frontpage),
    path('signup/', views.m_signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('approve/<int:id>/',views.approve),
    path('reject/<int:id>/',views.reject),
    path('delete_users/<int:id>/',views.delete_users),
    path('robot_home/',views.robot_home),
    path('un_users/',views.un_users),
    path('ano_users/',views.ano_users),
    path('release/',views.release),
    path('security_login/',views.security_login),
    path('security_home/',views.security_home),
    path('ex_intru/',views.security_ex_intru),
    path('in_acc/',views.security_in_acc),
    path('sec_acc/',views.security_sec_acc),
    path('inti_sec/<int:id>/',views.intimate_to_sec),
    path('del_intru/<int:id>/',views.delete_INTRUDERS),
    path('in_push/<int:id>/',views.in_push),
    path('chat_bot/', views.chatbot_response, name='chatbot_response'),
    path('fall_in/<int:id>/', views.fall_in),

]

