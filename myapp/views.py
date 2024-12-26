from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Product, Notification, Users
import pyotp
import qrcode
from io import BytesIO
import base64
import sys
from django.contrib import messages  # メッセージ表示用

User = get_user_model()

def main_page(request):
    registration_success = request.session.pop('registration_success', False)
    return render(request, 'main.html', {
        'registration_success': registration_success,
    })

    # セッションにシークレットキーを一時保存
# セッションにシークレットキーを一時保存
def register(request):
    if request.method == 'POST':
        username = request.session.get('username')
        password = request.session.get('password')
        secret = request.session.get('totp_secret')

        if not (username and password and secret):  # 初回の場合
            username = request.POST.get('username')
            password = request.POST.get('password')

            # セッションにユーザー情報を保存
            request.session['username'] = username
            request.session['password'] = password

            # ユーザー名の重複チェック
            User = get_user_model()
            if User.objects.filter(username=username).exists():
                messages.error(request, 'このユーザー名は既に登録されています。別の名前をお試しください。')
                return render(request, 'register.html')

            # TOTP用シークレットキーを生成しセッションに保存
            secret = pyotp.random_base32()
            request.session['totp_secret'] = secret

        # デバッグ用出力
        print("Username:", username)
        print("Password:", password)
        print("TOTP Secret:", secret)

        # 有効期限を1分（60秒）に設定
        totp = pyotp.TOTP(secret, interval=60)

        # QRコードを生成
        qr_code_data = totp.provisioning_uri(name=username, issuer_name="ECサイト")
        qr_image = qrcode.make(qr_code_data)

        # 画像をBase64に変換
        buffer = BytesIO()
        qr_image.save(buffer, format="PNG")
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

        # 登録成功モーダル表示用フラグをセッションに保存
        request.session['registration_success'] = True

        return render(request, 'register.html', {
            'qr_code_url': f"data:image/png;base64,{qr_code_base64}",
        })

    return render(request, 'register.html')

def verify_qr(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        secret = request.session.get('totp_secret')

        if not secret:  # セッションにシークレットがない場合はエラー
            return redirect('register')

        totp = pyotp.TOTP(secret, interval=60)
        if totp.verify(otp):  # TOTPの検証
            # ユーザー登録処理
            username = request.session.get('username')
            password = request.session.get('password')

            # ユーザー名の重複チェック
            User = get_user_model()
            if User.objects.filter(username=username).exists():
                return render(request, 'register.html', {
                    'error': 'このユーザー名は既に登録されています。別の名前をお試しください。',
                })

            user = User.objects.create_user(username=username, password=password)
            login(request, user)

            # `registration_success` をセッションに保存
            request.session['registration_success'] = True

            # セッションデータの一部を残す
            request.session['username'] = username  # 必要に応じて保持する
            return redirect('main')  # メイン画面にリダイレクト

        else:
            return render(request, 'register.html', {
                'error': 'Invalid OTP. Please try again.',
            })

    return redirect('register')



@login_required
def admin_product_list(request):
    products = Product.objects.all()
    return render(request, 'myapp/admin_product_list.html', {'products': products})


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    product.delete()
    return redirect('admin_product_list')


@login_required
def product_list_user(request):
    products = Product.objects.filter(stock__gt=0)
    return render(request, 'myapp/product_list_user.html', {'products': products})


@login_required
def product_add(request):
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        category = request.POST.get('category')
        size = request.POST.get('size')
        stock = request.POST.get('stock')
        image = request.FILES.get('image')

        # ログイン中のユーザーを出品者として登録
        seller_id = request.user.id

        # Product モデルに登録
        product = Product(
            name=name,
            price=price,
            stock=stock,
            seller_id=seller_id,
            image1=image,  # 最初の画像を使用
            category=category,
            size=size
        )
        product.save()

        # 出品完了後にリダイレクト
        return redirect('main')  # メインページへリダイレクト

    return render(request, 'product_add.html')


def custom_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})
    return render(request, 'login.html')


def custom_logout(request):
    logout(request)
    return redirect('main')


@login_required
def mypage(request):
    return render(request, 'mypage.html')


@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': notifications})

@login_required
def selling_products(request):
    selling_products = Product.objects.filter(seller_id=request.user.id, is_sold=False)
    return render(request, 'selling_products.html', {'selling_products': selling_products})

@login_required
def selling_detail(request, product_id):
    product = get_object_or_404(Product, product_id=product_id, seller_id=request.user.id)
    return render(request, 'selling_detail.html', {'product': product})
@login_required
def sold_products(request):
    sold_products = Product.objects.filter(seller=request.user, is_sold=True)
    return render(request, 'sold.html', {'sold_products': sold_products})


@login_required
def favorite_products(request):
    favorite_products = Product.objects.filter(favorites=request.user)
    return render(request, 'favorite_products.html', {'favorite_products': favorite_products})


@login_required
def purchase_history(request):
    purchases = [
        {"name": "商品C", "price": 1500, "date": "2024-12-18"},
        {"name": "商品D", "price": 3000, "date": "2024-12-17"},
    ]
    return render(request, 'purchase_history.html', {'purchases': purchases})


@login_required
def account_management(request):
    user = request.user
    return render(request, 'account_management.html', {'user': user})

def product_confirm(request):
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        category = request.POST.get('category')
        size = request.POST.get('size')
        stock = request.POST.get('stock')
        image = request.FILES.get('image')

        if not (name and price and stock and image):
            return render(request, 'product_add.html', {'error_message': 'すべての必須項目を入力してください。'})

        # 画像をセッションに一時保存
        request.session['temp_image'] = image.name
        request.session['temp_data'] = {
            'name': name,
            'price': price,
            'category': category,
            'size': size,
            'stock': stock,
        }

        context = {
            'name': name,
            'price': price,
            'category': category,
            'size': size,
            'stock': stock,
            'image_url': f"/media/product_images/{image.name}",
        }
        return render(request, 'product_confirm.html', context)

    return redirect('product_add')

def product_add_confirmed(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        category = request.POST.get('category')
        size = request.POST.get('size')
        stock = request.POST.get('stock')
        image = request.session.get('temp_image')  # セッションから画像データを取得

        seller_id = request.user.id

        Product.objects.create(
            name=name,
            price=price,
            category=category,
            size=size,
            stock=stock,
            image1=image,  # セッションから取得した画像を保存
            seller_id=seller_id
        )

        # セッションから一時データを削除
        request.session.pop('temp_image', None)
        request.session.pop('temp_data', None)

        return redirect('main')
    return redirect('product_add')


