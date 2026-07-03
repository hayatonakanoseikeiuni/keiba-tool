import streamlit as st
import pandas as pd

st.set_page_config(page_title="uni夏合宿ダービーオッズ計算機")

st.title("uni夏合宿ダービーオッズ計算機")

# 母数120は固定
total_votes = 120

# エントリー数の指定
num_entries = st.number_input("エントリー数", min_value=2, max_value=20, value=5)

st.subheader("各エントリーの名前と得票数を入力")

# データ入力欄
entries = []
for i in range(num_entries):
    # 名前と得票数を横並びで入力
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(f"名前 {i+1}", value=f"エントリー {i+1}", key=f"name_{i}")
    with col2:
        count = st.number_input(f"得票数 {i+1}", min_value=0, value=0, key=f"count_{i}")
    
    entries.append({"name": name, "count": count})

# 計算処理
if st.button("オッズを計算"):
    results = []
    total_input = sum(e["count"] for e in entries)
    
    for e in entries:
        # オッズ計算（母数 120 / 得票数）
        if e["count"] > 0:
            odds = total_votes / e["count"]
            odds_str = f"{odds:.2f} 倍"
        else:
            odds_str = "---"
            
        results.append({
            "名前": e["name"],
            "得票数": e["count"],
            "オッズ": odds_str
        })
    
    # 結果を表示
    df = pd.DataFrame(results)
    st.table(df)
    
    st.divider()
    st.write(f"合計得票数: {total_input} / {total_votes}")
    
    if total_input > total_votes:
        st.error("警告: 合計得票数が母数を超えています")