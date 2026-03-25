import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform


# 1) 한글 폰트 설정 (Streamlit Cloud 및 로컬 공용)
# --------------------------------------------------
def set_korean_font():
    if platform.system() == 'Windows':
        # 윈도우 로컬 환경
        plt.rc('font', family='Malgun Gothic')
    else:
        # Streamlit Cloud(리눅스) 환경 - packages.txt의 fonts-nanum 이용
        plt.rc('font', family='NanumGothic')

    plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지


# --------------------------------------------------

# 2) CSV 파일 불러오기
def load_data(file):
    df = pd.read_csv(file)
    return df


# 3) 데이터 탐색 및 요약 통계 출력
def show_data_exploration(df):
    st.header("데이터 탐색")
    st.subheader("데이터 미리보기 (상위 5행)")
    st.dataframe(df.head(5), use_container_width=True)

    st.subheader("데이터 주요 통계 요약")
    st.write(df.describe())


# 4) 막대그래프 시각화
def draw_bar_chart(df):
    st.header("항목 간 비교 (막대그래프)")
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

    if not numeric_cols:
        st.warning("분석할 수 있는 수치형 데이터가 없습니다.")
        return

    target_col = st.selectbox("비교할 항목을 선택하세요", numeric_cols, key="bar_select")

    if st.button("막대그래프 생성"):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=df, x='요일', y=target_col, ax=ax)
        ax.set_title(f"요일별 {target_col} 비교")
        st.pyplot(fig)


# 5) 산점도 및 추세선 시각화
def draw_scatter_plot(df):
    st.header("변수 관계 분석 (산점도)")
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

    if len(numeric_cols) < 2:
        st.warning("변수 간 관계를 분석하려면 최소 2개의 수치형 항목이 필요합니다.")
        return

    col1, col2 = st.columns(2)
    with col1:
        x_axis = st.selectbox("X축 선택", numeric_cols, key="x_select")
    with col2:
        y_axis = st.selectbox("Y축 선택", numeric_cols, key="y_select")

    show_reg = st.checkbox("추세선(회귀선) 표시")

    if st.button("산점도 생성"):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=df, x=x_axis, y=y_axis, ax=ax)

        if show_reg:
            sns.regplot(data=df, x=x_axis, y=y_axis, scatter=False, ax=ax, color='red')
            ax.set_title(f"{x_axis}와 {y_axis}의 관계 및 추세선")
        else:
            ax.set_title(f"{x_axis}와 {y_axis}의 관계")

        st.pyplot(fig)


# 6) 메인 함수
def main():
    st.set_page_config(page_title="카페 데이터 분석", layout="wide")
    st.title("카페 요일별 판매 데이터 분석 프로그램")

    # 폰트 설정 실행
    set_korean_font()

    uploaded_file = st.file_uploader("cafe_sales.csv 파일을 업로드하세요", type=["csv"])

    if uploaded_file is not None:
        df = load_data(uploaded_file)

        show_data_exploration(df)
        st.divider()
        draw_bar_chart(df)
        st.divider()
        draw_scatter_plot(df)
    else:
        st.info("CSV 파일을 업로드하면 분석 기능이 활성화됩니다.")


if __name__ == "__main__":
    main()