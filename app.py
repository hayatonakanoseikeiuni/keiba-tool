import streamlit as st

st.set_page_config(page_title="東京ダ1400/1600 期待度判定ツール", layout="centered")
st.title("東京ダ1400/1600 期待度判定ツール")
st.write("2026年最新バイアス・データ統合版")

course = st.radio("コース選択", ["東京ダート 1600m", "東京ダート 1400m"], horizontal=True)

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
    sire = st.selectbox("特注種牡馬", [
        "なし", "シニスターミニスター", "ヘニーヒューズ", "ドレフォン", "マインドユアビスケッツ",
        "ゴールドドリーム", "シルバーステート", "ジャスタウェイ", "ロードカナロア"
    ])

with col3:
    weight = st.selectbox("馬体重", ["490kg未満", "490kg以上"])
    prev_rank = st.selectbox("前走着順", ["1着", "2着", "3着", "4〜5着", "6〜9着", "10着以下"])
    prev_margin = st.selectbox("前走の着差", ["大敗", "0.6〜1.0秒差", "0.1〜0.5秒差", "勝ち"])
    is_distance_shortening = st.checkbox("前走からの距離短縮")
    fast_last_3f = st.checkbox("上がり3F上位経験あり")
    is_first_blinkers = st.checkbox("今回が初ブリンカー")

st.markdown("---")

if st.button("判定開始"):
    score = 0
    plus_reasons = []
    minus_reasons = []

    if "1600m" in course:
        if gate_num >= 13:
            score += 25
            plus_reasons.append("1600m外枠有利 (+25)")
        elif gate_num <= 4:
            score -= 5
            minus_reasons.append("1600m内枠の砂被りリスク (-5)")
    else:
        if 4 <= gate_num <= 9:
            score += 20
            plus_reasons.append("1400m中枠の安定配置 (+20)")
        if style in ["逃げ", "先行"]:
            score += 5
            plus_reasons.append("1400m先行バイアス (+5)")

    style_scores = {
        "東京ダート 1400m": {"逃げ": 20, "先行": 20, "差し": 5, "追い込み": -10},
        "東京ダート 1600m": {"逃げ": 10, "先行": 20, "差し": 15, "追い込み": 0}
    }
    s_score = style_scores[course].get(style, 0)
    score += s_score
    plus_reasons.append(f"脚質: {style}適性 ({s_score:+d})")

    jockey_scores = {"ルメール": 30, "戸崎圭太": 28, "レーン": 25, "モレイラ": 25, "佐々木大輔": 22, "田辺裕信": 20, "横山武史": 20, "原優介": 18, "川田将雅": 18, "横山和生": 18, "三浦皇成": 15, "坂井瑠星": 15, "菅原明良": 15, "C.デムーロ": 15, "武豊": 15, "内田博幸": 12, "松山弘平": 12, "岩田望来": 12, "鮫島克駿": 12, "木幡巧也": 12, "キング": 10, "津村明秀": 10, "丹内祐次": 10, "松岡正海": 10, "吉田豊": 10, "石川裕紀人": 10, "大野拓弥": 10, "木幡育也": 10, "木幡初也": 10, "永野猛蔵": 8, "小林勝太": 8, "横山典弘": 8, "高杉吏麒": 8, "団野大成": 8, "石橋脩": 8, "江田照男": 8}
    j_score = jockey_scores.get(jockey, 10)
    score += j_score
    plus_reasons.append(f"騎手: {jockey} (+{j_score})")
    
    if sire in ["シニスターミニスター", "ヘニーヒューズ"]:
        score += 20
        plus_reasons.append(f"鉄板種牡馬: {sire} (+20)")
    elif sire in ["ドレフォン", "マインドユアビスケッツ"]:
        score += 15
        plus_reasons.append(f"米国型: {sire} (+15)")
    elif sire in ["ゴールドドリーム", "シルバーステート", "ジャスタウェイ"]:
        score += 10
        plus_reasons.append(f"ダート適性サンデー系: {sire} (+10)")
    elif sire == "ロードカナロア":
        if "1400m" in course and style in ["逃げ", "先行"]:
            score += 15
            plus_reasons.append("ロードカナロア: 1400m先行力評価 (+15)")
        else:
            score += 5
            plus_reasons.append("ロードカナロア: スピード適性 (+5)")
    
    if weight == "490kg以上":
        score += 5
        plus_reasons.append("大型馬パワー評価 (+5)")
    
    if prev_rank == "1着":
        score += 20
        plus_reasons.append("前走1着 (+20)")
    elif prev_rank == "2着":
        score += 15
        plus_reasons.append("前走2着 (+15)")
    elif prev_rank == "3着":
        score += 10
        plus_reasons.append("前走3着 (+10)")
    
    if prev_margin == "0.1〜0.5秒差":
        score += 5
        plus_reasons.append("僅差負け (+5)")
    if is_distance_shortening:
        score += 15
        plus_reasons.append("距離短縮 (+15)")
    if fast_last_3f:
        score += 10
        plus_reasons.append("上がり3F上位経験あり (+10)")
    if is_first_blinkers:
        score += 10
        plus_reasons.append("初ブリンカー (+10)")

    st.subheader("判定結果")
    with st.container(border=True):
        if score >= 60:
            level = "Sランク (鉄板級)"
        elif score >= 40:
            level = "Aランク (勝負の一頭)"
        elif score >= 25:
            level = "Bランク (連下・抑え)"
        else:
            level = "Cランク (消し検討)"
        
        st.markdown(f"## {level} (合計: {score}点)")
        st.markdown("---")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**加点要素**")
            for r in plus_reasons:
                st.write(r)
        with c2:
            st.markdown("**減点要素**")
            if minus_reasons:
                for r in minus_reasons:
                    st.write(r)
            else:
                st.write("特になし")
else:
    st.info("条件を選択して判定開始ボタンを押してください。")