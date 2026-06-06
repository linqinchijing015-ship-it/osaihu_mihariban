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


# ===== 後悔スコアの意味づけ（全否定を避けるための3段階分類） =====
# 「お財布見張り番」が見張るのは後悔する買い物であって、満足した買い物ではない。
# 満足度が高く安い買い物は「納得」として肯定し、衝動買いだけ「後悔ぎみ」として赤くする。
# しきい値は対数式の実データ分布に合わせる。現行式は低額でも金額係数が高めに出るため、
# 満足度の高い買い物（満足度4〜5）を「納得」に拾えるよう、しきい値は高めに取る。
# 例: 満足×安い〜中 ≈ 48〜57 → 納得 / 中間 ≈ 62〜73 → ふつう / 衝動買い ≈ 90+ → 後悔ぎみ。
REGRET_OK_MAX = 60      # これ以下＝納得のいく買い物（肯定）
REGRET_WARN_MAX = 78    # これ以下＝ふつう（中立）。超えると後悔ぎみ（注意）


def regret_level(score):
    """後悔スコアを 3 段階に分類して表示用の情報を返す。

    引数:
        score: 後悔スコア（None なら未採点）

    戻り値:
        dict | None:
            {"key": "ok"|"normal"|"regret", "icon": 絵文字, "label": 表示名}。
            未採点（score is None）のときは None を返す。
    """
    if score is None:
        return None
    if score <= REGRET_OK_MAX:
        return {"key": "ok", "icon": "🙂", "label": "納得"}
    if score <= REGRET_WARN_MAX:
        return {"key": "normal", "icon": "😐", "label": "ふつう"}
    return {"key": "regret", "icon": "😣", "label": "後悔ぎみ"}


# ===== 節約力スコア（後悔スコアと我慢スコアの合算指標） =====
def calc_net_score(regret_total: float, control_total: float) -> float:
    """節約力スコア = 我慢スコア総計 − 後悔スコア総計。

    我慢で稼いだ分から後悔した分を引いた「謙虚に暮らせているか」の指標。
    プラスなら我慢が後悔を上回る＝節約できている。マイナスなら後悔が勝っている。

    引数:
        regret_total : 後悔スコアの合計（買った物・採点済みのみ）
        control_total: 我慢スコアの合計（我慢した物・採点済みのみ）

    戻り値:
        float: 節約力スコア（小数1桁）。負にもなりうる。
    """
    return round((control_total or 0) - (regret_total or 0), 1)


# ===== ごほうびバッジ（B案：ごほうびゲーム） =====
# 我慢の積み上げと節約力スコアを「実績」として段階的に解放する。
# デモで必ず1つは光るよう、初級の条件はごく緩く設定している。
# 各バッジは (絵文字, ラベル, 達成判定関数) のタプル。
# 判定には集計値 stats(dict) を渡す:
#   stats = {"count": 我慢の総回数, "saved": 我慢で浮いた総額, "net": 節約力スコア}
# 2系統:
#  STOCK = 一度達成したら残る積み上げ型（記録）
#  STATE = 今の状態を映す状態型（条件を外れると消える＝維持する動機になる）
# 表示は「達成しているものだけ」を出す方針（未達はそもそも表示しない）。
# 判定に使う集計 stats(dict):
#   count  : 我慢の総回数 / saved: 我慢で浮いた総額(円) / net: 節約力スコア
#   buy    : 買った物の総件数(採点済み) / ok: 「納得」件数 / regret: 「後悔ぎみ」件数
STOCK_BADGES = [
    ("🌱", "はじめの一歩", lambda s: s["count"] >= 1),
    ("🔥", "我慢5回",      lambda s: s["count"] >= 5),
    ("💪", "我慢10回",     lambda s: s["count"] >= 10),
    ("👑", "5万円ガマン",   lambda s: s["saved"] >= 50000),
]
STATE_BADGES = [
    ("✨", "後悔ゼロ",       lambda s: s["buy"] >= 3 and s["regret"] == 0),
    ("🎯", "納得率8割",      lambda s: s["buy"] >= 3 and s["ok"] >= s["buy"] * 0.8),
    ("⚖️", "収支プラス",     lambda s: s["net"] >= 0),
    ("🛡️", "我慢が勝ってる", lambda s: s["count"] > s["buy"] and s["count"] >= 1),
    ("🏆", "節約マスター",   lambda s: s["net"] >= 200),
]


def reward_badges(count: int, saved: int, net: float,
                  buy: int = 0, ok: int = 0, regret: int = 0):
    """達成しているバッジだけを返す（未達は含めない）。

    STOCK（積み上げ）と STATE（状態）を順に判定し、達成しているものだけを返す。
    STATE は条件を外れると消えるので、常に「今点いているもの」が並ぶ。

    戻り値:
        list[dict]: 各 {"icon", "label", "kind"("stock"|"state")}。
    """
    stats = {
        "count": count or 0, "saved": saved or 0, "net": net or 0,
        "buy": buy or 0, "ok": ok or 0, "regret": regret or 0,
    }
    out = []
    for kind, table in (("stock", STOCK_BADGES), ("state", STATE_BADGES)):
        for icon, label, cond in table:
            if cond(stats):
                out.append({"icon": icon, "label": label, "kind": kind})
    return out
