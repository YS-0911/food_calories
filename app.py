import streamlit as st
import pandas as pd
import plotly.express as px
import math

# 데이터 불러오기
food_df = pd.read_csv("농림수산식품교육문화정보원_칼로리 정보_20190926.csv", encoding='cp949')
exercise_df = pd.read_csv("1시간 운동 시 소모되는 칼로리 표.csv", encoding='utf-8-sig')

# 빈공간 제거
food_df = food_df.dropna(subset=['음식명'])

# 제목
st.set_page_config(page_title="얼마나 먹은게야?", layout="wide")
st.title("🍱 얼마나 먹은게야?")
st.markdown("### 하루 섭취 음식의 영양소 총량과 칼로리, 그리고 운동 추천까지!")

# 사이드바
st.sidebar.header("🍽️ 오늘 먹은 음식 선택")
food_list = food_df['음식명'].unique().tolist()

st.sidebar.subheader("🌅 아침")
breakfast = st.sidebar.multiselect("아침 식사:", food_list, key="breakfast")

st.sidebar.subheader("🌞 점심")
lunch = st.sidebar.multiselect("점심 식사:", food_list, key="lunch")

st.sidebar.subheader("🌙 저녁")
dinner = st.sidebar.multiselect("저녁 식사:", food_list, key="dinner")

# 전체 선택한 음식
all_selected = {
    "🌅 아침": breakfast,
    "🌞 점심": lunch,
    "🌙 저녁": dinner
}

# 메인
st.markdown("<div style='background-color:#fef9e7;padding:20px;border-radius:10px;'>", unsafe_allow_html=True)
st.subheader("🍽️ 오늘 먹은 음식 목록")

combined_selection = []
for meal, foods in all_selected.items():
    for food in foods:
        combined_selection.append({"meal": meal, "food": food})

if combined_selection:
    df_display = pd.DataFrame(combined_selection)
    unique_foods = df_display['food'].unique().tolist()

    for meal, foods in all_selected.items():
        if foods:
            st.markdown(f"**{meal}**: {', '.join(foods)}")

    st.markdown("</div>", unsafe_allow_html=True)

    selected_df = food_df[food_df['음식명'].isin(unique_foods)]

    st.markdown("<div style='background-color:#e8f8f5;padding:20px;border-radius:10px;margin-top:20px;'>", unsafe_allow_html=True)
    st.subheader("🥗 하루 섭취 영양소 비율")

    nutrients = ['탄수화물(g)', '단백질(g)', '지방(g)']
    nutrient_sums = selected_df[nutrients].sum()

    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(names=nutrient_sums.index, values=nutrient_sums.values,
                     title='탄수화물 / 단백질 / 지방 비율', color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("### 💡 총 영양소 합산")
        for nutrient in nutrients:
            st.markdown(f"**{nutrient}**: {nutrient_sums[nutrient]:.1f} g")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='background-color:#f4ecf7;padding:20px;border-radius:10px;margin-top:20px;'>", unsafe_allow_html=True)
    st.markdown("### 📋 영양소 상세 정보")
    st.dataframe(
        selected_df.set_index('음식명')[['1인분칼로리(kcal)', '탄수화물(g)', '단백질(g)', '지방(g)', '콜레스트롤(g)', '식이섬유(g)', '나트륨(g)']],
        use_container_width=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='background-color:#fdebd0;padding:20px;border-radius:10px;margin-top:20px;'>", unsafe_allow_html=True)
    total_kcal = selected_df['1인분칼로리(kcal)'].sum()
    st.markdown(f"## 🔥 총 섭취 칼로리: **{total_kcal:.1f} kcal**")
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("💪 얼마나 운동해야 할까?"):
        st.markdown("<div style='background-color:#d6eaf8;padding:20px;border-radius:10px;margin-top:20px;'>", unsafe_allow_html=True)
        st.markdown("### 🏃 운동 추천")

        exercise_df['시간(분)'] = exercise_df['kcal'].apply(lambda x: math.ceil(total_kcal / x * 60))
        exercise_df_sorted = exercise_df.sort_values('시간(분)').reset_index(drop=True)

        st.dataframe(
            exercise_df_sorted.rename(columns={"운동의 종류": "운동", "kcal": "1시간 소모 kcal"}).style.hide(axis='index'),
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown("</div>", unsafe_allow_html=True)
    st.info("왼쪽에서 아침, 점심, 저녁으로 오늘 먹은 음식을 입력해주세요! 🍙")