import streamlit as st

# ページのタイトル
st.set_page_config(page_title="東京ダ1400.1600 期待度判定ツール", layout="centered")
st.title("東京ダ1400.1600 期待度判定ツール")

# 1. コース選択
course = st.radio("【コース選択】", ["東京ダート 1600m", "東京ダート 1400m"], horizontal=True)

st.markdown("---")

# 2. 条件入力
col1, col2, col3 = st.columns(3)

with col1:
    gate = st.selectbox("枠順", [f"{i}番" for i in range(1, 17)])
    gate_num = int(gate.replace("番", ""))
    style = st.selectbox("脚質", ["逃げ", "先行", "差し", "追い込み"])
    track_condition = st.selectbox("馬場状態", ["良馬場", "稍重", "重馬場", "不良馬場"])

with col2:
    jockey = st.selectbox("騎手", [
        "ルメール", "レーン", "モレイラ", "戸崎圭太", "川田将雅", "横山武史", 
        "武豊", "C.デムーロ", "菅原明良", "坂井瑠星", "佐々木大輔", 
        "田辺裕信", "三浦皇成", "内田博幸", "津村明秀", "岩田望来", 
        "西村淳也", "鮫島克駿", "松山弘平", "キング", "その他"
    ])
    
    # 系統と特注種牡馬に分離
    lineage = st.selectbox("血統系統", [
        "ミスプロ系", "キングマンボ系", "サンデー系", "ロベルト系", "その他"
    ])
    sire = st.selectbox("特注種牡馬", ["なし", "シニスターミニスター", "ヘニーヒューズ"])
    weight = st.selectbox("馬体重", ["490kg未満", "490kg以上"])

with col3:
    prev_rank = st.selectbox("前走着順", ["1着", "2着", "3着", "4〜5着", "6〜9着", "10着以下"])
    distance_change = st.selectbox("距離短縮", ["あり", "なし"])
    prev_track = st.selectbox("前走競馬場", ["中央4場", "ローカル/他"])

prev_condition = st.selectbox("前走種類", ["通常ダート", "芝からの転戦", "クラス降級"])
prev_disadvantage = st.selectbox("前走の敗因/内容", ["特なし/実力負け", "勝ち", "出遅れ/詰まり", "ハイペース失速"])

st.markdown("---")

# 3. 判定ロジック
score = 0
plus_reasons = []
minus_reasons = []

# 脚質・馬場
if style in ["逃げ", "先行"]:
    score += 20
    plus_reasons.append("前有利な脚質（+20）")

if track_condition in ["重馬場", "不良馬場"] and style in ["逃げ", "先行"]:
    score += 15
    plus_reasons.append("高速馬場への適性（+15）")

# 血統と特注種牡馬
lineage_scores = {"ミスプロ系": 25, "キングマンボ系": 25, "サンデー系": 15, "ロベルト系": 15, "その他": 5}
score += lineage_scores.get(lineage, 5)
plus_reasons.append(f"血統：{lineage}（+{lineage_scores.get(lineage, 5)}）")

if sire == "シニスターミニスター": score += 20; plus_reasons.append("特注：シニミニ（+20）")
if sire == "ヘニーヒューズ": score += 20; plus_reasons.append("特注：ヘニーヒューズ（+20）")

# 騎手・前走等
jockey_scores = {"ルメール":30, "レーン":30, "モレイラ":30, "戸崎圭太":25, "川田将雅":20, "横山武史":20, "武豊":20, "C.デムーロ":20}
score += jockey_scores.get(jockey, 10)
plus_reasons.append(f"騎手評価（+{jockey_scores.get(jockey, 10)}）")

if prev_rank in ["1着", "2着", "3着"]: score += 15; plus_reasons.append("前走好走（+15）")
if distance_change == "あり" and style in ["逃げ", "先行"]: score += 20; plus_reasons.append("距離短縮の利（+20）")
if prev_condition == "芝からの転戦": score += 20; plus_reasons.append("芝からの転戦（+20）")
if prev_condition == "クラス降級": score += 25; plus_reasons.append("クラス降級（+25）")
if prev_disadvantage == "出遅れ/詰まり": score += 15; plus_reasons.append("敗因明確（+15）")

# コース
if "1600m" in course and gate_num >= 13: score += 25; plus_reasons.append("1600m外枠（+25）")
elif "1400m" in course and gate_num <= 8 and style in ["逃げ", "先行"]: score += 20; plus_reasons.append("1400m内枠先行（+20）")

# 4. 判定結果
st.subheader("判定結果")
with st.container(border=True):
    if score >= 100: st.markdown("## **Sランク**")
    elif score >= 65: st.markdown("## **Aランク**")
    elif score >= 35: st.markdown("## **Bランク**")
    else: st.markdown("## **Cランク**")
    st.write(f"合計得点: {score}")
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1: st.markdown("**[+]**"); [st.write(f"・{r}") for r in plus_reasons]
    with c2: st.markdown("**[-]**"); [st.write(f"・{r}") for r in minus_reasons]