import streamlit as st

st.title("東京ダート 期待度判定ツール 【騎手データ完全解析版】")
st.write("過去の東京ダートデータに登場する全騎手をランク化し、自動で鞍上補正をおこないます。")

st.markdown("---")

# 【最上段：コース切り替えスイッチ】
course = st.radio("勝負するコースを選択してください", ["東京ダート1600m", "東京ダート1400m"])

st.markdown("---")

# 血統辞書データの定義
SUNDAY_SIRES = ["ディープインパクト", "ハーツクライ", "キズナ", "エピファネイア", "ゴールドアリュール", "オルフェーヴル", "デュラメンテ", "スワーヴリチャード", "コントレイル"]
MR_PROS_SIRES = ["キングカメハメハ", "ロードカナロア", "ルーラーシップ", "ドゥラメンテ", "ホッコータルマエ", "ルヴァンスレーヴ"]
STORMCAT_SIRES = ["ヘニーヒューズ", "ドレフォン", "アジアエクスプレス", "モーニン", "ディスクリートキャット"]
MINISTER_SIRES = ["シニスターミニスター"]

# ----------------------------------------
# 【研究データに基づく騎手ランクの完全定義】
# ----------------------------------------
# Sランク：文句なしの東京ダートの絶対王者
JOCKEYS_S = ["ルメール", "川田将雅", "レーン"]

# Aランク：データ上、上位争いの常連であり信頼度抜群
JOCKEYS_A = ["戸崎圭太", "横山武史", "横山和生", "田辺裕信", "松山弘平", "佐々木大輔", "キング"]

# Bランク：データ内で複数回勝利、または人気薄での一発・好走が目立つ実力派
JOCKEYS_B = ["三浦皇成", "菅原明良", "原優介", "荻野極", "横山典弘", "吉田豊", "菊沢一樹", "大野拓弥", "佐藤翔馬"]

# Cランク：データに登場する、侮れない中堅・若手の騎手陣
JOCKEYS_C = [
    "上里直汰", "石田拓郎", "木幡巧也", "木幡初也", "柴田善臣", "岩田望来", 
    "坂井瑠星", "石川裕紀", "遠藤汰月", "長浜鴻緒", "富嶽賞", "武豊", "丹内祐次",
    "高杉吏麒", "津村明秀", "江田照男", "石橋脩", "団野大成", "柴田大知", 
    "杉原誠人", "矢野貴之", "原田和真", "岩田康誠", "丸山元気", "丸田恭介"
]

# 全騎手リストの作成（セレクトボックス用）
all_jockeys = ["選択してください"] + JOCKEYS_S + JOCKEYS_A + JOCKEYS_B + JOCKEYS_C + ["その他（データにない騎手・追加点なし）"]


# ユーザー入力エリア（2列構成）
col1, col2 = st.columns(2)

with col1:
    horse_number = st.number_input("馬番を入力 (1〜16)", min_value=1, max_value=16, value=1)
    
    style = st.selectbox(
        "脚質を選択",
        ["選択してください", "逃げ", "先行", "差し（一般）", "前走上がり最速の差し", "追い込み"]
    )
    
    sire_name = st.text_input("父名（種牡馬名）を入力", value="").strip()
    
    # 自動判別のロジック
    detected_lineage = "未判定"
    if sire_name:
        if sire_name in MINISTER_SIRES:
            detected_lineage = "シニスターミニスター（特注）"
        elif sire_name in STORMCAT_SIRES:
            detected_lineage = "ストームキャット系"
        elif sire_name in MR_PROS_SIRES:
            detected_lineage = "ミスプロ系"
        elif sire_name in SUNDAY_SIRES:
            detected_lineage = "サンデー系"
        else:
            detected_lineage = "その他・不明"

    st.info(f"AI自動判別：【 {detected_lineage} 】")
    
    lineage = st.selectbox(
        "（自動判別が「その他・不明」の場合のみ選択してください）",
        ["自動判別に従う", "シニスターミニスター（特注）", "ストームキャット系", "ミスプロ系", "サンデー系", "その他"]
    )
    
    if lineage == "自動判別に従う":
        final_lineage = detected_lineage
    else:
        final_lineage = lineage

with col2:
    track_condition = st.selectbox(
        "当日の馬場状態を選択",
        ["選択してください", "良", "稍重", "重", "不良"]
    )
    
    last_race_result = st.selectbox(
        "前走の着順を選択",
        ["選択してください", "1着", "2着〜3着", "4着〜5着", "6着〜9着（大敗・穴目）", "10着以下"]
    )
    
    # 完全網羅された騎手セレクトボックス
    selected_jockey = st.selectbox("鞍上（ジョッキー）を選択", all_jockeys)

st.markdown("---")

# 判定ボタン
if st.button("期待度をマルチ判定する"):
    if style == "選択してください" or track_condition == "選択してください" or last_race_result == "選択してください" or selected_jockey == "選択してください" or not sire_name:
        st.warning("すべての項目を入力・選択してください。")
    elif final_lineage in ["未判定", "その他・不明"] and lineage == "自動判別に従う":
        st.warning("血統が判定できませんでした。手動で系統を選択してください。")
    else:
        score = 0
        reasons = []

        # 馬番から枠順（1〜8枠）を算出
        if horse_number in [1, 2]: frame = 1
        elif horse_number in [3, 4]: frame = 2
        elif horse_number in [5, 6]: frame = 3
        elif horse_number in [7, 8]: frame = 4
        elif horse_number in [9, 10]: frame = 5
        elif horse_number in [11, 12]: frame = 6
        elif horse_number in [13, 14]: frame = 7
        else: frame = 8

        # 1. コース分岐ロジック：東京ダート1600m
        if course == "東京ダート1600m":
            if frame in [7, 8]:
                score += 30
                reasons.append(f"【高評価】1600m特有の芝スタート外枠有利バイアスに合致 (+30点)")
            elif frame in [1, 2]:
                score -= 20
                reasons.append(f"【危険】1600mの内枠砂被りリスク大 (-20点)")
            else:
                reasons.append(f"【中立】{frame}枠：標準評価 (+0点)")

            if final_lineage == "シニスターミニスター（特注）":
                if track_condition in ["良", "稍重"]:
                    score += 45
                    reasons.append("【特注】シニスターミニスター × 1600m乾いた馬場：単勝回収率トップの黄金パターン (+45点)")
                else:
                    score += 10
                    reasons.append("【割引】シニスターミニスター × 道悪馬場：キレ負けリスクあり (+10点)")
            elif final_lineage == "ストームキャット系":
                if track_condition in ["良", "稍重"]:
                    score += 40
                    reasons.append("【高評価】ストームキャット系 × 1600m乾いた馬場：複勝率35%超えの軸信頼 (+40点)")
                else:
                    score += 15
                    reasons.append("【割引】ストームキャット系 × 道悪馬場：若干パフォーマンス低下 (+15点)")
            elif final_lineage == "ミスプロ系":
                score += 20
                reasons.append("【中立】ミスプロ系：平均的な安定勢力 (+20点)")
            elif final_lineage == "サンデー系":
                if track_condition in ["重", "不良"]:
                    score += 25
                    reasons.append("【道悪特注】サンデー系 × 道悪馬場：芝的なスピード決着で浮上 (+25点)")
                else:
                    score += 5
                    reasons.append("【中立】サンデー系：良馬場ではパワー不足傾向 (+5点)")

        # 2. コース分岐ロジック：東京ダート1400m
        else:
            if frame in [4, 5, 6]:
                score += 25
                reasons.append(f"【高評価】1400mのベストゾーン、ロスなく砂も被りにくい中枠 (+25点)")
            elif frame in [1, 2]:
                score -= 20
                reasons.append(f"【危険】1400mの内枠：包まれてキックバックを浴びるリスク高 (-20点)")
            else:
                reasons.append(f"【中立】{frame}枠：標準評価 (+0点)")

            if final_lineage == "ストームキャット系":
                score += 40
                reasons.append("【高評価】1400mのストームキャット系：短距離スピードの絶対値が高く道悪でも不発が少ない (+40点)")
            elif final_lineage == "ミスプロ系":
                if track_condition in ["重", "不良"]:
                    score += 35
                    reasons.append("【道悪特注】ミスプロ系 × 1400m道悪：軽いスピード馬場で本領発揮 (+35点)")
                else:
                    score += 25
                    reasons.append("【良評価】ミスプロ系：1600mより1400mの方がスピードが活きる (+25点)")
            elif final_lineage == "シニスターミニスター（特注）":
                score += 20
                reasons.append("【中立】シニスターミニスター：1400mでは爆発力減、相手（2〜3着）までの評価 (+20点)")
            else:
                score += 10
                reasons.append(f"【中立】{final_lineage}：標準的な期待値 (+10点)")

        # 3. 脚質のロジック
        if style in ["逃げ", "先行"]:
            if course == "東京ダート1400m":
                score += 35
                reasons.append(f"【高評価】1400mの脚質[{style}]：1600mよりさらに前残りバイアスが強力 (+35点)")
            else:
                score += 30
                reasons.append(f"【高評価】1600mの脚質[{style}]：ダートの本質である前残りバイアス (+30点)")
        elif style == "前走上がり最速の差し":
            score -= 15
            reasons.append("【危険】前走上がり最速の差し：東京の直線に騙されたファンによる過剰人気馬 (-15点)")
        else:
            reasons.append(f"【中立】脚質[{style}]：標準評価 (+0点)")

        # 4. 前走着順による期待値・妙味ロジック
        if last_race_result == "1着":
            score += 10
            reasons.append("【安定】前走1着：勢いそのままに信頼度高め (+10点)")
        elif last_race_result in ["2着〜3着", "4着〜5着"]:
            score += 15
            reasons.append(f"【妙味】前走[{last_race_result}]：大崩れせずオイシイゾーン (+15点)")
        elif last_race_result == "6着〜9着（大敗・穴目）":
            is_good_frame = (course == "東京ダート1600m" and frame in [6, 7, 8]) or (course == "東京ダート1400m" and frame in [4, 5, 6, 7, 8])
            if is_good_frame and style in ["逃げ", "先行"]:
                score += 25
                reasons.append("【爆穴注意】前走大敗からの条件好転：好枠＋先行による巻き返しの期待値特大 (+25点)")
            else:
                score -= 10
                reasons.append("【静観】前走中位：条件好転の要素が薄く見送り妥当 (-10点)")
        elif last_race_result == "10着以下":
            score -= 20
            reasons.append("【危険】前走2桁着順：能力発揮が難しい状態 (-20点)")

        # ----------------------------------------
        # 5. 【データ完全対応：新・鞍上補正ロジック】
        # ----------------------------------------
        if selected_jockey in JOCKEYS_S:
            score += 35
            reasons.append(f"【特注・Sランク】{selected_jockey}騎手：東京ダート最上位。勝負強さと腕前は文句なしトップ (+35点)")
        elif selected_jockey in JOCKEYS_A:
            score += 25
            reasons.append(f"【高評価・Aランク】{selected_jockey}騎手：東京ダート上位の常連。馬の能力をきっちり引き出す信頼の塊 (+25点)")
        elif selected_jockey in JOCKEYS_B:
            score += 15
            reasons.append(f"【好気配・Bランク】{selected_jockey}騎手：人気薄での激走や一発を秘める東京ダート実力派 (+15点)")
        elif selected_jockey in JOCKEYS_C:
            score += 5
            reasons.append(f"【堅実・Cランク】{selected_jockey}騎手：研究データに勝利・好走履歴あり。展開ひとつで上位食い込み可能 (+5点)")
        else:
            reasons.append("【中立】データ外の騎手：乗り替わりや遠征等、騎手による過度な加点はなし (+0点)")

        # 6. 最終結果の出力
        st.subheader(f"総合判定結果: {score} 点")
        
        if score >= 115: # 騎手ポイントの上限が上がったため基準を調整
            st.success("評価：★★★★ 【超・勝負レース】期待値限界突破。厚く張れる極上馬")
        elif score >= 85:
            st.success("評価：★★★ 【勝負レース推奨】軸馬として高い信頼度")
        elif score >= 55:
            st.info("評価：★★ 【相手候補】ヒモ・連軸として優秀な期待値")
        elif score >= 25:
            st.warning("評価：★ 【押さえ】オッズ次第で3連複の端っこに")
        else:
            st.error("評価：❌ 【消し】人気でもバッサリ切って妙味を追うべき馬")

        st.write("■ スコア内訳:")
        for r in reasons:
            st.write(r)