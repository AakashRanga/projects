from .import views
from django.urls import path


urlpatterns=[
    path('',views.signup),
    path('login/',views.login),
    path('home/',views.home),
    path('update/<int:id>/',views.update),
    path('delete/<int:id>/',views.delete),
    path('mail/<int:id>/',views.mail),
]