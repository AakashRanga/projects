from django.urls import path
from .import views

urlpatterns=[
    path('',views.home),
    path('process_signup/',views.process_signup),
    path('process_login/',views.process_login),
    path('process_home/',views.process_home),
    path('process_logout/',views.process_logout),
    path('get_input/<int:id>/', views.get_input),

    path('prediction/',views.prediction_),
    path('view_predction/',views.view_predction),
    path('send_admin_team/<int:id>/', views.send_admin_team),
    path('send_view_predction/',views.send_view_predction),

    path('get_manufacturing/',views.get_manufacturing),
    path('get_manufacturing_team/<int:id>/',views.get_manufacturing_team),
    path('snd_manufacturing_team/',views.snd_manufacturing_team),

]