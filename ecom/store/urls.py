# store/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'), 
    path('register/', views.register, name='register'),               
    path('login/', views.login_user, name='login'),                   
    path('logout/', views.logout_user, name='logout'),                
    path('add-product/', views.add_product, name='add_product'),      
    path('edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    path('place-order/<int:product_id>/', views.place_order, name='place_order'),
    path('order-success/', views.order_success, name='order_success'), 
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]
