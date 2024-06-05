'''
columns = ['수축기_mmHg', '혈당식전_mgdL', '라면', '음료수', '패스트푸드', '육류', '우유_유제품', '과일', '채소(김치제외)', '아침식사', '다이어트경험_답변1', '다이어트경험_답변2', '다이어트경험_답변3',
            '다이어트경험_답변4', '주3회이상운동', '하루수면량','자아신체상(체형)', 'BMI', '학년']

df5 = df.copy()

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
df1.describe()

#뒤에 생활습관에서 활용
df_diet = df1.copy()
'''