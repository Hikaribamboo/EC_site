#urls.py
from django.urls import path
from django.contrib.auth.views import LoginView  # LoginViewのインポート
from . import views

urlpatterns = [
    # 空のパスをメイン画面にリダイレクト
    path('', views.main_page, name='main'),

    # 管理者用
    path('products/admin/', views.admin_product_list, name='admin_product_list'),  # 管理者用商品リスト
    path('products/delete/<str:product_id>/', views.delete_product, name='delete_product'),  # 商品削除
    path('product/add/', views.product_add, name='product_add'),  # 出品ページ

    # 一般ユーザー用
    path('products/', views.product_list_user, name='product_list_user'),  # 商品リスト
    path('main/', views.main_page, name='main'),  # メイン画面
    
    # ログイン用
    path('login/', views.custom_login, name='login'),  # ログイン画面
    path('logout/', views.custom_logout, name='logout'),  # ログアウト画面

    path('register/', views.register, name='register'),
    path('verify_qr/', views.verify_qr, name='verify_qr'),

    path('mypage/', views.mypage, name='mypage'),  # マイページ
    path('notifications/', views.notifications, name='notifications'),  # 通知ページ
]






