import streamlit as st

# ページのタイトル
st.set_page_config(page_title="東京ダート 期待度判定ツール", layout="centered")
st.title("東京ダート 期待度判定ツール")
st.write("JRA東京開催特化のジョッキーデータ ＋ 前走の敗因から穴馬を炙り出します。")

# 1. コース選択（1600m / 1400m）
course = st.radio("【コース選択】", ["東京ダート 1600m", "東京ダート 1400m"], horizontal=True)

st.markdown("---")

# 2. 基本情報の入力
col1, col2 = st.columns(2)

with col1:
    gate = st.selectbox("枠順 (馬番)", [f"{i}番" for i in range(1, 17)])
    gate_num = int(gate.replace("番", ""))
    
    style = st.selectbox("脚質 (想定)", ["逃げ", "先行", "差し", "追い込み"])

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

st.markdown("---")

# 3. 穴馬爆発条件の入力
st.subheader("穴馬激走ボーナス（該当する場合のみ選択）")

col3, col4, col5 = st.columns(3)

with col3:
    is_large_heavy = st.selectbox("馬体重（馬格）", ["490kg未満", "490kg以上の大型馬"])
    distance_change = st.selectbox("前走からの距離", ["同距離/延長", "距離短縮 (例:1800→1600)"])

with col4:
    prev_track = st.selectbox("前走の競馬場", ["中央4場 (東京/中山/京都/阪神)", "ローカル/中京/新潟など"])
    prev_condition = st.selectbox("前走のレース種類", ["通常のダート戦", "前走は【芝】を走っていた", "今回【クラス下がり(降級)】"])

with col5:
    prev_disadvantage = st.selectbox("前走の敗因・内容", ["特なし/実力負け", "前走【出遅れ】や【直線前詰まり】", "前走【ハイペースに巻き込まれ】失速"])

st.markdown("---")

# 4. 判定ロジック（点数計算）
score = 0
plus_reasons = []
minus_reasons = []

# --- 基本得点（共通） ---
if style in ["逃げ", "先行"]:
    score += 20
    plus_reasons.append("ダートの定石である前有利（+20）")

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
        plus_reasons.append("1600mの芝を長く走れる有利な外枠（+25）")
        if is_large_heavy == "490kg以上の大型馬":
            score += 15
            plus_reasons.append("【穴パターン】外枠 × パワー型の大型馬（+15）")
    elif gate_num <= 4:
        score -= 10
        minus_reasons.append("1600mの砂を被りやすい不利な内枠（-10）")
else:
    if gate_num <= 8 and style in ["逃げ", "先行"]:
        score += 20
        plus_reasons.append("1400mの内〜中枠で先手を奪える好配置（+20）")
    elif gate_num >= 13 and style in ["差し", "追い込み"]:
        score += 15
        plus_reasons.append("1400mの外枠から砂を被らずスムーズに差せる（+15）")

# --- 単体穴馬ボーナス加算 ---
if distance_change == "距離短縮 (例:1800→1600)" and style in ["逃げ", "先行"]:
    score += 20
    plus_reasons.append("【穴パターン】距離短縮の逃げ・先行粘り込み（+20）")

if prev_track == "ローカル/中京/新潟など":
    score += 15
    plus_reasons.append("【穴パターン】ローカルからタフな東京へのコース替わり（+15）")

# --- 前走巻き返しロジックの加算 ---
if prev_condition == "前走は【芝】を走っていた":
    score += 20
    plus_reasons.append("【穴パターン】前走芝大敗からのダート替わり一変（+20）")
elif prev_condition == "今回【クラス下がり(降級)】":
    score += 25
    plus_reasons.append("【能力上位】相手関係が楽になるクラスダウン（+25）")

if prev_disadvantage == "前走【出遅れ】や【直線前詰まり】":
    score += 15
    plus_reasons.append("【敗因明確】前走不完全燃焼、スムーズなら巻き返し（+15）")
elif prev_disadvantage == "前走【ハイペースに巻き込まれ】失速" and style in ["逃げ", "先行"]:
    score += 15
    plus_reasons.append("【展開不向き】前走ハイペース度外視、マイペースなら（+15）")


# 5. 判定結果の表示
st.subheader("📊 判定結果")

with st.container(border=True):
    if score >= 75:
        st.markdown(f"## **Sランク** （合計: `{score}` 点）")
        st.markdown("<span style='color:#ff4b4b; font-weight:bold;'>【評価】本命・軸馬として信頼度最高値。勝負レース候補。</span>", unsafe_allow_html=True)
    elif score >= 50:
        st.markdown(f"## **Aランク** （合計: `{score}` 点）")
        st.markdown("<span style='color:#ffaa00; font-weight:bold;'>【評価】対抗〜紐には必須。穴パターン合致なら妙味あり。</span>", unsafe_allow_html=True)
    elif score >= 25:
        st.markdown(f"## **Bランク** （合計: `{score}` 点）")
        st.markdown("<span style='color:#00a0ff; font-weight:bold;'>【評価】押さえまで。展開の助けがあれば浮上可能。</span>", unsafe_allow_html=True)
    else:
        st.markdown(f"## **Cランク** （合計: `{score}` 点）")
        st.markdown("<span style='color:#777777; font-weight:bold;'>【評価】静観妥当。人気を考慮し、見送りを推奨。</span>", unsafe_allow_html=True)

    st.markdown("---")
    
    col_p, col_m = st.columns(2)
    
    with col_p:
        st.markdown("**[+] プラス材料**")
        if plus_reasons:
            for r in plus_reasons:
                st.write(f"・{r}")
        else:
            st.write("なし")
            
    with col_m:
        st.markdown("**[-] マイナス材料**")
        if minus_reasons:
            for r in minus_reasons:
                st.write(f"・{r}")
        else:
            st.write("なし")