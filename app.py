import streamlit as st

# ページのタイトル
st.set_page_config(page_title="東京ダート 期待度判定ツール", layout="centered")
st.title("東京ダート 期待度判定ツール")
st.write("コース特性・馬場・血統・騎手・前走条件から期待度を総合判定します。")

# 1. コース選択
course = st.radio("【コース選択】", ["東京ダート 1600m", "東京ダート 1400m"], horizontal=True)

st.markdown("---")

# 2. 条件入力（すべての項目を均等に配置）
col1, col2, col3 = st.columns(3)

with col1:
    gate = st.selectbox("枠順 (馬番)", [f"{i}番" for i in range(1, 17)])
    gate_num = int(gate.replace("番", ""))
    style = st.selectbox("脚質 (想定)", ["逃げ", "先行", "差し", "追い込み"])
    track_condition = st.selectbox("馬場状態", ["良馬場", "稍重", "重馬場", "不良馬場"])

with col2:
    jockey_list = [
        "ルメール", "レーン (短期免許の鬼)", "モレイラ (マジックマン)",
        "戸崎圭太", "川田将雅", "横山武史", "武豊", "C.デムーロ",
        "菅原明良", "坂井瑠星", "佐々木大輔", "田辺裕信", "三浦皇成",
        "内田博幸", "津村明秀", "岩田望来", "西村淳也", "鮫島克駿",
        "松山弘平", "キング", "丹内祐次", "木幡巧也", "大野拓弥",
        "その他（上記以外）"
    ]
    jockey = st.selectbox("ジョッキー", jockey_list)
    
    bloodline = st.selectbox(
        "血統 (種牡馬)", 
        [
            "シニスターミニスター (ダート最強格)", 
            "ヘニーヒューズ (抜群の安定感)", 
            "ドレフォン", "ロードカナロア", "ホッコータルマエ",
            "キタサンブラック (大型一発あり)", "その他"
        ]
    )
    is_large_heavy = st.selectbox("馬体重（馬格）", ["490kg未満", "490kg以上の大型馬"])

with col3:
    distance_change = st.selectbox("前走からの距離", ["同距離/延長", "距離短縮 (例:1800→1600)"])
    prev_track = st.selectbox("前走の競馬場", ["中央4場 (東京/中山/京都/阪神)", "ローカル/中京/新潟など"])
    prev_condition = st.selectbox("前走のレース種類", ["通常のダート戦", "前走は【芝】を走っていた", "今回【クラス下がり(降級)】"])

# 3列の下に残りの1つの項目を配置
prev_disadvantage = st.selectbox("前走の敗因・内容", ["特なし/実力負け", "前走【出遅れ】や【直線前詰まり】", "前走【ハイペースに巻き込まれ】失速"])

st.markdown("---")

# 3. 判定ロジック（点数計算）
score = 0
plus_reasons = []
minus_reasons = []

# --- 基本得点：脚質 ---
if style in ["逃げ", "先行"]:
    score += 20
    plus_reasons.append("ダートの定石である前有利（+20）")

# --- 馬場状態のロジック ---
if track_condition in ["重馬場", "不良馬場"]:
    if style in ["逃げ", "先行"]:
        score += 15
        plus_reasons.append(f"{track_condition}の高速馬場 × 前に行ける脚質（+15）")
    elif style == "追い込み":
        score -= 10
        minus_reasons.append(f"{track_condition}の高速馬場は前が止まらず、追い込み不利（-10）")
elif track_condition == "良馬場":
    if is_large_heavy == "490kg以上の大型馬":
        score += 10
        plus_reasons.append("タフな良馬場で活きるパワー型の大型馬（+10）")

# --- 血統の配点 ---
if bloodline in ["シニスターミニスター (ダート最強格)", "ヘニーヒューズ (抜群の安定感)"]:
    score += 20
    plus_reasons.append(f"血統：東京ダート鉄板種牡馬の{bloodline.split(' ')[0]}（+20）")
elif bloodline in ["ドレフォン", "ロードカナロア", "ホッコータルマエ", "キタサンブラック (大型一発あり)"]:
    score += 10
    plus_reasons.append(f"血統：東京ダート好相性の{bloodline.split(' ')[0]}（+10）")

# --- 騎手データ ---
jockey_scores = {
    "ルメール": 30, "レーン (短期免許の鬼)": 30, "モレイラ (マジックマン)": 30,
    "戸崎圭太": 25,
    "川田将雅": 20, "横山武史": 20, "武豊": 20, "C.デムーロ": 20,
    "菅原明良": 18, "坂井瑠星": 18, "佐々木大輔": 18,
    "田辺裕信": 15, "三浦皇成": 15, "内田博幸": 15,
    "津村明秀": 12, "岩田望来": 12, "西村淳也": 12,
    "鮫島克駿": 10, "松山弘平": 10, "キング": 10,
    "丹内祐次": 5, "木幡巧也": 5, "大野拓弥": 5,
    "その他（上記以外）": 0
}

jockey_score = jockey_scores.get(jockey, 0)
if jockey_score > 0:
    score += jockey_score
    plus_reasons.append(f"騎手：{jockey}（+{jockey_score}）")


# --- コース別専用ロジック ---
if "1600m" in course:
    if gate_num >= 13:
        score += 25
        plus_reasons.append("1600mの芝を長く走