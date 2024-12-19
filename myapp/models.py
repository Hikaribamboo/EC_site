import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


def generate_id_with_date(model, field_name, prefix, length):
    """
    指定されたモデルで日付 + 連番形式のユニークなIDを生成
    :param model: モデルクラス
    :param field_name: IDのフィールド名
    :param prefix: IDのプレフィックス
    :param length: 連番部分の桁数
    """
    today = datetime.date.today().strftime('%Y%m%d')  # YYYYMMDD形式の日付
    prefix_with_date = f"{prefix}{today}"  # プレフィックス + 日付

    # フィルタリングに明示的なフィールド名を使用
    last_instance = model.objects.filter(**{f"{field_name}__startswith": prefix_with_date}).order_by('-id').first()

    if last_instance:
        last_number = int(getattr(last_instance, field_name).split('-')[-1])
    else:
        last_number = 0

    new_number = str(last_number + 1).zfill(length)  # ゼロ埋めして番号を作成
    return f"{prefix_with_date}-{new_number}"


class Product(models.Model):
    product_id = models.CharField(max_length=20, unique=True, editable=False)
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    seller_id = models.IntegerField()

    image1 = models.ImageField(upload_to='product_images/', default='default_images/image_default.png')
    image2 = models.ImageField(upload_to='product_images/', null=True, blank=True)
    image3 = models.ImageField(upload_to='product_images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.product_id:
            self.product_id = generate_id_with_date(Product, 'product_id', 'PRD', 4)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_id


class Users(AbstractUser):
    """
    カスタムユーザーモデル
    """
    # 自動生成されるユーザーID (例: 1219-0011)
    user_id = models.CharField(max_length=20, unique=True, editable=False)

    # 他のユーザー情報
    postal_code = models.CharField(max_length=10, null=True, blank=True)  # 郵便番号
    address_prefecture = models.CharField(max_length=255, null=True, blank=True)  # 都道府県
    address_city = models.CharField(max_length=255, null=True, blank=True)  # 市町村
    address_detail = models.CharField(max_length=255, null=True, blank=True)  # 詳細住所
    phone_number = models.BigIntegerField(null=True, blank=True)  # 電話番号
    credit_card_number = models.BigIntegerField(null=True, blank=True)  # クレジットカード番号
    totp_secret = models.CharField(max_length=32, blank=True, null=True)  # TOTP秘密鍵

    # 保有ポイント残高（デフォルトで1000ポイント）
    points_balance = models.PositiveIntegerField(default=1000)

    def save(self, *args, **kwargs):
        """
        初回保存時に `user_id` を自動生成。
        """
        if not self.user_id:  # まだ `user_id` が設定されていない場合
            self.user_id = generate_id_with_date(Users, 'user_id', '', 4)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        表示用文字列
        """
        return f"{self.user_id} ({self.username})"


class Order(models.Model):
    order_id = models.CharField(max_length=20, unique=True, editable=False)
    product_id = models.CharField(max_length=8)
    buyer_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = generate_id_with_date(Order, 'order_id', 'ORD', 4)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_id


class NotificationPattern(models.Model):
    pattern_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return self.type


class Notification(models.Model):
    notification_id = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pattern = models.ForeignKey(NotificationPattern, on_delete=models.CASCADE)
    variables = models.JSONField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.notification_id:
            self.notification_id = generate_id_with_date(Notification, 'notification_id', 'NOT', 4)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.notification_id
