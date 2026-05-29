# views.py — Tier 0: 一覧画面のみ
# Tier 1 で CreateView / UpdateView / DeleteView を同じパターンで追加していく

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Expense
from .forms import ExpenseForm

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
