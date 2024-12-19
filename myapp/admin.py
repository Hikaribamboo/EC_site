from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Product, Order, NotificationPattern, Notification, Users

# 商品モデルを登録
admin.site.register(Product)

# Orderモデルを登録
admin.site.register(Order)

# Notificationモデルを登録
admin.site.register(NotificationPattern)
admin.site.register(Notification)

# ユーザーモデルを管理画面にカスタマイズして登録
class CustomUserAdmin(UserAdmin):
    model = Users
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': (
                'points_balance', 
                'postal_code', 
                'address_prefecture', 
                'address_city', 
                'address_detail', 
                'phone_number', 
                'credit_card_number'
            )
        }),
    )
    list_display = (
        'user_id',  # ユーザーIDを表示
        'username', 
        'email', 
        'is_staff', 
        'is_active', 
        'points_balance'
    )
    readonly_fields = ('user_id',)  # ユーザーIDを編集不可に設定

admin.site.register(Users, CustomUserAdmin)


