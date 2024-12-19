from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Product, Notification, Users
import pyotp
import qrcode
from io import BytesIO
import base64


User = get_user_model()  # カスタムユーザーモデルを取得

def main_page(request):
    registration_success = request.session.pop('registration_success', False)
    return render(request, 'main.html', {
        'registration_success': registration_success
    })

def admin_product_list(request):
    products = Product.objects.all()
    return render(request, 'myapp/admin_product_list.html', {'products': products})

def delete_product(request, product_id):
    # 削除対象の商品を取得
    product = get_object_or_404(Product, product_id=product_id)
    product.delete()  # 商品を削除
    return redirect('admin_product_list')  # 管理者用商品リストにリダイレクト

def product_list_user(request):
    products = Product.objects.filter(stock__gt=0)  # 在庫がある商品のみ表示
    return render(request, 'myapp/product_list_user.html', {'products': products})

@login_required
def notification_list(request):
    """
    ログイン中のユーザーに関連する通知を取得し、通知一覧画面を表示するビュー
    """
    # ログイン中のユーザーの通知を取得
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    # コンテキストに通知データを渡してテンプレートをレンダリング
    return render(request, 'notification_list.html', {'notifications': notifications})

def custom_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('main')  # ログイン成功後にメイン画面へ
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})
    return render(request, 'login.html')

def custom_logout(request):
    logout(request)
    return redirect('login')  # ログアウト後、ログイン画面へリダイレクト

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

            # TOTP用シークレットキーを生成しセッションに保存
            secret = pyotp.random_base32()
            request.session['totp_secret'] = secret

        # ユーザーを作成し、デフォルトポイントを設定
        User = get_user_model()
        user = User.objects.create_user(
            username=username,
            password=password,
            totp_secret=secret,
            points_balance=1000  # デフォルトで 1000 ポイント
        )
        
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
            user = User.objects.create_user(username=username, password=password)
            login(request, user)

            # セッションデータをクリア
            request.session.flush()
            return redirect('main')  # メイン画面にリダイレクト

        else:
            return render(request, 'register.html', {
                'error': 'Invalid OTP. Please try again.',
            })

    return redirect('register')


def product_add(request):
    return render(request, 'product_add.html')  # 出品ページのテンプレートを作成

def mypage(request):
    return render(request, 'mypage.html')  # マイページのテンプレートを作成

def notifications(request):
    return render(request, 'notifications.html')  # 通知ページのテンプレートを作成


