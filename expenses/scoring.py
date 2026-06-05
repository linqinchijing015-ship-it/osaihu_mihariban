# scoring.py — 後悔スコア・我慢スコアの計算ロジック

# カテゴリごとの基礎スコア
# 無駄遣いになりやすいものほど高い値を設定
import math


CATEGORY_BASE_SCORE = {
    "food":    10,   # 食費・日用品（生活必需品）
    "apparel": 20,   # 衣服・書籍
    "gadget":  30,   # ガジェット・趣味
    "luxury":  40,   # 嗜好品・課金・コンビニ
}


def calc_regret_score(amount: int, satisfaction: int, category: str) -> float:
    """
    後悔スコアを計算して返す（0〜100）

    計算式:
        後悔スコア = カテゴリ基礎スコア × 満足度係数 + 金額係数 × 60

    引数:
        amount      : 金額（円）
        satisfaction: 満足度（1〜5）
        category    : カテゴリコード（"food" など）

    戻り値:
        float: 後悔スコア（0〜100）
    """
    # 満足度が低いほど係数が大きくなる
    # 満足度1 → 1.0（全然満足してない）
    # 満足度5 → 0.2（すごく満足）
    satisfaction_factor = (6 - satisfaction) / 5

    # 金額係数（10000円で最大1.0）
    amount_factor = min(math.log10(amount + 1) / 4, 1.0)

    # カテゴリ基礎スコア（未知カテゴリはデフォルト20）
    base = CATEGORY_BASE_SCORE.get(category, 20)

    score = base * satisfaction_factor + amount_factor * 60
    return round(min(max(score, 0), 100), 1)


def calc_endurance_score(amount: int, endurance: int, category: str) -> float:
    """
    我慢スコアを計算して返す（0〜100）

    計算式:
        我慢スコア = カテゴリ基礎スコア × 我慢度係数 + 金額係数 × 60

    引数:
        amount   : 我慢した金額（円）
        endurance: 我慢度（1〜5）
        category : カテゴリコード

    戻り値:
        float: 我慢スコア（0〜100）
    """
    # 我慢度が高いほど係数が大きくなる
    # 我慢度1 → 0.2（ちょっとしか我慢できなかった）
    # 我慢度5 → 1.0（完全に我慢できた）
    endurance_factor = endurance / 5

    amount_factor = min(math.log10(amount + 1) / 4, 1.0)
    base = CATEGORY_BASE_SCORE.get(category, 20)

    score = base * endurance_factor + amount_factor * 60
    return round(min(max(score, 0), 100), 1)