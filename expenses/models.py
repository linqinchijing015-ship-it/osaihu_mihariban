from django.db import models

# models.py — 支出を表すモデルの定義
class Expense(models.Model):
    CATEGORY_CHOICES = [
        ("food",    "食費・日用品"),
        ("apparel", "衣服・書籍"),
        ("gadget",  "ガジェット・趣味"),
        ("luxury",  "嗜好品・課金・コンビニ"),
    ]

    name = models.CharField(max_length=100, verbose_name="品名")
    amount = models.PositiveIntegerField(verbose_name="金額（円）")
    category = models.CharField(
        max_length=16,
        choices=CATEGORY_CHOICES,
        verbose_name="カテゴリ",
    )
    # 次フェーズで scoring.py が埋める
    regret_score = models.FloatField(
        null=True,
        blank=True,
        verbose_name="後悔スコア",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日時")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "支出"
        verbose_name_plural = "支出一覧"

    def __str__(self):
        return f"{self.name} ({self.amount}円)"
    

# 追加: 我慢した物を表すモデル
class nonExpense(models.Model):
    CATEGORY_CHOICES = [
        ("food",    "食費・日用品"),
        ("apparel", "衣服・書籍"),
        ("gadget",  "ガジェット・趣味"),
        ("luxury",  "嗜好品・課金・コンビニ"),
    ]

    name = models.CharField(max_length=100, verbose_name="品名")
    amount = models.PositiveIntegerField(verbose_name="金額（円）")
    category = models.CharField(
        max_length=16,
        choices=CATEGORY_CHOICES,
        verbose_name="カテゴリ",
    )
    self_control_score = models.FloatField(
        null=True,
        blank=True,
        verbose_name="自己制御スコア",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日時")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "我慢した物"
        verbose_name_plural = "我慢した物一覧"

    def __str__(self):
        return f"{self.name} ({self.amount}円)"