from django.contrib import admin
from django.urls import path, include  # include をインポート

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),  # myapp の urls.py を参照
]
