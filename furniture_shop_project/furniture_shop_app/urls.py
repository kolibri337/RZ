from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('goods/', views.list_goods, name='list_goods'),
    path('orders/create/<int:id_good>/', views.create_order, name='create_order'),
    path('confirm_order/<int:order_id>/', views.confirm_order, name='confirm_order'),
    path('orders/', views.list_orders, name='list_orders'),
    path('orders/update/<int:id_order>/', views.update_order, name='update_order'),
    path('orders/delete/<int:id_order>/', views.delete_order, name='delete_order'),
    path('goods/insert/', views.insert_good, name='insert_good'),
    path('goods/update/<int:id_good>/', views.update_good, name='update_good'),
    path('goods/delete/<int:id_good>/', views.delete_good, name='delete_good'),
    path('clients/', views.list_clients, name='list_clients'),
    path('clients/create/', views.create_client, name='create_client'),
    path('clients/update/<int:id_client>/', views.update_client, name='update_client'),
    path('clients/delete/<int:id_client>/', views.delete_client, name='delete_client'),
    path('orders/latest/', views.latest_orders, name='latest_orders'),

    # Аутентификация
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='welcome'), name='logout'),
    path('register/', views.register, name='register'),
]