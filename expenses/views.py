# views.py — Tier 0: 一覧画面のみ
# Tier 1 で CreateView / UpdateView / DeleteView を同じパターンで追加していく

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Expense, nonExpense
from .forms import ExpenseForm, nonExpenseForm

class ExpenseListView(ListView):
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

class ExpenseCreateView(CreateView):
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

    
class ExpenseUpdateView(UpdateView):
    """支出を編集するView。
    
    UpdateViewが自動でやること:
    - 指定されたidのデータを取得してフォームに表示
    - POSTリクエスト → バリデーションして更新
    """
    model = Expense
    form_class = ExpenseForm
    template_name = "expenses/expense_form.html"
    success_url = reverse_lazy("expenses:list")

class ExpenseDeleteView(DeleteView):
    """支出を削除するView。
    
    DeleteViewが自動でやること:
    - 確認画面を表示
    - POSTリクエスト → 削除して success_url へ
    """
    model = Expense
    template_name = "expenses/expense_confirm_delete.html"
    success_url = reverse_lazy("expenses:list")

class nonExpenseListView(ListView):
    """我慢した物の一覧を表示する View。構成は ExpenseListView と同じ。
    """
    model = nonExpense
    template_name = "expenses/nonexpense_list.html"
    context_object_name = "nonexpenses"

class nonExpenseCreateView(CreateView):
    """我慢した物を新規登録するView。構成は ExpenseCreateView と同じ。
    """
    model = nonExpense
    form_class = nonExpenseForm
    template_name = "expenses/nonexpense_form.html"
    success_url = reverse_lazy("expenses:non_list")  # 保存後に我慢ログ一覧へ

class nonExpenseUpdateView(UpdateView):
    """我慢した物を編集するView。構成は ExpenseUpdateView と同じ。
    """
    model = nonExpense
    form_class = nonExpenseForm
    template_name = "expenses/nonexpense_form.html"
    success_url = reverse_lazy("expenses:non_list")

class nonExpenseDeleteView(DeleteView):
    """我慢した物を削除するView。構成は ExpenseDeleteView と同じ。
    """
    model = nonExpense
    template_name = "expenses/nonexpense_confirm_delete.html"
    success_url = reverse_lazy("expenses:non_list")