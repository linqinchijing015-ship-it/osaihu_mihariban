# urls.py — expenses アプリ内の URL ルーティング
# app_name を設定することで {% url 'expenses:list' %} のように名前空間付きで参照できる

from django.urls import path

from . import views

app_name = "expenses"

urlpatterns = [
    # /expenses/ → 一覧画面（Tier 0）
    path("", views.ExpenseListView.as_view(), name="list"),
    # Tier 1 で path("add/", ..., name="add") などをここに追加していく
]
