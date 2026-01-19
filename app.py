import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Data Analytics Pro", layout="wide")
st.title("📊 Student Performance Intelligence")

# 1. OBTAINING DATA
try:
    df = pd.read_csv('student-performance.csv')
    
    # --- RANKING LOGIC (Calculated before filtering) ---
    df['Rank_Num'] = df['Grade'].rank(ascending=False, method='min').astype(int)

    def format_rank(val):
        if 11 <= val <= 13:
            return f"{val}th"
        last_digit = val % 10
        if last_digit == 1: return f"{val}st"
        if last_digit == 2: return f"{val}nd"
        if last_digit == 3: return f"{val}rd"
        return f"{val}th"

    df['Rank'] = df['Rank_Num'].apply(format_rank)

    # Re-order columns to put Rank first
    other_cols = [col for col in df.columns if col not in ['Rank', 'Rank_Num']]
    df = df[['Rank'] + other_cols]

    # 2. SIDEBAR FILTERING
    st.sidebar.header("Filter Data")
    min_score = st.sidebar.slider("Minimum Score", 0, 100, 50)
    filtered_df = df[df['Grade'] >= min_score].sort_values(by='Grade', ascending=False)

    # 3. TOP PERFORMER HIGHLIGHT
    if not filtered_df.empty:
        top_student_row = filtered_df.iloc[0] 
        st.success(f"🏆 **Top Performer in this range:** {top_student_row['Name']} (Rank: {top_student_row['Rank']}) with {top_student_row['Grade']}%")
    else:
        st.error("No students found in this score range.")

    # 4. DASHBOARD LAYOUT
    col1, col2 = st.columns(2)

    with col1:
        st.write("### 🥇 Leaderboard (Top 10)")
        st.dataframe(filtered_df.head(10), hide_index=True) 

    with col2:
        st.write("### 🏆 Top 3 Performers")
        top_3 = df.nlargest(3, 'Grade')
        st.bar_chart(data=top_3, x='Name', y='Grade', color="#2ecc71")

    # 5. DISTRIBUTION CHART
    st.write("### 📈 Overall Grade Distribution")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.histplot(df['Grade'], kde=True, color="skyblue", ax=ax)
    st.pyplot(fig) 

    # 6. EXPORT TOOLS
    st.divider()
    st.write("### ⬇️ Export Filtered Data")
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download filtered list as CSV",
        data=csv,
        file_name='filtered_student_results.csv',
        mime='text/csv',
    )

except FileNotFoundError:
    st.warning("⚠️ CSV file not found. Make sure 'student-performance.csv' is in the same folder!")