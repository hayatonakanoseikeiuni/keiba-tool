import streamlit as st

st.set_page_config(page_title="東京ダート 期待度判定ツール", layout="centered")
st.title("東京ダート 期待度判定ツール")
st.write("2026年最新バイアス対応版：判定ロジック強化")

course = st.radio("【コース選択】", ["東京ダート 1600m", "東京ダート 1400m"], horizontal=True)

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    gate = st.selectbox("枠順", [f"{i}番" for i in range(1, 17)])
    gate_num = int(gate.replace("番", ""))
    style = st.selectbox("脚質", ["逃げ", "先行", "差し", "追い込み"])
    track_condition = st.selectbox("馬場状態", ["良馬場", "稍重", "重馬場", "不良馬場"])

with col2:
    jockey_list = [
        "ルメール", "レーン", "モレイラ", "戸崎圭太", "川田将雅", "横山武史", "武豊", "C.デムーロ",
        "原優介", "菅原明良", "坂井瑠星", "佐々木大輔", "田辺裕信", "三浦皇成", "内田博幸",
        "松山弘平", "岩田望来", "西村淳也", "鮫島克駿", "キング", "津村明秀", "丹内祐次",
        "松岡正海", "吉田豊", "石川裕紀人", "大野拓弥", "木幡育也", "木幡初也", "木幡巧也", 
        "永野猛蔵", "小林勝太", "横山和生", "横山典弘", "高杉吏麒", "団野大成", "石橋脩", 
        "江田照男", "その他"
    ]
    jockey = st.selectbox("騎手", jockey_list)
    lineage = st.selectbox("血統系統", ["ミスプロ系(王道)", "キングマンボ系(パワー)", "サンデー系(瞬発)", "米国型(スピード持続)", "その他"])
    sire = st.selectbox("特注種牡馬", ["なし", "シニスターミニスター", "ヘニーヒューズ", "ドレフォン", "マインドユアビスケッツ"])

with col3:
    weight = st.selectbox("馬体重", ["490kg未満", "490kg以上"])
    prev_rank = st.selectbox("前走着順", ["1着", "2着", "3着", "4〜5着", "6〜9着", "10着以下"])
    prev_last_3f_fastest = st.radio("前走上がり最速", ["なし", "あり"], horizontal=True)

prev_condition = st.selectbox("前走種類", ["通常ダート", "芝からの転戦", "クラス降級"])
prev_disadvantage = st.selectbox("前走の敗因/内容", ["特なし/実力負け", "勝ち", "出遅れ/詰まり", "ハイペース失速"])

st.markdown("---")

# 判定ボタンを設置
if st.button("🚀 判定開始"):
    # ここから判定処理（ボタンを押したときだけ実行）
    score = 0
    plus_reasons = []
    minus_reasons = []

    # コース別ロジック
    if "1600m" in course:
        if gate_num >= 13: score += 25; plus_reasons.append("1600m外枠バイアス（+25）")
        elif gate_num <= 4: score -= 15; minus_reasons.append("1600m内枠砂被り（-15）")
    else: # 1400m
        if 4 <= gate_num <= 9: score += 20; plus_reasons.append("1400m中枠安定配置（+20）")
        if style in ["逃げ", "先行"]: score += 15; plus_reasons.append("1400m先行有利（+15）")

    # 騎手評価
    jockey_scores = {
        "ルメール": 30, "戸崎圭太": 28, "レーン": 25, "モレイラ": 25, 
        "佐々木大輔": 22, "田辺裕信": 20, "横山武史": 20, "原優介": 18, 
        "川田将雅": 18, "横山和生": 18, "三浦皇成": 15, "坂井瑠星": 15, 
        "菅原明良": 15, "C.デムーロ": 15, "武豊": 15, "内田博幸": 12,
        "松山弘平": 12, "岩田望来": 12, "鮫島克駿": 12, "木幡巧也": 12,
        "キング": 10, "津村明秀": 10, "丹内祐次": 10, "松岡正海": 10, 
        "吉田豊": 10, "石川裕紀人": 10, "大野拓弥": 10, "木幡育也": 10, 
        "木幡初也": 10, "永野猛蔵": 8, "小林勝太": 8, "横山典弘": 8, 
        "高杉吏麒": 8, "団野大成": 8, "石橋脩": 8, "江田照男": 8
    }
    j_score = jockey_scores.get(jockey, 10)
    score += j_score
    plus_reasons.append(f"騎手：{jockey}（+{j_score}）")

    # 血統
    if sire in ["シニスターミニスター", "ヘニーヒューズ"]: score += 20
    elif sire in ["ドレフォン", "マインドユアビスケッツ"]: score += 15

    # 前走
    if prev_last_3f_fastest == "あり": score += (20 if track_condition in ["重馬場", "不良馬場"] else 5)
    if prev_rank in ["1着", "2着", "3着"]: score += 15
    if prev_condition == "クラス降級": score += 25

    # 結果表示
    st.subheader("判定結果")
    with st.container(border=True):
        if score >= 90: level = "Sランク"
        elif score >= 60: level = "Aランク"
        elif score >= 35: level = "Bランク"
        else: level = "Cランク"
        
        st.markdown(f"## **{level}** （合計: {score}点）")
        st.markdown("---")
        
        # Reason表示部分の修正（リストが空の場合のケア）
        c1, c2 = st.columns(2)
        with c1: 
            st.markdown("**[+]**")
            for r in plus_reasons: st.write(f"・{r}")
        with c2: 
            st.markdown("**[-]**")
            if minus_reasons:
                for r in minus_reasons: st.write(f"・{r}")
            else:
                st.write("・特になし")
else:
    st.info("条件を選択して「判定開始」ボタンを押してください。")