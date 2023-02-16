from django.urls import path
from .import views

urlpatterns=[
    path('',views.home),
    path('mfta_signup/',views.mfta_signup),
    path('mfta_login/',views.mfta_login),
    path('mfta_home/',views.mfta_home),
    path('mfta_logout/',views.mfta_logout),
    path('appr_product/',views.approve_product),
    path('count_time/',views.count_time),
    path('admin_final/',views.admin_final),
    path('progress_bar/',views.progress_bar),
    path('mail/<int:id>/',views.mail),


]