# 03. 대시보드 구현하기
# StreramIt으로 구현한 Data App 입니다.

### 3.1 공통 모듈 불러오기 및 설정
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu
import streamlit as st
from datetime import date
import os

st.cache_resource.clear()
sns.set_theme(style='whitegrid', font_scale=0.6)
sns.set_palette('Set2', n_colors=10)

font_path = '/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf' 

#plt.rc('font', family='NanumBarunGothic')
plt.rc('axes', unicode_minus=False)

# 디렉토리 내 파일 목록 읽기
file_list = os.listdir("/usr/share/fonts/truetype/")



font = {'fontsize':10, 'fontstyle':'italic', 'backgroundcolor':'white', 'color':'black', 'fontweight': 'bold'} # for plot title

### 3.2 분석할 데이터 읽어오기
df = pd.read_csv(fr"https://raw.githubusercontent.com/wooyeon83/AIBP_Team_Project/main/data/input/data.csv", encoding='utf-8', low_memory=False)
df.head()

### 3.3 웹페이지 타이틀 설정하기
st.set_page_config(page_title='Elementary Student Growth Analysis Dashboard', 
                   page_icon='👩‍👩‍👧‍👧', layout='wide')
st.title("👩‍👩‍👧‍👧 초등학생 성장발달 분석")
# 파일 목록 출력
print("디렉토리 내 파일 목록:")
for file in file_list:
    st.write(file)
### 3.4 새로고침 버튼 추가
if st.button('새로고침'):
    st.experimental_rerun()

#### 3.5 사이드바 꾸미기
# 날짜 조건 필터 생성
st.sidebar.header("날짜 조건")
# 현재 연도 가져오기
first_year = 2015
last_year = 2022
col1, col2 = st.sidebar.columns(2)
with col1:
    start_year = st.selectbox("시작 연도", list(range(first_year, last_year)), index=0)
with col2:
    end_year = st.selectbox("종료 연도", list(range(first_year+1, last_year+1)), index=last_year-first_year-1)

# 종료 연도가 시작 연도보다 이전일 경우 오류 메시지 표시
if start_year > end_year:
    st.error("오류: 종료 연도는 시작 연도 이후여야 합니다.")

df = df[(df['학년도'] >= start_year) & (df['학년도'] <= end_year)]


def first_page_draw():
    st.header('0. 데이터 소개')
    st.write('* 교육부_학생건강검사 표본조사')
    st.write('* 체계적이고 신뢰성 있는 학생건강지표를 생성하고자 표본학교를 대상으로 분석된 통계데이터입니다. 생성된 통계는 ‘통계법』제17조에 근거한 정부 지정통계(승인번호 112002호)입니다.')
    # 아이콘과 링크를 HTML로 생성
    link_icon_html = '''* 출처 : 공공데이터포털
    <a href="https://www.data.go.kr/data/15100360/fileData.do" target="_blank">
        <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAMAAABF0y+mAAAANlBMVEUAXqoAXqoAWKgAVKZSjcKyyeHD0uWMstZ0oczt9Pn////1+PvV5PFrnMqYvt0ATaQwd7cAXqp66WfTAAAAEnRSTlOS/////////////////////6e+bY7iAAAAo0lEQVR4AaXSRQKDQAxA0UbG/f6XbfBQl7+Dh4xdLvA0ZQ96i0inUCOysUfGMaBCH6Iqhcx0hypHGm3xc8XVnEQNKqwN1wg5x5gcKiTYoy6aOz5EwD799gkCWfkrPEa5M3/3CbIg/4QuRtvhCebnAyIZT/D4CFGu56/u6NoWsBELjAcmVZTEDjwX4NiykoMue0DYsRcV94l2FNbB0R/ndjy3cQWaWwzHLpuneAAAAABJRU5ErkJggg==" alt="link icon"/>
    </a>
    '''
    st.write('* 제공기관 : 교육부')  
    st.markdown(link_icon_html, unsafe_allow_html=True)

    st.header('1. Overview')
    col1, col2, col3, col4, col5 = st.columns([2, 1, 2, 2, 1])
    col1.metric(label = "총 데이터 건수", value = f'총 {df.shape[0]} 건')
    col2.metric(label = "총 컬럼수", value = f'총 {len(df.columns)}개')
    col3.metric(label = "데이터 범위", value = f"{df['학년도'].min()}년~{df['학년도'].max()}년")
    col4.metric(label = "데이터 대상", value = f"{df['학년'].min()}학년~{df['학년'].max()}학년")
    col5.metric(label = "대상 시도", value = f"총 {len(df['시도별'].unique())}개")

    st.header('2. 컬럼정보')
    file_contents = """
        | 순번 | 컬럼명 | 설명|
        |:---:|:-----:|---------------|
        | 01 | 학년도 |  건강검진 기준년도 |
        | 02 | 시도별 |  학교 시도 위치(서울, 부산, 대구, 인천, 광주, 대전, 울산, 세종, 경기, 강원, 충북, 충남, 전북, 전남, 경북, 경남, 제주)  |
        | 03 | 학교급 |  초 (초등학생만 분석 대상으로 정함) |
        | 04 | 학년  | 1~6학년 |
        | 05 | 생년월일  | YYYYMMDD |
        | 06 | 성별  | 남, 여 |
        | 07 | 키_cm  | 키_cm|
        | 08 | 몸무게_kg  | 몸무게_kg |
        | 09 | 건강검진일  | YYYYMMDD |
        | 10 | 근골격및 척추  | 정상,  척추측만, 검사안함, 기타,  요통, 척추전만, 어깨결림|
        | 11 | 시력_나안_좌 | 나안 시력(안경이나 렌즈 등 시력 교정 장치를 착용하지 않은 시력) 측정값(좌) |
        | 12 | 시력_나안_우 | 나안 시력(안경이나 렌즈 등 시력 교정 장치를 착용하지 않은 시력) 측정값(우) |
        | 13 | 시력_교정_좌 | 교정 시력 측정값(좌) |
        | 14 | 시력_교정_우 | 교정 시력 측정값(우) |
        | 15 | 안질환 | 결막염, 사시, 없음, 기타, 검사안함 |
        | 16 | 청력_좌 | 정상, 이상, 검사안함 |
        | 17 | 청력_우 | 정상, 이상, 검사안함 |
        | 18 | 비만여부 | 정상체중, 비만, 과체중, 저체중|
        | 19 | 귓병 | 외이도염, 중이염, 중이염및외이도염, 없음, 기타, 검사안함|
        | 20 | 콧병 | 비염, 코곁굴염, 기타, 없음, 검사안함 |
        | 21 | 목병 | 목부위림프절비대, 편도비대, 기타, 없음, 검사안함 |
        | 22 | 피부병 | 아토피성피부염, 전염성피부염, 기타, 없음, 검사안함 |
        | 23 | 요단백 | 양성(+4), 양성(+3), 양성(+2), 양성(+1), 약양성(+-), 음성, 검사안함|
        | 24 | 요잠혈 | 양성(+4), 양성(+3), 양성(+2), 양성(+1), 약양성(+-), 음성, 검사안함 |
        | 25 | 혈당식전_mgdL | 식전 혈당 측정값 |
        | 26 | 총콜레스테롤(mg_dl) | 총 콜레스테롤 측정값 |
        | 27 | AST(U_L) | 간세포효소(AST) 측정값 |
        | 28 | ALT(U_L) | 간세포효소(ALT) 측정값 |
        | 29 | 수축기_mmHg | 수축기 혈압 측정값(mmHg) |
        | 30 | 이완기 | 이완기 혈압 측정값(mmHg) |
        | 31 | 기타 | 소견 작성 |
        | 32 | 건강검진_종합소견 | 정상, 정상(경계), 정밀검사요함|
        | 33 | 충치치아_유무 | 유, 무, 검사안함 |
        | 34 | 충치치아_개수_상 | 충치치아 개수(윗니) | 
        | 35 | 충치치아_개수_하 | 충치치아 개수(아랫니) |
        | 36 | 충치발생위험치아_유무 | 유, 무, 검사안함| 
        | 37 | 충치발생위험치아_개수_상 | 충치발생위험 치아 개수(윗니) |
        | 38 | 충치발생위험치아_개수_하 | 충치발생위험 치아 개수(아랫니) |  
        | 39 | 결손치아(영구치아)_유무 | 유, 무, 검사안함 |
        | 40 | 결손치아(영구치아)__개수_상 | 결손치아(영구치 기준) 개수(윗니) |
        | 41 | 결손치아(영구치아)__개수_하 | 결손치아(영구치 기준) 개수(아랫니) |
        | 42 | 구내염및연조직질환 | 유, 무, 검사안함 |
        | 43 | 부정교합 |교정중, 요교정, 없음, 검사안함 |
        | 44 | 구강위생상태 | 우수, 보통, 개선요망, 검사안함 |
        | 45 | 그밖의치아상태 | 과잉치, 유치잔존, 기타, 해당없음, 검사안함 |
        | 46 | 치주질환(잇몸병)_유무 | 유, 무, 검사안함 |
        | 47 | 치주질환_종류 | 치석, 치은출혈/비대, 치주낭, 기타, 해당없음, 검사안함 |
        | 48 | 치아마모증 | 유, 무, 검사안함 |
        | 49 | 제3대구치(사랑니) | 이상, 정상, 검사안함 |
        | 50 | 구강검진_종합소견 | 정상, 정상(경계), 정밀검사요함 |
        | 51 | 구강검진일 | YYYYMMDD |
        | 52 | 라면 | 일주일 동안 라면을 먹는 횟수 ① 먹지 않음 ② 1-2번 ③ 3-5번 ④ 매일 먹음|
        | 53 | 음료수 | 일주일 동안 음료수를 먹는 횟수 ① 먹지 않음 ② 1-2번 ③ 3-5번 ④ 매일 먹음|
        | 54 | 패스트푸드 | 일주일 동안 패스트푸드 (햄버거, 피자, 튀김 등)를 먹는 횟수 ① 먹지 않음 ② 1-2번 ③ 3-5번 ④ 매일 먹음|
        | 55 | 육류 | 일주일 동안 육류(소, 돼지, 닭고기 등)를 먹는 횟수 ① 먹지 않음 ② 1-2번  ③ 3-5번 ④ 매일 먹음|
        | 56 | 우유_유제품 | 일주일 동안 우유, 유제품을 먹는 횟수 ① 먹지 않음 ② 1-2번 ③ 3-5번 ④ 매일 먹음|
        | 57 | 과일 | 일주일 동안 과일을 먹는 횟수 ① 먹지 않음 ② 1-2번 ③ 3-5번 ④ 매일 먹음|
        | 58 | 채소(김치제외) | 일주일 동안 채소(김치 제외)를 먹는 횟수 ① 먹지 않음  ② 1-2번 ③ 3-5번 ④ 매일 먹음|
        | 59 | 아침식사 | 아침식사습관 ① 거의 꼭 먹음 ② 대체로 먹음 ③ 대체로 안 먹음 ④ 거의 안 먹음|
        | 60 | 다이어트경험_답변1 | 다이어트 경험(있는 대로 고르시오) ① 아무것도 안 함  ② 식단을 조절 한다  ③ 약을 먹는다 ④ 운동으로 감량 한다|
        | 61 | 다이어트경험_답변2 | 위와 동일 |
        | 62 | 다이어트경험_답변3 | 위와 동일 |
        | 63 | 다이어트경험_답변4 | 위와 동일 |
        | 64 | 주3회이상운동 | 일주일에 세 번 이상 숨이 차거나 땀이 날 정도의 운동 여부 ①예 ②아니오|
        | 65 | 하루수면량 | 평소에 하루 수면 시간 ① 6시간 이내 ② 6-7시간  ③ 7-8시간  ④ 8시간 이상|
        | 66 | 자아신체상(체형) | 자신의 체형에 대한 생각 ① 매우 마른 편이다  ② 약간 마른 편이다 ③ 보통이다 ④ 약간 살이 찐 편이다   ⑤ 매우 살이 찐 편이다|
        | 67 | 손씻기 | 밥을 먹기 전이나 밖에서 놀다 돌아와서 비누로 손을 씻는다. ①예 ②아니오 |
        | 68 | 양치질 | 하루에 두 번 이상 이를 닦는다. ①예 ②아니오|
        | 69 | 안전벨트착용 | 자동차를 탈 때 안전벨트를 맨다 ①예 ②아니오|
        | 70 | 안전장비착용 | 인라인스케이트･롤러블레이드･스케이트보드 또는 자전거 등을 탈 때 헬멧을 쓰고 보호대를 착용한다. ①예 ②아니오|
        | 71 | 하루TV시청2시간이상 | 텔레비전을 하루에 2시간 이상 본다. ①예 ②아니오|
        | 72 | 2시간이상게임 | 인터넷이나 게임을 하루에 2시간 이상 한다. ①예 ②아니오|
        | 73 | 괴롭힘따돌림 | 지난 1년 동안 친구들에게 괴롭힘이나 따돌림을 당한 적이 있다. ①예 ②아니오|
        | 74 | 현금갈취 | 돈을 빼앗는 친구가 있다. ①예 ②아니오|
        | 75 | 신체접촉 | 내 몸을 자주 만지는 사람이 있다. ①예 ②아니오|
        | 76 | 가출생각 | 집을 나가고 싶을 때가 자주 있다. ①예 ②아니오|
        | 77 | 가족지지 | 우리 가족은 나의 이야기를 잘 들어주고 나의 감정을 존중해 준다. ①예 ②아니오|
        | 78 | 체벌경험 | 자주 매를 맞는 편이다. ①예 ②아니오|
        | 79 | 상담요청 | 고민이나 괴로운 일로 상담을 받고 싶다. ①예 ②아니오|
        | 80 | 가족흡연 | 같이 사는 사람 중에 담배를 피우는 사람이 있다. ①예 ②아니오|
        | 81 | 가족음주 | 같이 사는 사람 중에 술을 너무 많이 마셔서 걱정되는 사람이 있다. ①예 ②아니오|
        | 82 | 무기력감 | 모든 것이 귀찮고 희망이 없는 것처럼 느껴진다. ①예 ②아니오|
        | 83 | 수업태도교정 | 공부시간에 선생님께 자주 혼난다. ①예 ②아니오|
        | 84 | 과잉행동 | [부모님란] 귀하의 자녀가 만 5세 이후 가만히 앉아 있지 못하고 항상 뛰어다니거나 말을 많이 합니까?(1학년만) ①예 ②아니오|
        | 85 | 주의력산만 |[부모님란] 귀하의 자녀는 주의력이 없고 주의가 산만합니까?(1학년만) ①예 ②아니오|
        | 86 | 상담희망 | 가정 및 학교생활 문제로 선생님의 상담이 필요하다. ①예 ②아니오|
    """
    st.markdown(file_contents)

def calculate_bmi(weight, height_cm):
    """
    체중과 키를 받아서 BMI를 계산하는 함수.

    :param weight: 체중 (kg)
    :param height_cm: 키 (cm)
    :return: BMI 지수
    """
    height_m = height_cm / 100  # cm를 m로 변환
    bmi = weight / (height_m ** 2)
    return bmi

def add_bmi_column(df5):
    #df5['BMI'] = df5['몸무게_kg']/df5['키_cm'] * 100
    df5['BMI'] = calculate_bmi(df5['몸무게_kg'], df5['키_cm'])

    # 몸무게 대비 비율로 Lower, Normer, Upper 등급 분류하기
    Q1 = df5['BMI'].quantile(0.25)
    Q3 = df5['BMI'].quantile(0.75)

    # IQR 계산
    IQR = Q3 - Q1

    upper_fence = Q3 + 1.5 * IQR
    lower_fence = Q1 - 1.5 * IQR

    print('IQR:' , IQR, 'Q3:', Q3, 'Q1:', Q1, 'Upper기준:', upper_fence,'초과 ', 'Lower기준:', lower_fence, '미만 ')

    df5.loc[df5['BMI'] < Q1, 'BMI등급'] = 'Lower'
    df5.loc[df5['BMI'] > Q3, 'BMI등급'] = 'Upper'
    df5['BMI등급'] = df5['BMI등급'].fillna('Normal')
    df5[['학년도', '학년', '몸무게_kg', '키_cm', 'BMI', 'BMI등급']].head()
    return upper_fence, lower_fence
    

def second_page_draw():
    st.header('1. 키 성장 변화')

    df1 = df.groupby(['학년도', '학년']).agg({'키_cm' : 'mean'}).sort_values(['학년도', '학년']).reset_index()
    df1.head()  
    years = [ i  for i in np.arange(start_year, end_year+1) ]
    if start_year <= 2020 and end_year >= 2020:
        years.remove(2020)

    heights_by_grade = {
        '1학년': df1[df1['학년'] == 1]['키_cm'].to_list(),
        '2학년': df1[df1['학년'] == 2]['키_cm'].to_list(),
        '3학년': df1[df1['학년'] == 3]['키_cm'].to_list(),
        '4학년': df1[df1['학년'] == 4]['키_cm'].to_list(),
        '5학년': df1[df1['학년'] == 5]['키_cm'].to_list(),
        '6학년': df1[df1['학년'] == 6]['키_cm'].to_list(),
    }
    col1, col2, col3 = st.columns([1, 2, 1])
    # 다중 라인 그래프 그리기
    fig = plt.figure(figsize=(6, 3))

    for grade, heights in heights_by_grade.items():
        plt.plot(years, heights, label=grade)

    plt.title('학년별 평균 키 변화추이', fontdict=font, pad=10)
    plt.xlabel('Year')
    plt.ylabel('평균 키 (cm)')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(True)
    plt.xticks(years)
    col2.pyplot(fig)

    st.header('2. 몸무게 성장 변화')
    col1, col2 = st.columns([1,8])

    grade_arr = np.append('전체', df['학년'].unique().astype(str))
    grade_frame = col1.selectbox("학년", grade_arr)

    df1 = df.groupby(['학년도', '학년']).agg({'몸무게_kg' : 'mean'}).sort_values(['학년도', '학년']).reset_index()
    df1.head()
    if grade_frame != '전체':
        df2 = df[df['학년']==int(grade_frame)].groupby(['학년도', '성별']).agg({'몸무게_kg' : 'mean'}).sort_values(['학년도',  '성별']).reset_index()
    else :
        df2 = df.groupby(['학년도', '성별']).agg({'몸무게_kg' : 'mean'}).sort_values(['학년도',  '성별']).reset_index()
    df2.head()

    heights_by_grade = {
        '1학년': df1[df1['학년'] == 1]['몸무게_kg'].to_list(),
        '2학년': df1[df1['학년'] == 2]['몸무게_kg'].to_list(),
        '3학년': df1[df1['학년'] == 3]['몸무게_kg'].to_list(),
        '4학년': df1[df1['학년'] == 4]['몸무게_kg'].to_list(),
        '5학년': df1[df1['학년'] == 5]['몸무게_kg'].to_list(),
        '6학년': df1[df1['학년'] == 6]['몸무게_kg'].to_list(),
    }

    col1, col2, col3 = st.columns([1, 4, 1])
    fig, ax = plt.subplots(1,2,figsize=(10,3))

    for grade, heights in heights_by_grade.items():
        ax[0].plot(years, heights, label=grade)

    ax[0].set_title('학년별 평균 몸무게 변화', fontdict=font, pad=40)
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('평균 몸무게 (kg)')
    ax[0].legend(loc='upper center', bbox_to_anchor=(0.5, 1.25), ncol=3)
    ax[0].grid(True)
    ax[0].set_xticks(years)

    male_weights = df2[df2['성별'] == '남']['몸무게_kg'].to_list()
    female_weights = df2[df2['성별'] == '여']['몸무게_kg'].to_list()

    label_name = ''
    if grade_frame != '전체':
        label_name = '('+grade_frame+'학년)'
    ax[1].plot(years, male_weights, marker='o', label=f'남학생{label_name}')
    ax[1].plot(years, female_weights, marker='o', label=f"여학생{label_name}")

    ax[1].set_title('연간 성별 평균 몸무게 변화', fontdict=font, pad=40)
    ax[1].set_xlabel('연도')
    ax[1].set_ylabel('평균 몸무게 (kg)')
    ax[1].legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=2)
    ax[1].grid(True)
    ax[1].set_xticks(years)  # x축 눈금을 연도로 설정
    fig.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.2, wspace=0.4)
    col2.pyplot(fig)

    st.header('3. BMI 변화')
    st.markdown("""
            * BMI 변수 생성
                * BMI = 체중(kg) / (키(m))^2
            * BMI 등급 변수 생성
                * Upper : 사분위수 Q3 초과
                * Lower : 사분위수 Q1 미만
                * Normal : 사분위수 Q1 ~ Q3 범위
            """)
    col1, col2, col3 = st.columns([1, 4, 1])

    fig, ax = plt.subplots(1,2,figsize=(10,3))

    df5 = df.copy()
    upper_fence, lower_fence = add_bmi_column(df5)
    
    ax[0].set_title('연도별 초등학생 BMI 분포', fontdict=font, pad=15)
    df1_filtered = df5[(df5['BMI'] > lower_fence+5) & (df5['BMI'] < upper_fence-5)] # 이상치 없이 box 플롯그리기
    sns.boxplot(y='BMI', x='학년도', data=df1_filtered, ax = ax[0]);

    df2 = df5.groupby(['학년도', 'BMI등급'])['학년'].count().reset_index().rename(columns={'학년':'학생수'})
    df1_sub = df5.groupby('학년도')['학년'].count().reset_index().rename(columns={'학년':'전체학생수'})
    df2 = df2.merge(df1_sub, on='학년도')
    df2['비율'] = df2['학생수']/df2['전체학생수']
    df2.head()

    sns.barplot(x='학년도', y='비율', hue='BMI등급', data=df2, ax=ax[1])
    ax[1].set_title('연도별 BMI 등급별 비율' , fontdict=font, pad=15)
    ax[1].set_xlabel('연도')
    ax[1].set_ylabel('비율')
    ax[1].legend(title='BMI 등급', loc='upper left', bbox_to_anchor=(1, 1))
    ax[1].grid(True, axis='y')  # y 축에 그리드 추가
    fig.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.2, wspace=0.4)
    col2.pyplot(fig)

    st.header('4. BMI지수와 생활습관간의 상관관계')
    df2 = df5[['BMI등급', '라면', '음료수','패스트푸드', '육류', '우유_유제품', '과일', 
           '채소(김치제외)', '아침식사', '주3회이상운동', '하루수면량', '하루TV시청2시간이상',
            '2시간이상게임']].copy()
    mapping = {'Lower':1, 'Normal':2, 'Upper':3}
    df2.loc[:, 'BMI등급'] = df2['BMI등급'].map(mapping).astype(int)
    # 아침식사 ① 거의 꼭 먹음 ② 대체로 먹음 ③ 대체로 안 먹음 ④ 거의 안 먹음
    mapping = {1 : 4, 2 : 3, 3 : 2, 4: 1}
    df2.loc[:, '아침식사'] = df2['아침식사'].map(mapping)
    # 주3회이상운동 ①예 ②아니오
    df2.loc[(df2['주3회이상운동'] != 1) & (df2['주3회이상운동'] != 2), '주3회이상운동'] = None
    mapping = {1 : 2, 2 : 1}
    df2.loc[:, '주3회이상운동'] = df2['주3회이상운동'].map(mapping)
    # 하루TV시청2시간이상 ①예 ②아니오
    df2.loc[(df2['하루TV시청2시간이상'] != 1) & (df2['하루TV시청2시간이상'] != 2), '하루TV시청2시간이상'] = None
    mapping = {1 : 2, 2 : 1}
    df2.loc[:, '하루TV시청2시간이상'] = df2['하루TV시청2시간이상'].map(mapping)
    # 2시간이상게임 ①예 ②아니오
    mapping = {1 : 2, 2 : 1}
    df2.loc[:, '2시간이상게임'] = df2['2시간이상게임'].map(mapping)

    col1, col2, col3 = st.columns([1, 2, 1])
    fig = plt.figure(figsize=(12, 5))
    sns.heatmap(round(df2.corr(),3), cmap='Reds', annot=True)
    plt.title('BMI 상관관계', fontdict=font, pad=15)
    col2.pyplot(fig)

    st.header('5. 시력/청력 건강')
    df1 = df[(df['시력_교정_좌'].notnull()) | (df['시력_교정_우'].notnull()) | (df['시력_나안_우'].notnull()) | (df['시력_나안_좌'].notnull())][['학년도', '학년', '시력_교정_좌', '시력_교정_우', '시력_나안_좌', '시력_나안_우','라면', '음료수','패스트푸드', '육류', '우유_유제품', '과일', 
           '채소(김치제외)', '아침식사',  '주3회이상운동', '하루수면량', '하루TV시청2시간이상',
            '2시간이상게임']].copy()

    df1['시력저하유무'] = (df['시력_교정_좌'].notnull()) | (df['시력_교정_우'].notnull()) |  (df['시력_나안_우'] <= 0.5) |   (df['시력_나안_좌'] <= 0.5)

    df2 = df.copy()
    df2 = df[(df['청력_좌'].notnull()) | (df['청력_우'].notnull()) | (df['청력_좌'] != '검사안함') | (df['청력_우'] != '검사안함')][['학년도', '학년', '청력_좌', '청력_우']]

    df2['청력정상유무'] = (df['청력_좌'] =='이상') | (df['청력_우'] == '이상')

    col1, col2, col3 = st.columns([2, 4, 2])
    fig, ax = plt.subplots(1,2,figsize=(6,3))

    # count of col (pie chart)
    slices = df1['시력저하유무'].value_counts().values
    activities =['시력정상','시력저하']
    ax[0].pie(slices, labels=activities, shadow=True, autopct='%1.1f%%')
    ax[0].set_title('시력건강', fontdict=font, pad=15)

    slices1 = df2['청력정상유무'].value_counts().values
    activities1 =['청력정상','청력이상']
    ax[1].pie(slices1, labels=activities1, shadow=True, autopct='%1.1f%%')
    ax[1].set_title('청력건강', fontdict=font, pad=15)
    fig.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.2, wspace=0.4)
    col2.pyplot(fig)

    st.header('6. 시력건강과 생활습관과의 상관관계')

    df2 = df1[['시력저하유무', '육류', '우유_유제품', '과일', '채소(김치제외)', '아침식사',  
           '주3회이상운동', '하루수면량', '하루TV시청2시간이상', '2시간이상게임']].copy()
    # 아침식사 ① 거의 꼭 먹음 ② 대체로 먹음 ③ 대체로 안 먹음 ④ 거의 안 먹음
    mapping = {1 : 4, 2 : 3, 3 : 2, 4: 1}
    df2.loc[:, '아침식사'] = df2['아침식사'].map(mapping)
    # 주3회이상운동 ①예 ②아니오
    df2.loc[(df2['주3회이상운동'] != 1) & (df2['주3회이상운동'] != 2), '주3회이상운동'] = None
    mapping = {1 : 2, 2 : 1}
    df2.loc[:, '주3회이상운동'] = df2['주3회이상운동'].map(mapping)
    # 하루TV시청2시간이상 ①예 ②아니오
    df2.loc[(df2['하루TV시청2시간이상'] != 1) & (df2['하루TV시청2시간이상'] != 2), '하루TV시청2시간이상'] = None
    mapping = {1 : 2, 2 : 1}
    df2.loc[:, '하루TV시청2시간이상'] = df2['하루TV시청2시간이상'].map(mapping)
    # 2시간이상게임 ①예 ②아니오
    mapping = {1 : 2, 2 : 1}
    df2.loc[:, '2시간이상게임'] = df2['2시간이상게임'].map(mapping)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    fig = plt.figure(figsize=(12, 5))
    sns.heatmap(round(df2.corr(),3), cmap='Reds', annot=True)
    plt.title('시력건강과의 상관관계', fontdict=font, pad=15)
    col2.pyplot(fig)

    st.header('7. 치아건강')
    df1 = df[df['충치치아_유무'].isin (['무', '유']) ].groupby(['학년도'])['충치치아_유무'].count().reset_index().rename(columns={'충치치아_유무':'충치유병전체학생수'})
    df2 = df[df['충치치아_유무'].isin (['무', '유']) ].groupby(['학년도', '충치치아_유무'])['학년'].count().reset_index().rename(columns={'학년':'구강검진학생수'})
    df2 = df2.merge(df1, on='학년도')
    df2['비율'] = df2['구강검진학생수']/df2['충치유병전체학생수']

    df3 = df[df['구강위생상태'].isin (['보통', '우수', '개선요망']) ].groupby(['학년도'])['구강위생상태'].count().reset_index().rename(columns={'구강위생상태':'구강검진전체학생수'})
    df4 = df[df['구강위생상태'].isin (['보통', '우수', '개선요망']) ].groupby(['학년도', '구강위생상태'])['학년'].count().reset_index().rename(columns={'학년':'구강검진학생수'})
    df4 = df4.merge(df3, on='학년도')
    df4['비율'] = df4['구강검진학생수']/df4['구강검진전체학생수']

    col1, col2, col3 = st.columns([1, 2, 1])
    fig, ax = plt.subplots(1,2,figsize=(10,3))

    rates = df2[df2['충치치아_유무'] == '유']['비율'].to_list()

    ax[0].plot(years, rates, marker='o', label='충치유병비율')


    ax[0].set_title('연간 충치유병비율 변화', fontdict=font, pad=40)
    ax[0].set_xlabel('연도')
    ax[0].set_ylabel('충치유병비율')
    ax[0].legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=2)
    ax[0].grid(True)
    ax[0].set_xticks(years)  # x축 눈금을 연도로 설정
    fig.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.2, wspace=0.4)

    rates = df4[df4['구강위생상태'] == '개선요망']['비율'].to_list()
    ax[1].plot(years, rates, marker='o', label='개선요망')
    rates1 = df4[df4['구강위생상태'] == '보통']['비율'].to_list()
    ax[1].plot(years, rates1, marker='o', label='보통')
    rates2 = df4[df4['구강위생상태'] == '우수']['비율'].to_list()
    ax[1].plot(years, rates2, marker='o', label='우수')


    ax[1].set_title('연간 구강위생상태 변화', fontdict=font, pad=40)
    ax[1].set_xlabel('연도')
    ax[1].set_ylabel('구강위생상태')
    ax[1].legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3)
    ax[1].grid(True)
    ax[1].set_xticks(years)  # x축 눈금을 연도로 설정
    fig.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.2, wspace=0.4)
    col2.pyplot(fig)

def third_page_draw():
    st.write("* [참고] 표본에서 건강검진은 초등학교 4학년 학생들에 대한 데이터만 조사함")
    st.markdown("""
            * 혈당 기준 판정
                * 공복 혈당 정상 범위는 다음과 같다.
                * 정상 수치: 70-100 mg/dL (3.9-5.6 mmol/L)
                * 전당뇨 (Prediabetes): 100-125 mg/dL (5.6-6.9 mmol/L)
                * 당뇨병 (Diabetes): 126 mg/dL 이상 (7.0 mmol/L 이상)
            * 총 콜레스테롤 기준 판정
                * 정상 수치: 170 mg/dL 미만
                * 경계 수치 (Borderline high): 170-199 mg/dL
                * 높은 수치 (High): 200 mg/dL 이상
            * 혈압 기준 판정
                * 정상 수치 : 성별, 연령별, 신장대비 90 백분위수 미만
                * 정상 경계 : 성별, 연령별, 신장대비 90~95 백분위수 
                    * 단 90백분위 미만이라도 130/80 mmHg 이상인 경우 포함
                * 정밀검사 요함 : 95백분위수 초과
            * BMI 기준 판정
                * BMI < 18.5: 저체중
                * 18.5 <= BMI < 25: 정상
                * 25 <= BMI < 30: 과체중
                * BMI >= 30: 비만
            """)

    years = [ i  for i in np.arange(start_year, end_year+1) ]
    if start_year <= 2020 and end_year >= 2020:
        years.remove(2020)

    columns = ['학년도','학년', '혈당식전_mgdL', '총콜레스테롤(mg_dl)', '수축기_mmHg', '이완기']
    df1 = df[columns].copy()
 
    st.header('1. 혈당/혈압/콜레스테롤 수치 변화')

    col1, col2, col3 = st.columns([1, 2, 1])
    fig , ax= plt.subplots(2,2, figsize=(10,6))
    i=0
    j=0
    for col in columns : 
        if col not in (['학년도', '학년']):
            df2 = df1[df1[col].isna() == False]
            df2 = df2.groupby('학년도').agg({col : 'median'}).reset_index()

            mgdls = df2[col].to_list()
            
            col_text = col.replace('_mgdL', '(mgdL)').replace('_mmHg','(mmHg)').replace('이완기', '이완기(mmHg)')
            ax[i][j].plot(years, mgdls, marker='o', label=col_text)

        
            ax[i][j].set_title(f'연간 {col_text} 변화', fontdict=font, pad=40)
            ax[i][j].set_xlabel('연도')
            ax[i][j].set_ylabel(col_text)
            ax[i][j].legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=2)
            ax[i][j].grid(True)
            ax[i][j].set_xticks(years)  # x축 눈금을 연도로 설정
            j = j+1
            if j==2:
                j=0
                i = i+1

    fig.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.2, wspace=0.4)
    plt.tight_layout()
    col2.pyplot(fig)

    st.header('2. 혈압 및 혈당과 생활습관과의 상관관계')
    pd.set_option('mode.chained_assignment',  None)
    columns = ['수축기_mmHg', '혈당식전_mgdL',  '라면', '음료수', '패스트푸드', '육류', '우유_유제품', '과일', '채소(김치제외)', '아침식사', '다이어트경험_답변1', '다이어트경험_답변2', '다이어트경험_답변3',
                '다이어트경험_답변4', '주3회이상운동', '하루수면량','자아신체상(체형)', 'BMI']
    
    df5 = df.copy()
    upper_fence, lower_fence = add_bmi_column(df5)
    
    df1 = df5[columns].copy()
    # 아침식사 | 아침식사습관 ① 거의 꼭 먹음 ② 대체로 먹음 ③ 대체로 안 먹음 ④ 거의 안 먹음|
    mapping = {1:4, 2:3, 3:2, 4:1}
    df1.loc[:, '아침식사'] = df1['아침식사'].map(mapping)
    # 다이어트경험_답변1 | 다이어트 경험(있는 대로 고르시오) ① 아무것도 안 함  ② 식단을 조절 한다  ③ 약을 먹는다 ④ 운동으로 감량 한다|
    df1.loc[:, '다이어트경험유무'] = df1[df1['다이어트경험_답변1'] != 1]['다이어트경험_답변1']
    df1['다이어트경험유무'] = df1['다이어트경험유무'].fillna(df1[df1['다이어트경험_답변2'] != 1]['다이어트경험_답변2'])
    mapping = {3:2}
    df1['다이어트경험유무'] = df1['다이어트경험유무'].fillna(df1[df1['다이어트경험_답변3'] != 1]['다이어트경험_답변3'].map(mapping))
    mapping = {4:2}
    df1['다이어트경험유무'] = df1['다이어트경험유무'].fillna(df1[df1['다이어트경험_답변4'] != 1]['다이어트경험_답변4'].map(mapping))
    df1['다이어트경험유무'] = df1['다이어트경험유무'].fillna(1)
    df1 = df1.drop(columns=['다이어트경험_답변1', '다이어트경험_답변2', '다이어트경험_답변3', '다이어트경험_답변4'], axis = 0)
    # 주3회이상운동 ①예 ②아니오
    df1.loc[(df1['주3회이상운동'] != 1) & (df1['주3회이상운동'] != 2), '주3회이상운동'] = None
    mapping = {1 : 2, 2 : 1}
    df1.loc[:, '주3회이상운동'] = df1['주3회이상운동'].map(mapping)

    col1, col2, col3 = st.columns([1, 2, 1])
    fig = plt.figure(figsize=(12, 5))
    sns.heatmap(round(df1.corr(),3), cmap='Reds', annot=True)
    plt.title('혈압 및 혈당과의 상관관계', fontdict=font, pad=15)
    col2.pyplot(fig)

    st.header('3. 혈압과 BMI간의 상관관계')
    df2 = df1.copy()
    df2['BMI'] = df2['BMI'].clip(lower=10, upper=50)
    df2['수축기_mmHg'] = df2['수축기_mmHg'].clip(lower=50, upper=180)

    mapping = {1 : '매우 마른편', 2 : '약간 마른편', 3 : '보통', 4 : '약간 살찐편', 5 : '매우 살찐편'}
    df2.loc[:, '자아신체상(체형)'] = df2['자아신체상(체형)'].map(mapping)
    df2['자아신체상(체형)'] = df2['자아신체상(체형)'].fillna('보통')

    mapping = {1 : '무', 2 : '유'}
    df2.loc[:, '다이어트경험유무'] = df2['다이어트경험유무'].map(mapping)
    df2['다이어트경험유무'] = df2['다이어트경험유무'].fillna('무')

    col1, col2, col3 = st.columns([1, 2, 1])
    fig, ax = plt.subplots(1,2,figsize=(10,4))
    sns.scatterplot(data=df2, y='BMI', x='수축기_mmHg', hue='자아신체상(체형)', ax=ax[0], palette='Set2')
    ax[0].set_title(f'혈압 vs BMI (based on 자아신체상)', y=1.09, **font)

    sns.scatterplot(data=df2, y='BMI', x='수축기_mmHg', hue='다이어트경험유무', ax=ax[1], palette='Set2')
    ax[1].set_title(f'혈압 vs BMI (based on 다이어트)', y=1.09, **font)

    fig.tight_layout() 
    col2.pyplot(fig)


# https://icons.getbootstrap.com/ 에 아이콘 선택
# pip install streamlit-option-menu 설치 필요
with st.sidebar:
    choice = option_menu("목록", ["데이터 소개", "신체발달", "건강지수", "생활습관", "사회/환경"],
                         icons=['exclamation-square', 'bar-chart', 'bi bi-robot', 'clipboard-data', 'person-lines-fill'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
                            "container": {"padding": "4!important", "background-color": "#fafafa"},
                            "icon": {"color": "black", "font-size": "25px"},
                            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#fafafa"},
                            "nav-link-selected": {"background-color": "#08c7b4"},
                        }
            )
    
if choice == "데이터 소개":
    first_page_draw()
elif choice == "신체발달":
    second_page_draw()
elif choice == "건강지수":
    third_page_draw()
elif choice == "생활습관":
    st.title("Contact Page")
    st.write("Get in touch with me.")
elif choice == "사회/환경":
    st.title("Contact Page")
    st.write("Get in touch with me.")
