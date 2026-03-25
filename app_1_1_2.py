import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
from matplotlib import font_manager, rc

import platform

if platform.system() == 'Windows':
    # 윈도우(로컬) 환경
    plt.rc('font', family='Malgun Gothic')
else:
    # Streamlit Cloud(리눅스) 환경
    # 기본 설치된 폰트 중 한글을 지원하는 DejaVu Sans 등을 사용하거나
    # 폰트 경로를 직접 지정하지 않아도 아래 설정으로 마이너스 깨짐을 방지합니다.
    plt.rcParams['axes.unicode_minus'] = False

# 1) 그래프 내 한글 깨짐 방지를 위한 폰트 설정 [cite: 433, 766]
def set_korean_font():
    for font in ["Malgun Gothic", "AppleGothic", "NanumGothic"]:
        try:
            rcParams["font.family"] = font
            break
        except Exception:
            pass
    rcParams["axes.unicode_minus"] = False  # 마이너스 기호 깨짐 방지 [cite: 442, 773]


# 2) CSV 파일 불러오기 [cite: 48, 209, 774]
def load_data(file):
    df = pd.read_csv(file)
    return df


# 3) 데이터 탐색 및 요약 통계 출력 [cite: 70, 212, 777]
def show_data_exploration(df):
    st.header("데이터 탐색")
    # 상위 5행 데이터 출력 [cite: 71, 213, 780]
    st.subheader("데이터 미리보기 (상위 5행)")
    st.dataframe(df.head(5), use_container_width=True)

    # 주요 통계 요약 정보 출력 [cite: 73, 80, 1045]
    st.subheader("데이터 주요 통계 요약")
    st.write(df.describe())


# 4) 막대그래프 시각화 (항목 간 비교) [cite: 164, 234, 1049]
def draw_bar_chart(df):
    st.header("항목 간 비교 (막대그래프)")
    # 수치형 데이터 컬럼만 선택 [cite: 218, 517]
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    target_col = st.selectbox("비교할 항목을 선택하세요", numeric_cols)

    if st.button("막대그래프 생성"):
        fig, ax = plt.subplots()
        # 요일별 선택 항목의 평균값 시각화 [cite: 170, 299, 1052]
        sns.barplot(data=df, x='요일', y=target_col, ax=ax)
        ax.set_title(f"요일별 {target_col} 비교")
        st.pyplot(fig)


# 5) 산점도 및 추세선 시각화 (변수 관계 분석) [cite: 701, 794, 1058]
def draw_scatter_plot(df):
    st.header("변수 관계 분석 (산점도)")
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

    col1, col2 = st.columns(2)
    with col1:
        x_axis = st.selectbox("X축 선택", numeric_cols)
    with col2:
        y_axis = st.selectbox("Y축 선택", numeric_cols)

    # 추세선 표시 여부 선택 체크박스 [cite: 953, 995]
    show_reg = st.checkbox("추세선(회귀선) 표시")

    if st.button("산점도 생성"):
        fig, ax = plt.subplots()
        # 산점도 그리기 [cite: 710, 884, 1059]
        sns.scatterplot(data=df, x=x_axis, y=y_axis, ax=ax)

        # 추세선 추가 기능 [cite: 946, 981, 1060]
        if show_reg:
            sns.regplot(data=df, x=x_axis, y=y_axis, scatter=False, ax=ax, color='red')
            ax.set_title(f"{x_axis}와 {y_axis}의 관계 및 추세선")
        else:
            ax.set_title(f"{x_axis}와 {y_axis}의 관계")

        st.pyplot(fig)


# 6) 메인 함수 [cite: 245, 463, 809]
def main():
    st.title("카페 요일별 판매 데이터 분석 프로그램")
    set_korean_font()

    # 파일 업로드 영역 [cite: 193, 250, 471]
    uploaded_file = st.file_uploader("cafe_sales.csv 파일을 업로드하세요", type=["csv"])

    if uploaded_file is not None:
        df = load_data(uploaded_file)

        # 순서대로 배치: 데이터 탐색 -> 시각화 [cite: 191, 410, 742]
        show_data_exploration(df)
        st.divider()
        draw_bar_chart(df)
        st.divider()
        draw_scatter_plot(df)
    else:
        st.info("CSV 파일을 업로드하면 분석 기능이 활성화됩니다.")


if __name__ == "__main__":
    main()