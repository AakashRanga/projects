from django.urls import path
from .import views

urlpatterns=[
    path('attacker_home/',views.attacker_home),
    path('hacked_details/',views.user_details),
    path('ha_login/',views.hacker_login),
    path('ha_l/<int:id>/',views.update)
]