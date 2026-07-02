import streamlit as st
import pandas as pd

st.title("🏇 ダービー・オッズ計算機")

# 1. 設定：参加人数と対象の数
total_votes = 120
num_entries = st.number_input("エントリー数（馬やチームの数）", min_value=2, value=5)

# 2. 投票数の入力欄を動的に作成
st.subheader("各エントリーへの投票数を入力してください")
votes = {}
for i in range(num_entries):
    votes[f"エントリー {i+1}"] = st.number_input(f"エントリー {i+1} の得票数", min_value=0, value=0)

# 3. オッズ計算ロジック
if st.button("オッズを計算"):
    current_total = sum(votes.values())
    
    if current_total == 0:
        st.warning("まだ票が入力されていません。")
    elif current_total > total_votes:
        st.error(f"合計票数（{current_total}）が母数（{total_votes}）を超えています！")
    else:
        results = []
        for name, count in votes.items():
            if count > 0:
                # オッズ = 総投票数 / そのエントリーの得票数
                odds = total_votes / count
            else:
                odds = 0 # 0票の場合はオッズなし
            
            results.append({"エントリー名": name, "得票数": count, "オッズ": f"{odds:.2f} 倍"})
        
        # 4. 結果の表示
        df = pd.DataFrame(results)
        st.table(df)
        
        remaining = total_votes - current_total
        st.info(f"現在の投票数: {current_total} / {total_votes} (残り: {remaining})")