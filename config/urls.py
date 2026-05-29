"""URL configuration for kakeibo-regret."""

from django.contrib import admin
from django.urls import include, path  # include を追加

urlpatterns = [
    path("admin/", admin.site.urls),
    # expenses アプリの URL を /expenses/ 以下に接続
    # namespace="expenses" により {% url 'expenses:list' %} で参照できる
    path("expenses/", include("expenses.urls", namespace="expenses")),
]
