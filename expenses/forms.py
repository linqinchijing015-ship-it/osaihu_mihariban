# forms.py — 支出入力フォームの定義

from django import forms
from .models import Expense, nonExpense


class ExpenseForm(forms.ModelForm):
    """支出登録・編集フォーム。
    
    ModelFormが自動でやること:
    - Expenseモデルのフィールドからフォームを生成
    - バリデーション（必須チェック・型チェック）
    - 保存処理
    """
    class Meta:
        model = Expense
        fields = ["name", "amount", "category", "satisfaction", "memo"]  # 表示するフィールド
        widgets = {
            # Bootstrap5のフォームスタイルを適用
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "例: コンビニスイーツ"}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "placeholder": "例: 350"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            # 満足度：1〜5の選択肢
            "satisfaction": forms.Select(attrs={"class": "form-select"}),
            # メモ：自由記述欄
            "memo": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "例: 衝動買いだった"}),
        }

# 追加: 我慢した物の入力フォーム
class nonExpenseForm(forms.ModelForm):
    class Meta:
        model = nonExpense
        fields = ["name", "amount", "category", "endurance", "memo"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "例: コンビニスイーツ"}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "placeholder": "例: 350"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            # 我慢度：1〜5の選択肢
            "endurance": forms.Select(attrs={"class": "form-select"}),
            # メモ：自由記述欄
            "memo": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "例: 衝動買いを我慢した"}),
        }