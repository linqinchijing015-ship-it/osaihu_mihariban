# urls.py — expenses アプリ内の URL ルーティング
# app_name を設定することで {% url 'expenses:list' %} のように名前空間付きで参照できる

from django.urls import path

from . import views

app_name = "expenses"

urlpatterns = [
    # /expenses/ → 一覧画面（Tier 0）
    path("", views.ExpenseListView.as_view(), name="list"),

     # /expenses/add/ → 新規作成画面
    # name="add" とすることで {% url 'expenses:add' %} で参照できる
    path("add/", views.ExpenseCreateView.as_view(), name="add"),

    # /expenses/1/edit/ → 編集画面
    # <int:pk> は「整数のid」を受け取るという意味
    # pkはprimary key（主キー）の略でDBのidと対応している
    path("<int:pk>/edit/", views.ExpenseUpdateView.as_view(), name="edit"),

    # /expenses/1/delete/ → 削除確認画面
    path("<int:pk>/delete/", views.ExpenseDeleteView.as_view(), name="delete"),

    # 追加: 我慢した物のURLパターン,構成は上記と同じ
    path("non/",                views.nonExpenseListView.as_view(),   name="non_list"),
    path("non/add/",            views.nonExpenseCreateView.as_view(), name="non_add"),
    path("non/<int:pk>/edit/",  views.nonExpenseUpdateView.as_view(), name="non_edit"),
    path("non/<int:pk>/delete/",views.nonExpenseDeleteView.as_view(), name="non_delete"),
]
