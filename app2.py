import streamlit as st

def JRA_Mile_Expectation_Engine(horse_name, base_data, current_race):
    """JRA競馬場芝1600期待値判別エンジン（ロジック部分はそのまま）"""
    score = 20  # 初期値

    jockey = base_data.get('jockey')
    jockey_points = {
        'C.ルメール': 20, 'J.モレイラ': 19, '川田将雅': 18, 
        '坂井瑠星': 16, '戸崎圭太': 16, '横山武史': 12, '丹内祐次': 3
    }
    score += jockey_points.get(jockey, 5)

    sire = base_data.get('sire')
    sire_group = base_data.get('sire_group')
    track_condition = current_race.get('track_condition', '良')
    
    if track_condition in ['重', '不良']:
        if sire_group in ['ディープ系', 'ロードカナロア系']: s_score = 5
        elif sire_group == 'ロベルト系' or sire == 'ハービンジャー': s_score = 15 + 12
        else: s_score = 8
    else:
        if sire_group == 'ディープ系': s_score = 15
        elif sire == 'ロードカナロア': s_score = 12
        elif sire_group == 'キングマンボ系': s_score = 13
        elif sire == 'エピファネイア': s_score = 19
        elif sire == 'キズナ': s_score = 18
        else: s_score = 10
    score += s_score

    prev_distance = base_data.get('prev_distance')
    venue = current_race.get('venue')
    dist_score = 0
    if prev_distance >= 2000:
        dist_score = 14 if venue in ['東京', '阪神'] else 5
    elif prev_distance == 1800: dist_score = 6
    elif prev_distance == 1400: dist_score = 4
    score += dist_score

    prev_venue = base_data.get('prev_venue')
    venue_score = 0
    if prev_venue in ['中山', '小倉', '福島', '函館', '札幌'] and venue in ['東京', '阪神']: venue_score = 11
    elif prev_venue in ['東京', '京都', '新潟'] and venue == '中山': venue_score = 3
    score += venue_score

    prev_rank = base_data.get('prev_rank')
    time_difference = base_data.get('time_diff')
    prev_class = base_data.get('prev_class')
    prev_performance = base_data.get('prev_performance', [])
    has_best_agari = '上がり最速' in prev_performance
    
    perf_score = 0
    is_disqualified = False
    if prev_rank <= 1: perf_score += 8 if not base_data.get('is_class_up') else 4
    elif 2 <= prev_rank <= 3: perf_score += 6
    elif 4 <= prev_rank <= 5 or time_difference <= 0.3: perf_score += 3
    else:
        if prev_class in ['G1', 'G2', 'G3']:
            if time_difference < 2.0: perf_score += 7
            else: is_disqualified = True
        else:
            if time_difference >= 2.0: is_disqualified = True
            elif time_difference <= 0.9 and has_best_agari: perf_score += 18
            elif time_difference <= 0.9: perf_score += 7
            elif has_best_agari: perf_score += 11

    if is_disqualified:
        score -= dist_score
        score -= venue_score
        perf_score = 0
    score += perf_score

    gate = current_race.get('gate_number')
    if venue == '中山' and gate in [1, 2, 3, 4]: score += 13
    elif venue == '東京' and gate in [9, 10, 11, 12, 13, 14]: score += 5
    
    return score

# ==========================================
# Streamlit 画面表示レイアウト
# ==========================================
st.title(" JRA競馬場芝1600期待値判別エンジン")
st.write("出走馬のデータを入力して、今週末の爆発マグマ馬を炙り出そう！")

# 1. レース環境設定
st.header("レース環境設定")
col1, col2 = st.columns(2)
with col1:
    venue = st.selectbox("開催競馬場", ["東京", "阪神", "中山", "京都", "新潟", "小倉", "福島", "中京", "函館", "札幌"])
with col2:
    track_condition = st.selectbox("馬場状態", ["良", "稍重", "重", "不良"])

current_race_info = {"venue": venue, "track_condition": track_condition}

# 2. 出走馬のデータ入力（動的追加）
st.header("🐎 出走馬データ入力")
if "horses" not in st.session_state:
    # 初期データとして2頭分用意
    st.session_state.horses = [
        {'name': 'ソニックライン', 'gate_number': 16, 'jockey': '川田将雅', 'sire': 'キングカメハメハ', 'sire_group': 'キングマンボ系', 'prev_distance': 1800, 'prev_venue': '中山', 'prev_class': 'G2', 'prev_rank': 11, 'time_diff': 1.6, 'agari_fastest': False, 'is_class_up': False},
        {'name': 'ゴディアーモ', 'gate_number': 12, 'jockey': '戸崎圭太', 'sire': 'エピファネイア', 'sire_group': 'ロベルト系', 'prev_distance': 1600, 'prev_venue': '東京', 'prev_class': '平場', 'prev_rank': 1, 'time_diff': 0.0, 'agari_fastest': False, 'is_class_up': True}
    ]

# 馬を追加するボタン
if st.button("➕ 馬を追加する"):
    st.session_state.horses.append({'name': f'馬_{len(st.session_state.horses)+1}', 'gate_number': 1, 'jockey': 'C.ルメール', 'sire': '', 'sire_group': 'サンデー系', 'prev_distance': 1600, 'prev_venue': '東京', 'prev_class': '平場', 'prev_rank': 1, 'time_diff': 0.0, 'agari_fastest': False, 'is_class_up': False})

# 各馬の入力フォームをループ表示
updated_horses = []
for i, h in enumerate(st.session_state.horses):
    with st.expander(f"🐴 {h['name']} のデータ設定", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            h['name'] = st.text_input(f"馬名", h['name'], key=f"name_{i}")
            h['gate_number'] = st.number_input(f"馬番", min_value=1, max_value=18, value=int(h['gate_number']), key=f"gate_{i}")
        with c2:
            h['jockey'] = st.text_input(f"騎手名", h['jockey'], key=f"jock_{i}")
            h['sire_group'] = st.selectbox(f"血統系統", ['サンデー系', 'ディープ系', 'キングマンボ系', 'ロベルト系', 'ロードカナロア系', 'その他'], index=['サンデー系', 'ディープ系', 'キングマンボ系', 'ロベルト系', 'ロードカナロア系', 'その他'].index(h['sire_group']), key=f"sireg_{i}")
        with c3:
            h['prev_distance'] = st.number_input(f"前走距離", value=int(h['prev_distance']), step=200, key=f"pdist_{i}")
            h['prev_venue'] = st.selectbox(f"前走競馬場", ["東京", "中山", "阪神", "京都", "新潟", "小倉", "福島", "函館", "札幌"], index=["東京", "中山", "阪神", "京都", "新潟", "小倉", "福島", "函館", "札幌"].index(h['prev_venue']), key=f"pvenue_{i}")
        with c4:
            h['prev_rank'] = st.number_input(f"前走着順", min_value=1, max_value=18, value=int(h['prev_rank']), key=f"prank_{i}")
            h['time_diff'] = st.number_input(f"前走タイム差", value=float(h['time_diff']), step=0.1, key=f"tdiff_{i}")
        
        # チェックボックス系
        cc1, cc2 = st.columns(2)
        with cc1:
            h['agari_fastest'] = st.checkbox("前走上がり最速", value=h['agari_fastest'], key=f"agari_{i}")
        with cc2:
            h['is_class_up'] = st.checkbox("今回昇級戦（前走1着）", value=h['is_class_up'], key=f"class_{i}")
            
        h['prev_class'] = '平場' # 簡易化のため固定（必要に応じて拡張可能）
        h['prev_performance'] = ['上がり最速'] if h['agari_fastest'] else []
        
        updated_horses.append(h)

st.session_state.horses = updated_horses

# 3. 判定ボタンとランキング表示
st.write("---")
if st.button("期待値ランキングを計算する", type="primary"):
    ranking_list = []
    for horse in st.session_state.horses:
        score = JRA_Mile_Expectation_Engine(horse['name'], horse, current_race_info)
        ranking_list.append({'name': horse['name'], 'score': score, 'jockey': horse['jockey']})
    
    ranking_list.sort(key=lambda x: x['score'], reverse=True)
    
    st.header(" 判定結果ランキング")
    for rank, h_info in enumerate(ranking_list, 1):
        st.subheader(f"Rank {rank}: {h_info['name']} ({h_info['jockey']}) ➔ **{h_info['score']} POINTS**")