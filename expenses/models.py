from django.db import models
from django.contrib.auth.models import User  # 追加

# カテゴリコードごとの固定色。買った/我慢どちらの画面でも・並び順が変わっても
# 「食費は常にこの色」になるよう、カテゴリと色を1対1で固定する。
# グラフ（views）とカード左のドット（テンプレート）の両方がこれを参照する。
# B案（ごほうびゲーム）の暖色テーマに合わせ、4カテゴリを「黄→赤」の暖色グラデで配色。
# 嗜好品ほど赤（注意）に寄せ、生活必需品ほど黄（穏やか）にして直感と一致させる。
CATEGORY_COLORS = {
    "food":    "#fbbf24",  # 食費・日用品 = アンバー（穏やか）
    "apparel": "#fb923c",  # 衣服・書籍 = ライトオレンジ
    "gadget":  "#f97316",  # ガジェット・趣味 = オレンジ
    "luxury":  "#dc2626",  # 嗜好品・課金・コンビニ = 赤（注意）
}


# models.py — 支出を表すモデルの定義
class Expense(models.Model):
    CATEGORY_CHOICES = [
        ("food",    "食費・日用品"),
        ("apparel", "衣服・書籍"),
        ("gadget",  "ガジェット・趣味"),
        ("luxury",  "嗜好品・課金・コンビニ"),
    ]

    # ユーザーに紐付けるフィールドを追加
    # on_delete=CASCADE → ユーザーが削除されたら支出データも削除
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="ユーザー",
        null=True,
    )

    name = models.CharField(max_length=100, verbose_name="品名")
    amount = models.PositiveIntegerField(verbose_name="金額（円）")
    category = models.CharField(
        max_length=16,
        choices=CATEGORY_CHOICES,
        verbose_name="カテゴリ",
    )

    #満足度を表すフィールドを追加
    SATISFACTION_CHOICES = [(i, str(i)) for i in range(1, 6)]
    satisfaction = models.IntegerField(
    null=True,
    blank=True,
    choices=SATISFACTION_CHOICES,
    verbose_name="満足度",
    )
    memo = models.TextField(
    blank=True,
    verbose_name="メモ",
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

    @property
    def category_color(self):
        # カード左のドット用。未知カテゴリは灰
        return CATEGORY_COLORS.get(self.category, "#9ca3af")


# 追加: 我慢した物を表すモデル
class nonExpense(models.Model):
    CATEGORY_CHOICES = [
        ("food",    "食費・日用品"),
        ("apparel", "衣服・書籍"),
        ("gadget",  "ガジェット・趣味"),
        ("luxury",  "嗜好品・課金・コンビニ"),
    ]

    # ユーザーに紐付けるフィールドを追加
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="ユーザー",
        null=True,
    )

    name = models.CharField(max_length=100, verbose_name="品名")
    amount = models.PositiveIntegerField(verbose_name="金額（円）")
    category = models.CharField(
        max_length=16,
        choices=CATEGORY_CHOICES,
        verbose_name="カテゴリ",
    )

    #我慢の度合いを表すフィールドを追加
    ENDURANCE_CHOICES = [(i, str(i)) for i in range(1, 6)]

    endurance = models.IntegerField(
    null=True,
    blank=True,
    choices=ENDURANCE_CHOICES,
    verbose_name="我慢度",
    )
    memo = models.TextField(
    blank=True,
    verbose_name="メモ",
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

    @property
    def category_color(self):
        # カード左のドット用。未知カテゴリは灰
        return CATEGORY_COLORS.get(self.category, "#9ca3af")