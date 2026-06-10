import streamlit as st

st.set_page_config(page_title="東京ダート 期待度判定ツール", layout="centered")
st.title("東京ダート 期待度判定ツール")
st.write("2026年最新バイアス対応版：上がり最速データ反映")

course = st.radio("【コース選択】", ["東京ダート 1600m", "東京ダート 1400m"], horizontal=True)

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    gate = st.selectbox("枠順", [f"{i}番" for i in range(1, 17)])
    gate_num = int(gate.replace("番", ""))
    style = st.selectbox("脚質", ["逃げ", "先行", "差し", "追い込み"])
    track_condition = st.selectbox("馬場状態", ["良馬場", "稍重", "重馬場", "不良馬場"])

with col2:
    jockey = st.selectbox("騎手", [
        "ルメール", "戸崎圭太", "原優介", "レーン", "モレイラ", "川田将雅", 
        "横山武史", "武豊", "C.デムーロ", "菅原明良", "坂井瑠星", "その他"
    ])
    lineage = st.selectbox("血統系統", ["ミスプロ系(王道)", "キングマンボ系(パワー)", "サンデー系(瞬発)", "米国型(スピード持続)", "その他"])
    sire = st.selectbox("特注種牡馬", ["なし", "シニスターミニスター", "ヘニーヒューズ", "ドレフォン", "マインドユアビスケッツ"])

with col3:
    weight = st.selectbox("馬体重", ["490kg未満", "490kg以上"])
    prev_rank = st.selectbox("前走着順", ["1着", "2着", "3着", "4〜5着", "6〜9着", "10着以下"])
    # 🌟 追加：前走上がり最速かどうか
    prev_last_3f_fastest = st.radio("前走上がり最速", ["なし", "あり"], horizontal=True)

prev_condition = st.selectbox("前走種類", ["通常ダート", "芝からの転戦", "クラス降級"])
prev_disadvantage = st.selectbox("前走の敗因/内容", ["特なし/実力負け", "勝ち", "出遅れ/詰まり", "ハイペース失速"])

st.markdown("---")

score = 0
plus_reasons = []
minus_reasons = []

# --- 判定ロジック ---
# 1. 枠順・コース
if "1600m" in course:
    if gate_num >= 13: score += 25; plus_reasons.append("1600m外枠有利（+25）")
    elif gate_num <= 4: score -= 15; minus_reasons.append("1600m内枠の砂被りリスク（-15）")
else:
    if 4 <= gate_num <= 9: score += 20; plus_reasons.append("1400m中枠の安定配置（+20）")
    elif gate_num <= 2: score -= 10; minus_reasons.append("1400m内枠の砂被りリスク（-10）")

# 2. 脚質
if style in ["逃げ", "先行"]: score += 20; plus_reasons.append("前残り優位（+20）")

# 3. 2026年トレンド血統
if sire in ["シニスターミニスター", "ヘニーヒューズ"]: score += 20; plus_reasons.append(f"鉄板種牡馬{sire}（+20）")
elif sire in ["ドレフォン", "マインドユアビスケッツ"]: score += 15; plus_reasons.append(f"トレンド米国型{sire}（+15）")

# 4. 前走上がり最速ロジック
if prev_last_3f_fastest == "あり":
    if track_condition in ["重馬場", "不良馬場"]:
        score += 20; plus_reasons.append("重・不良の高速馬場で上がり最速は脅威（+20）")
    else:
        score += 5; plus_reasons.append("前走上がり最速（良馬場は過剰人気に注意）")

# 5. 騎手・その他
jockey_scores = {"ルメール":30, "戸崎圭太":25, "原優介":20, "レーン":30, "モレイラ":30}
score += jockey_scores.get(jockey, 10)
if prev_rank in ["1着", "2着", "3着"]: score += 15
if prev_condition == "クラス降級": score += 25

# 判定結果
st.subheader("📊 判定結果")
with st.container(border=True):
    if score >= 90: st.markdown("## **Sランク**")
    elif score >= 60: st.markdown("## **Aランク**")
    elif score >= 35: st.markdown("## **Bランク**")
    else: st.markdown("## **Cランク**")
    st.write(f"合計得点: {score}")
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1: st.markdown("**[+]**"); [st.write(f"・{r}") for r in plus_reasons]
    with c2: st.markdown("**[-]**"); [st.write(f"・{r}") for r in minus_reasons]