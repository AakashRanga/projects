from django.urls import path
from .import views

urlpatterns=[
    path('',views.home),
    path('contact/',views.contact),
    path('signup/',views.signup),
    path('login/',views.login),
    path('about/',views.about),
    path('client_contact/',views.contact),
    path('client_home/',views.client_home),
    path('newproduct/', views.newproduct),
    path('product_looking_for/',views.product_looking_for),
    path('cient_logout/', views.client_logout),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('store/', views.store),
    path('cart/',views.cart),
    path('checkout/',views.checkout),
    path('purchase/',views.purchase),
    path('purchased/',views.purchased),
    path('specific_product/',views.product_specification),
    path('manu_t/',views.manu_team),
    path('payment/',views.payment),
    path('c_mail/<int:id>/',views.c_mail),

]
