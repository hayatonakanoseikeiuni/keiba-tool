def JRA_Mile_Expectation_Engine(horse_name, base_data, current_race):
    """
    JRA競馬場芝1600期待値判別エンジン
    """
    score = 20  # 初期値

    # ==========================================
    # 1. 騎手マスタ
    # ==========================================
    jockey = base_data.get('jockey')
    jockey_points = {
        'C.ルメール': 20, 'J.モレイラ': 19, '川田将雅': 18, 
        '坂井瑠星': 16, '戸崎圭太': 16, '横山武史': 12, '丹内祐次': 3
    }
    j_score = jockey_points.get(jockey, 5)
    score += j_score

    # ==========================================
    # 2. 血統マスタ（種牡馬）
    # ==========================================
    sire = base_data.get('sire')
    sire_group = base_data.get('sire_group')
    track_condition = current_race.get('track_condition', '良')
    
    if track_condition in ['重', '不良']:
        if sire_group in ['ディープ系', 'ロードカナロア系']:
            s_score = 5
        elif sire_group == 'ロベルト系' or sire == 'ハービンジャー':
            s_score = 15 + 12  # ベース15点 + 道悪パワーバフ12点
        else:
            s_score = 8
    else:
        if sire_group == 'ディープ系': s_score = 15
        elif sire == 'ロードカナロア': s_score = 12
        elif sire_group == 'キングマンボ系': s_score = 13
        elif sire == 'エピファネイア': s_score = 19
        elif sire == 'キズナ': s_score = 18
        else: s_score = 10
        
    score += s_score

    # ==========================================
    # 3. 前走からの「距離ギャップ」
    # ==========================================
    prev_distance = base_data.get('prev_distance')
    venue = current_race.get('venue')
    dist_score = 0
    
    if prev_distance >= 2000:
        if venue in ['東京', '阪神']:
            dist_score = 14
        else:
            dist_score = 5
    elif prev_distance == 1800:
        dist_score = 6
    elif prev_distance == 1400:
        dist_score = 4
        
    score += dist_score

    # ==========================================
    # 4. 前走からの「競馬場ギャップ」（コース形状変化）
    # ==========================================
    prev_venue = base_data.get('prev_venue')
    venue_score = 0
    
    if prev_venue in ['中山', '小倉', '福島', '函館', '札幌'] and venue in ['東京', '阪神']:
        venue_score = 11
    elif prev_venue in ['東京', '京都', '新潟'] and venue == '中山':
        venue_score = 3
        
    score += venue_score

    # ==========================================
    # 5. 前走成績・着差ボーナスの連動フィルター
    # ==========================================
    prev_rank = base_data.get('prev_rank')
    time_difference = base_data.get('time_diff')
    prev_class = base_data.get('prev_class')
    prev_performance = base_data.get('prev_performance', [])
    has_best_agari = '上がり最速' in prev_performance
    
    perf_score = 0
    is_disqualified = False  # 大敗によるギャップ没収フラグ

    # Aパターン：前走好走（1着〜3着）
    if prev_rank <= 1:
        perf_score += 8 if not base_data.get('is_class_up') else 4
    elif 2 <= prev_rank <= 3:
        perf_score += 6

    # Bパターン：掲示板確保、またはクラス問わず0.3秒以内の大接戦
    elif 4 <= prev_rank <= 5 or time_difference <= 0.3:
        perf_score += 3

    # Cパターン：6着以下の大敗ケース（着差ボーナスの判定）
    else:
        if prev_class in ['G1', 'G2', 'G3']:
            # 重賞ボーナス：相手が強いので2.0秒未満なら見直し対象
            if time_difference < 2.0:
                perf_score += 7
            else:
                is_disqualified = True
        else:
            # 平場ボーナス：0.9秒以内のタイム差が絶対条件
            if time_difference >= 2.0:
                is_disqualified = True
            elif time_difference <= 0.9 and has_best_agari:
                # 平場の僅差大敗 × 上がり最速の最強コンボ
                perf_score += 18
            elif time_difference <= 0.9:
                perf_score += 7
            elif has_best_agari:
                perf_score += 11

    # 大敗フラグが立ったら、累積していた距離・競馬場ギャップをゼロ（没収）にする
    if is_disqualified:
        score -= dist_score
        score -= venue_score
        perf_score = 0

    score += perf_score

    # ==========================================
    # 6. 当日の「枠順ギャップ」
    # ==========================================
    gate = current_race.get('gate_number')
    gate_score = 0
    
    if venue == '中山':
        if gate in [1, 2, 3, 4]: 
            gate_score = 13
    elif venue == '東京':
        if gate in [9, 10, 11, 12, 13, 14]: 
            gate_score = 5
            
    score += gate_score
    return score


# ==========================================
# 出走馬一括ランキング処理メインスクリプト
# ==========================================
if __name__ == "__main__":
    # 当日のレース環境設定（検証したいレースに合わせて書き換え）
    current_race_info = {
        'venue': '東京',
        'track_condition': '良',
    }

    # 出走馬全頭のデータベース
    field_horses = [
        {
            'name': 'ソニックライン',
            'gate_number': 16,
            'jockey': 'ゴンサルベス',
            'sire': 'キングカメハメハ',
            'sire_group': 'キングマンボ系',
            'prev_distance': 1800,
            'prev_venue': '中山',
            'prev_class': 'G2',
            'prev_rank': 11,
            'time_diff': 1.6,
            'prev_performance': [],
            'is_class_up': False
        },
        {
            'name': 'ゴディアーモ',
            'gate_number': 12,
            'jockey': '戸崎圭太',
            'sire': 'エピファネイア',
            'sire_group': 'ロベルト系',
            'prev_distance': 1600,
            'prev_venue': '東京',
            'prev_class': '平場',
            'prev_rank': 1,
            'time_diff': 0.0,
            'prev_performance': [],
            'is_class_up': True
        },
        {
            'name': 'タイセフレッサ',
            'gate_number': 8,
            'jockey': '岩田望来',
            'sire': 'リアルスティール',
            'sire_group': 'ディープ系',
            'prev_distance': 1600,
            'prev_venue': '京都',
            'prev_class': '平場',
            'prev_rank': 5,
            'time_diff': 0.6,
            'prev_performance': [],
            'is_class_up': False
        },
        {
            'name': 'スワローシチー',
            'gate_number': 3,
            'jockey': '荻野極',
            'sire': 'コパノリッキー',
            'sire_group': 'サンデー系',
            'prev_distance': 1600,
            'prev_venue': '新潟',
            'prev_class': '平場',
            'prev_rank': 2,
            'time_diff': 0.1,
            'prev_performance': [],
            'is_class_up': False
        }
    ]

    # 各馬のスコアをループで計算して格納
    ranking_list = []
    for horse in field_horses:
        calculated_score = JRA_Mile_Expectation_Engine(horse['name'], horse, current_race_info)
        ranking_list.append({
            'name': horse['name'],
            'score': calculated_score,
            'jockey': horse['jockey']
        })

    # スコアの高い順（降順）に並び替え
    ranking_list.sort(key=lambda x: x['score'], reverse=True)

    # ランキングの出力
    print("=== JRA競馬場芝1600期待値判別エンジン ===")
    for rank, h_info in enumerate(ranking_list, 1):
        print(f"Rank {rank}: {h_info['name']:<12} ({h_info['jockey']}) -> {h_info['score']} POINTS")
    print("==========================================")