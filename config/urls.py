"""URL configuration for kakeibo-regret."""

from django.contrib import admin
from django.urls import include, path 
from django.views.generic import RedirectView  # 追加
from expenses.views import RegisterView

urlpatterns = [
    path("admin/", admin.site.urls),
    # expenses アプリの URL を /expenses/ 以下に接続
    # namespace="expenses" により {% url 'expenses:list' %} で参照できる
    path("expenses/", include("expenses.urls", namespace="expenses")),
    #ログイン・ログアウトのURL
    path("accounts/", include("django.contrib.auth.urls")),
    # ユーザー登録URL
    path("accounts/register/", RegisterView.as_view(), name="register"),

        # トップページ（/）にアクセスしたらログイン画面に飛ばす
    path("", RedirectView.as_view(url="/accounts/login/")),

  
]
