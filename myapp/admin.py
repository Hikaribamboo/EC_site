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

# カスタムユーザーモデルを管理画面に登録
class CustomUserAdmin(UserAdmin):
    model = Users

    # 管理画面に表示するフィールドをカスタマイズ
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('user_id', 'postal_code', 'address_prefecture',
                                     'address_city', 'address_detail', 'phone_number',
                                     'credit_card_number', 'totp_secret')}),
    )

    # 新規追加時に表示するフィールド
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('postal_code', 'address_prefecture', 'address_city',
                                     'address_detail', 'phone_number', 'credit_card_number',
                                     'totp_secret')}),
    )

    # リスト表示時に表示するフィールド
    list_display = ('username', 'email', 'is_staff', 'is_active', 'phone_number')

    # 'user_id' を非編集フィールドとして設定
    readonly_fields = ('user_id',)

# カスタムユーザーモデルを登録
admin.site.register(Users, CustomUserAdmin)

