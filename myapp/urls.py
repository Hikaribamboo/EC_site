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

    # マイページと通知ページ
    path('mypage/', views.mypage, name='mypage'),  # マイページ
    path('notifications/', views.notifications, name='notifications'),  # 通知ページ
    path('product/add/', views.product_add, name='product_add'),  # 出品ページ

    #マイページ関連
    path('selling_products/', views.selling_products, name='selling_products'),  # 出品中
    path('selling_products/<str:product_id>/', views.selling_detail, name='selling_detail'),


    path('sold_products/', views.sold_products, name='sold_products'),  # 販売履歴
    path('purchase_history/', views.purchase_history, name='purchase_history'),  # 購入履歴
    path('account_management/', views.account_management, name='account_management'),  # アカウント管理
    path('favorite_products/', views.favorite_products, name='favorite_products'),  # お気に入り商品のURL

    #出品関連
    path('product/add/', views.product_add, name='product_add'),
    path('product/confirm/', views.product_confirm, name='product_confirm'),
    path('product/add/confirmed/', views.product_add_confirmed, name='product_add_confirmed'),
]







