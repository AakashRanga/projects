from django.urls import path
from .import views

urlpatterns=[
    path('',views.home),
    path('admin_login/',views.admin_login),
    path('about/',views.about),
    path('admin_home/',views.admin_home),
    path('admin_logout/',views.admin_logout),
    path('company_details/',views.access_domain_team),
    path('prediction_d/',views.prediction_detail),
    path('send_process_team/<int:id>/', views.send_process_team),
    path('process_details/',views.process_details),
    path('send_manufac_team/<int:id>/',views.send_manufacturing_team),
    path('s_manufacturing_team/',views.s_manufacturing_team),
    path('pay_slip/',views.pay_slip),
    path('notify/',views.notify_user),


]