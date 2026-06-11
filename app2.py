
import streamlit as st

def JRA_Mile_Expectation_Engine(base_data, current_race):
    """JRA芝1600期待値判別エンジン（新馬戦フラット評価・マスターデータ連動版）"""
    score = 20  # 初期値
    venue = current_race.get('venue')

    # ========================================================
    # 🌟 JRA全騎手 競馬場別マイル適性マスターデータ
    # ========================================================
    jockey_master_data = {
        'C.ルメール': {'東京': 20, '中山': 14, '阪神': 16, '京都': 15},
        '川田将雅':   {'東京': 15, '中山': 5,  '阪神': 20, '京都': 18},
        '戸崎圭太':   {'東京': 16, '中山': 15, '阪神': 6,  '京都': 5},
        '横山武史':   {'東京': 12, '中山': 18, '阪神': 7,  '京都': 6},
        '坂井瑠星':   {'東京': 11, '中山': 10, '阪神': 16, '京都': 12},
        '武豊':       {'東京': 9,  '中山': 6,  '阪神': 8,  '京都': 18},
        'D.レーン':   {'東京': 20, '中山': 15, '阪神': 13, '京都': 12},
        'J.モレイラ': {'東京': 16, '中山': 13, '阪神': 19, '京都': 16},
        '西村淳也':   {'東京': 9,  '中山': 8,  '阪神': 12, '京都': 15},
        '岩田望来':   {'東京': 8,  '中山': 7,  '阪神': 13, '京都': 12},
        '津村明秀':   {'東京': 12, '中山': 12, '阪神': 4,  '京都': 3},
        '菅原明良':   {'東京': 11, '中山': 7,  '阪神': 3,  '京都': 3},
        '松山弘平':   {'東京': 8,  '中山': 9,  '阪神': 11, '京都': 11},
        '鮫島克駿':   {'東京': 7,  '中山': 6,  '阪神': 11, '京都': 10},
        '団野大成':   {'東京': 8,  '中山': 6,  '阪神': 10, '京都': 11},
        '三浦皇成':   {'東京': 8,  '中山': 10, '阪神': 4,  '京都': 3},
        '岩田康誠':   {'東京': 6,  '中山': 8,  '阪神': 9,  '京都': 11},
        'M.デムーロ': {'東京': 10, '中山': 11, '阪神': 8,  '京都': 7},
        '丹内祐次':   {'東京': 3,  '中山': 9,  '阪神': 2,  '京都': 2},
        '佐々木大輔': {'東京': 5,  '中山': 8,  '阪神': 3,  '京都': 3},
        '横山和生':   {'東京': 8,  '中山': 7,  '阪神': 6,  '京都': 5},
        '北村友一':   {'東京': 5,  '中山': 4,  '阪神': 9,  '京都': 9},
        '田辺裕信':   {'東京': 7,  '中山': 7,  '阪神': 3,  '京都': 2},
        '藤岡佑介':   {'東京': 6,  '中山': 4,  '阪神': 8,  '京都': 8},
        '幸英明':     {'東京': 4,  '中山': 4,  '阪神': 7,  '京都': 7},
        '大野拓弥':   {'東京': 7,  '中山': 6,  '阪神': 2,  '京都': 2},
        '石川裕紀人': {'東京': 5,  '中山': 7,  '阪神': 3,  '京都': 2},
        '荻野極':     {'東京': 5,  '中山': 4,  '阪神': 6,  '京都': 6},
        '北村宏司':   {'東京': 4,  '中山': 3,  '阪神': 2,  '京都': 2},
        '丸山元気':   {'東京': 3,  '中山': 4,  '阪神': 1,  '京都': 1},
        '石橋脩':     {'東京': 3,  '中山': 4,  '阪神': 2,  '京都': 2},
        '武藤雅':     {'東京': 3,  '中山': 3,  '阪神': 1,  '京都': 1},
        '内田博幸':   {'東京': 4,  '中山': 4,  '阪神': 1,  '京都': 1},
        '木幡巧也':   {'東京': 2,  '中山': 4,  '阪神': 1,  '京都': 1},
        '吉田隼人':   {'東京': 4,  '中山': 4,  '阪神': 4,  '京都': 4},
        '永島まなみ': {'東京': 2,  '中山': 1,  '阪神': 4,  '京都': 4},
        '和田竜二':   {'東京': 2,  '中山': 2,  '阪神': 4,  '京都': 4},
        '古川吉洋':   {'東京': 1,  '中山': 1,  '阪神': 3,  '京都': 3},
        '秋山稔樹':   {'東京': 2,  '中山': 3,  '阪神': 1,  '京都': 1},
        '小沢大仁':   {'東京': 1,  '中山': 1,  '阪神': 3,  '京都': 3},
        '角田大河':   {'東京': 2,  '中山': 1,  '阪神': 4,  '京都': 4},
        '今村聖奈':   {'東京': 1,  '中山': 1,  '阪神': 3,  '京都': 3},
        '松若風馬':   {'東京': 2,  '中山': 2,  '阪神': 4,  '京都': 4},
        '斎藤新':     {'東京': 3,  '中山': 3,  '阪神': 4,  '京都': 4},
        '国分優作':   {'東京': 1,  '中山': 1,  '阪神': 3,  '京都': 3},
        '国分恭介':   {'東京': 1,  '中山': 1,  '阪神': 3,  '京都': 3},
        '富田暁':     {'東京': 3,  '中山': 2,  '阪神': 4,  '京都': 4},
        '高田潤':     {'東京': 1,  '中山': 1,  '阪神': 1,  '京都': 1},
        '太宰啓介':   {'東京': 1,  '中山': 1,  '阪神': 2,  '京都': 2},
        '酒井学':     {'東京': 1,  '中山': 1,  '阪神': 3,  '京都': 3},
        '柴田大知':   {'東京': 1,  '中山': 3,  '阪神': 1,  '京都': 1},
        '長岡禎仁':   {'東京': 1,  '中山': 1,  '阪神': 2,  '京都': 2},
        '水口優也':   {'東京': 1,  '中山': 1,  '阪神': 2,  '京都': 2},
        '舟山瑠泉':   {'東京': 2,  '中山': 4,  '阪神': 2,  '京都': 2},
        'ゴンザルベス':{'東京': 14, '中山': 10, '阪神': 12, '京都': 11},
        'その他':     {'東京': 5,  '中山': 5,  '阪神': 5,  '京都': 5}
    }

    jockey = base_data.get('jockey')
    if venue in ['東京', '中山', '阪神', '京都'] and jockey in jockey_master_data:
        score += jockey_master_data[jockey].get(venue, 0)
    
    sire_individual_data = {
        'ディープインパクト': {'東京': 20, '中山': 4,  '阪神': 15, '京都': 18},
        'キズナ':             {'東京': 16, '中山': 12, '阪神': 18, '京都': 14},
        'エピファネイア':     {'東京': 14, '中山': 11, '阪神': 19, '京都': 12},
        'ダイワメジャー':     {'東京': 8,  '中山': 20, '阪神': 6,  '京都': 5},
        'ロードカナロア':     {'東京': 12, '中山': 13, '阪神': 10, '京都': 16},
        'モーリス':           {'東京': 10, '中山': 15, '阪神': 9,  '京都': 10},
        'ハーツクライ':       {'東京': 17, '中山': 6,  '阪神': 12, '京都': 13},
        'スワーヴリチャード': {'東京': 15, '中山': 8,  '阪神': 12, '京都': 11},
        'ドゥラメンテ':       {'東京': 13, '中山': 10, '阪神': 14, '京都': 11},
        'シルバーステート':   {'東京': 6,  '中山': 12, '阪神': 8,  '京都': 13},
        'ハービンジャー':     {'東京': 8,  '中山': 10, '阪神': 7,  '京都': 4},
        'ルーラーシップ':     {'東京': 9,  '中山': 3,  '阪神': 10, '京都': 8}
    }

    sire_group_data = {
        'ディープインパクト系':      {'東京': 15, '中山': 9,  '阪神': 13, '京都': 14},
        'その他サンデーサイレンス系': {'東京': 10, '中山': 12, '阪神': 10, '京都': 10},
        'キングマンボ系':           {'東京': 13, '中山': 11, '阪神': 11, '京都': 14},
        'ロベルト系':               {'東京': 9,  '中山': 16, '阪神': 12, '京都': 8},
        'ノーザンダンサー系・外国産馬':{'東京': 11, '中山': 11, '阪神': 9,  '京都': 5},
        'ナスルーラ系・その他':      {'東京': 6,  '中山': 7,  '阪神': 5,  '京都': 7},
        '完全該当なし':             {'東京': 0,  '中山': 0,  '阪神': 0,  '京都': 0}
    }

    sire = base_data.get('sire', '（個別指定なし）')
    sire_group = base_data.get('sire_group')
    sire_score = 0

    if venue in ['東京', '中山', '阪神', '京都']:
        if sire != '（個別指定なし）' and sire in sire_individual_data:
            sire_score = sire_individual_data[sire].get(venue, 0)
        elif sire_group in sire_group_data:
            sire_score = sire_group_data[sire_group].get(venue, 0)
            
    score += sire_score

    if base_data.get('prev_class') != '新馬（前走なし）':
        prev_distance = base_data.get('prev_distance')
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

    gate = base_data.get('gate_number')
    if venue == '中山' and gate in [1, 2, 3, 4]: score += 13
    elif venue == '東京' and gate in [9, 10, 11, 12, 13, 14]: score += 5
    
    # 🔥追加要素（UIと同期）
    if base_data.get('first_blinker', False):
        score += 10

    prev_condition = base_data.get('prev_condition', '良')
    current_condition = current_race.get('track_condition', '良')

    if prev_condition in ['重', '不良'] and current_condition in ['良', '稍重']:
        score += 8

    style = base_data.get('running_style', '先行')
    if venue == '東京':
        if style == '差し':
            score += 5
        elif style == '追込':
            score += 3
    
    return score

st.title("JRA芝1600 期待値判別エンジン")

st.header("レース環境設定")
col1, col2 = st.columns(2)
with col1:
    venue = st.selectbox("開催競馬場", ["東京", "阪神", "中山", "京都", "新潟", "小倉", "福島", "中京", "函館", "札幌"])
with col2:
    track_condition = st.selectbox("馬場状態", ["良", "稍重", "重", "不良"])

current_race_info = {"venue": venue, "track_condition": track_condition}

st.header("出走馬データ入力")
if "horses" not in st.session_state:
    st.session_state.horses = [
        {'gate_number': 16, 'jockey': '川田将雅', 'sire': '（個別指定なし）', 'sire_group': 'キングマンボ系', 'prev_distance': 1800, 'prev_venue': '中山', 'prev_class': 'G2', 'prev_rank': 11, 'time_diff': 1.6, 'agari_fastest': False, 'is_class_up': False, 'first_blinker': False, 'prev_condition': '良', 'running_style': '先行'},
        {'gate_number': 12, 'jockey': '戸崎圭太', 'sire': 'エピファネイア', 'sire_group': 'ロベルト系', 'prev_distance': 1600, 'prev_venue': '東京', 'prev_class': '平場', 'prev_rank': 1, 'time_diff': 0.0, 'agari_fastest': False, 'is_class_up': True, 'first_blinker': False, 'prev_condition': '良', 'running_style': '先行'}
    ]

if st.button("馬を追加"):
    st.session_state.horses.append({'gate_number': 1, 'jockey': 'C.ルメール', 'sire': '（個別指定なし）', 'sire_group': 'ディープインパクト系', 'prev_distance': 1600, 'prev_venue': '東京', 'prev_class': '平場', 'prev_rank': 1, 'time_diff': 0.0, 'agari_fastest': False, 'is_class_up': False, 'first_blinker': False, 'prev_condition': '良', 'running_style': '先行'})

jockey_list = ['C.ルメール', 'J.モレイラ', '川田将雅', '坂井瑠星', '戸崎圭太', '横山武史', '武豊', 'D.レーン', '西村淳也', '岩田望来', '津村明秀', '菅原明良', '松山弘平', '鮫島克駿', '団野大成', '三浦皇成', '岩田康誠', 'M.デムーロ', '丹内祐次', '佐々木大輔', '横山和生', '北村友一', '田辺裕信', '藤岡佑介', '幸英明', '大野拓弥', '石川裕紀人', '荻野極', '北村宏司', '丸山元気', '石橋脩', '武藤雅', '内田博幸', '木幡巧也', '吉田隼人', '永島まなみ', '和田竜二', '古川吉洋', '秋山稔樹', '小沢大仁', '角田大河', '今村聖奈', '松若風馬', '斎藤新', '国分優作', '国分恭介', '富田暁', '高田潤', '太宰啓介', '酒井学', '柴田大知', '長岡禎仁', '水口優也', '舟山瑠泉', 'ゴンザルベス', 'その他']

updated_horses = []
for i, h in enumerate(st.session_state.horses):
    with st.expander(f"馬番 {h['gate_number']} の設定", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            h['gate_number'] = st.number_input(f"馬番", min_value=1, max_value=18, value=int(h['gate_number']), key=f"gate_{i}")
            h['jockey'] = st.selectbox(f"騎手名", jockey_list, index=jockey_list.index(h['jockey'] if h['jockey'] in jockey_list else 'その他'), key=f"jock_{i}")
        with c2:
            sire_list = ['（個別指定なし）', 'ディープインパクト', 'キズナ', 'エピファネイア', 'ダイワメジャー', 'ロードカナロア', 'モーリス', 'ハーツクライ', 'スワーヴリチャード', 'ドゥラメンテ', 'シルバーステート', 'ハービンジャー', 'ルーラーシップ']
            h['sire'] = st.selectbox(f"種牡馬名", sire_list, index=sire_list.index(h.get('sire', '（個別指定なし）')), key=f"sire_name_{i}")
            sire_group_list = ['ディープインパクト系', 'その他サンデーサイレンス系', 'キングマンボ系', 'ロベルト系', 'ノーザンダンサー系・外国産馬', 'ナスルーラ系・その他', '完全該当なし']
            h['sire_group'] = st.selectbox(f"血統系統", sire_group_list, index=sire_group_list.index(h.get('sire_group', '完全該当なし')), key=f"sireg_{i}")
        with c3:
            h['prev_class'] = st.selectbox(f"前走クラス", ['平場', 'G3', 'G2', 'G1', '新馬（前走なし）'], index=['平場', 'G3', 'G2', 'G1', '新馬（前走なし）'].index(h.get('prev_class', '平場')), key=f"pclass_{i}")
        
        # 追加要素のUI
        c4, c5, c6 = st.columns(3)
        with c4:
            h['running_style'] = st.selectbox("脚質", ["逃げ", "先行", "差し", "追込"], index=["逃げ", "先行", "差し", "追込"].index(h.get('running_style', '先行')), key=f"style_{i}")
        with c5:
            h['first_blinker'] = st.checkbox("初ブリンカー", value=h.get('first_blinker', False), key=f"blink_{i}")
        with c6:
            h['prev_condition'] = st.selectbox("前走馬場状態", ["良", "稍重", "重", "不良"], index=["良", "稍重", "重", "不良"].index(h.get('prev_condition', '良')), key=f"pcond_{i}")

        if h['prev_class'] != '新馬（前走なし）':
            cc1, cc2, cc3 = st.columns(3)
            with cc1:
                h['prev_distance'] = st.number_input(f"前走距離", value=int(h.get('prev_distance', 1600)), step=200, key=f"pdist_{i}")
                h['prev_venue'] = st.selectbox(f"前走競馬場", ["東京", "中山", "阪神", "京都", "新潟", "小倉", "福島", "中京", "函館", "札幌"], index=["東京", "中山", "阪神", "京都", "新潟", "小倉", "福島", "中京", "函館", "札幌"].index(h.get('prev_venue', '東京')), key=f"pvenue_{i}")
            with cc2:
                h['prev_rank'] = st.number_input(f"前走着順", min_value=1, max_value=18, value=int(h.get('prev_rank', 1)), key=f"prank_{i}")
                h['time_diff'] = st.number_input(f"前走タイム差", value=float(h.get('time_diff', 0.0)), step=0.1, key=f"tdiff_{i}")
            with cc3:
                h['agari_fastest'] = st.checkbox("前走上がり最速", value=h.get('agari_fastest', False), key=f"agari_{i}")
                h['is_class_up'] = st.checkbox("今回昇級戦", value=h.get('is_class_up', False), key=f"class_{i}")
            h['prev_performance'] = ['上がり最速'] if h['agari_fastest'] else []
        
        updated_horses.append(h)

st.session_state.horses = updated_horses

st.write("---")
if st.button("期待値ランキングを計算", type="primary"):
    ranking_list = []
    for horse in st.session_state.horses:
        score = JRA_Mile_Expectation_Engine(horse, current_race_info)
        if score >= 60: band, color = "S", "#FF3333"
        elif score >= 50: band, color = "A", "#FFA500"
        elif score >= 38: band, color = "B", "#1E90FF"
        else: band, color = "C", "#778899"
        ranking_list.append({'gate_number': horse['gate_number'], 'score': score, 'jockey': horse['jockey'], 'band': band, 'color': color})
    
    ranking_list.sort(key=lambda x: x['score'], reverse=True)
    st.header("判定結果")
    for rank, h_info in enumerate(ranking_list, 1):
        st.markdown(f"### Rank {rank} [<span style='color:{h_info['color']}; font-weight:bold;'>{h_info['band']}</span>]: 馬番 {h_info['gate_number']} ({h_info['jockey']}) -> **{h_info['score']}** POINTS", unsafe_allow_html=True)

```