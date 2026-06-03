# views.py — Tier 0: 一覧画面のみ
# Tier 1 で CreateView / UpdateView / DeleteView を同じパターンで追加していく

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic import CreateView
from django.db.models import Sum
import json

from .models import Expense, nonExpense, CATEGORY_COLORS
from .forms import ExpenseForm, nonExpenseForm


def _category_chart_json(queryset, category_choices):
    """カテゴリ別の合計金額を、円グラフ用の JSON 文字列にして返す。

    - 金額が 0 のカテゴリは凡例がうるさくなるので除外する
    - ラベルは choices の表示名（例: "食費・日用品"）を使う
    - 色は CATEGORY_COLORS でカテゴリごとに固定し、ラベルと同じ並びで渡す
    - 返り値はテンプレートで {{ chart_data|safe }} として Chart.js に渡す
    """
    # {カテゴリコード: 表示名} の対応表
    label_map = dict(category_choices)
    # カテゴリごとに金額を合計。
    # 注意: モデルの Meta.ordering（-created_at）が GROUP BY に混入すると
    # 「category, created_at」でグループ化され、同カテゴリが日時ごとに分割されて
    # 円グラフに同色の重複スライスが出る。.order_by() で並びを消してから集計する。
    rows = queryset.order_by().values("category").annotate(total=Sum("amount"))
    labels, values, colors = [], [], []
    for row in rows:
        if not row["total"]:
            continue
        code = row["category"]
        labels.append(label_map.get(code, code))
        values.append(row["total"])
        colors.append(CATEGORY_COLORS.get(code, "#9ca3af"))  # 未知カテゴリは灰
    return json.dumps(
        {"labels": labels, "values": values, "colors": colors},
        ensure_ascii=False,
    )

class ExpenseListView(LoginRequiredMixin, ListView):
    """支出一覧を表示する View。

    ListView が自動でやること:
    - Expense.objects.all() を取得（Meta.ordering が効くので降順）
    - context_object_name で指定した名前でテンプレートに渡す
    - template_name のテンプレートをレンダリングして返す
    """

    model = Expense
    template_name = "expenses/expense_list.html"
    # テンプレート内で {{ expenses }} として参照できる
    context_object_name = "expenses"

    def get_context_data(self, **kwargs):
        # 上部の集計バー用に「合計金額」を渡す（件数はテンプレート側で |length）
        context = super().get_context_data(**kwargs)
        # Sum は該当行が0件のとき None を返すので、その場合は 0 にそろえる
        context["total_amount"] = self.get_queryset().aggregate(total=Sum("amount"))["total"] or 0
        # 対比表示用：我慢で浮いた額（相手タブの合計）
        context["saved_amount"] = nonExpense.objects.aggregate(total=Sum("amount"))["total"] or 0
        # カテゴリ別円グラフ用のデータ（ラベルと金額の配列）を JSON 文字列で渡す
        context["chart_data"] = _category_chart_json(self.get_queryset(), Expense.CATEGORY_CHOICES)
        return context
    def get_queryset(self):
        # self.request.user → 今ログインしているユーザー
        # filter → そのユーザーのデータだけ取得
        return Expense.objects.filter(user=self.request.user)

class ExpenseCreateView(LoginRequiredMixin, CreateView):
    """支出を新規登録するView。
    
    CreateViewが自動でやること:
    - GETリクエスト → フォームを表示
    - POSTリクエスト → バリデーションして保存
    - 保存成功 → success_urlにリダイレクト
    """
    model = Expense
    form_class = ExpenseForm
    template_name = "expenses/expense_form.html"
    success_url = reverse_lazy("expenses:list")  # 保存後に一覧画面へ

    def form_valid(self, form):
        # 保存前にユーザーを自動でセット
        form.instance.user = self.request.user
        return super().form_valid(form)


    
class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    """支出を編集するView。
    
    UpdateViewが自動でやること:
    - 指定されたidのデータを取得してフォームに表示
    - POSTリクエスト → バリデーションして更新
    """
    model = Expense
    form_class = ExpenseForm
    template_name = "expenses/expense_form.html"
    success_url = reverse_lazy("expenses:list")

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)


class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    """支出を削除するView。
    
    DeleteViewが自動でやること:
    - 確認画面を表示
    - POSTリクエスト → 削除して success_url へ
    """
    model = Expense
    template_name = "expenses/expense_confirm_delete.html"
    success_url = reverse_lazy("expenses:list")

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)


class nonExpenseListView(LoginRequiredMixin, ListView):
    """我慢した物の一覧を表示する View。構成は ExpenseListView と同じ。
    """
    model = nonExpense
    template_name = "expenses/nonexpense_list.html"
    context_object_name = "nonexpenses"

    def get_context_data(self, **kwargs):
        # 上部の集計バー用に「我慢して浮いた合計金額」を渡す
        context = super().get_context_data(**kwargs)
        context["total_amount"] = self.get_queryset().aggregate(total=Sum("amount"))["total"] or 0
        # 対比表示用：使った額（相手タブの合計）
        context["spent_amount"] = Expense.objects.aggregate(total=Sum("amount"))["total"] or 0
        # カテゴリ別円グラフ用のデータを JSON 文字列で渡す
        context["chart_data"] = _category_chart_json(self.get_queryset(), nonExpense.CATEGORY_CHOICES)
        return context
    
    def get_queryset(self):
        return nonExpense.objects.filter(user=self.request.user)

class nonExpenseCreateView(LoginRequiredMixin, CreateView):
    """我慢した物を新規登録するView。構成は ExpenseCreateView と同じ。
    """
    model = nonExpense
    form_class = nonExpenseForm
    template_name = "expenses/nonexpense_form.html"
    success_url = reverse_lazy("expenses:non_list")  # 保存後に我慢ログ一覧へ

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class nonExpenseUpdateView(LoginRequiredMixin, UpdateView):
    """我慢した物を編集するView。構成は ExpenseUpdateView と同じ。
    """
    model = nonExpense
    form_class = nonExpenseForm
    template_name = "expenses/nonexpense_form.html"
    success_url = reverse_lazy("expenses:non_list")

    def get_queryset(self):
        return nonExpense.objects.filter(user=self.request.user)


class nonExpenseDeleteView(LoginRequiredMixin, DeleteView):
    """我慢した物を削除するView。構成は ExpenseDeleteView と同じ。
    """
    model = nonExpense
    template_name = "expenses/nonexpense_confirm_delete.html"
    success_url = reverse_lazy("expenses:non_list")

    def get_queryset(self):
        return nonExpense.objects.filter(user=self.request.user)

class RegisterView(CreateView):
    """ユーザー登録View。
    
    UserCreationForm はDjangoが用意しているユーザー登録フォームで
    ユーザー名・パスワード・パスワード確認の3つのフィールドを持つ
    """
    form_class = UserCreationForm
    template_name = "registration/register.html"
    success_url = "/expenses/"

    def form_valid(self, form):
        # 登録成功後に自動でログインさせる
        response = super().form_valid(form)
        login(self.request, self.object)
        return response