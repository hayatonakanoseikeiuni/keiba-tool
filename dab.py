import streamlit as st
import pandas as pd

st.set_page_config(page_title="ダービー推定オッズ計算機")

st.title("🏇 ダービー推定オッズ計算機")

# 1. 母数の設定（120固定）
total_votes = 120

# 2. エントリー情報の入力
num_entries = st.number_input("エントリー数", min_value=2, max_value=20, value=5)

st.subheader("各エントリーの名前と推定得票数を入力")
entries = []
for i in range(num_entries):
    col1, col2 = st.columns([2, 1])
    with col1:
        name = st.text_input(f"エントリー {i+1} 名前", value=f"エントリー {i+1}", key=f"name_{i}")
    with col2:
        count = st.number_input(f"得票数", min_value=0, value=0, key=f"count_{i}")
    entries.append({"name": name, "count": count})

# 3. 推定オッズ計算
if st.button("オッズを算出"):
    total_input = sum(e["count"] for e in entries)
    
    # 計算ロジック: 母数(120) / 得票数
    results = []
    for e in entries:
        if e["count"] > 0:
            odds = total_votes / e["count"]
            odds_str = f"{odds:.2f} 倍"
        else:
            odds_str = "---"
        
        results.append({
            "エントリー名": e["name"],
            "推定得票数": e["count"],
            "推定オッズ": odds_str
        })
    
    # 4. 結果表示
    df = pd.DataFrame(results)
    st.table(df)
    
    st.write(f"---")
    st.write(f"合計得票数: {total_input} / {total_votes}")