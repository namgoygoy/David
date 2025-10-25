import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform
import os

def set_korean_font():
    """ 맥이나 윈도우에서 한글 폰트 설정하는 함수 """
    system_name = platform.system()
    
    try:
        if system_name == 'Windows':
            plt.rc('font', family='Malgun Gothic')
        elif system_name == 'Darwin': # MacOS
            plt.rc('font', family='AppleGothic')
        elif system_name == 'Linux':
            plt.rc('font', family='NanumGothic')
        
        plt.rc('axes', unicode_minus=False) # 마이너스 부호
        print(f'한글 폰트 설정 완료 (OS: {system_name})')
    
    except Exception as e:
        print(f'폰트 설정 중 오류: {e}')

# 한글 폰트 설정 실행
set_korean_font()

# 이 스크립트(app.py)가 있는 폴더 기준으로 파일 경로 설정
script_dir = os.path.dirname(os.path.abspath(__file__))
train_file_path = os.path.join(script_dir, 'train.csv')
test_file_path = os.path.join(script_dir, 'test.csv')


# --- 2. 데이터 불러오기 및 병합 (문제 2, 3, 4) ---
    
try:
    # (문제 2) 파일 읽기
    train_df = pd.read_csv(train_file_path)
    test_df = pd.read_csv(test_file_path)
    print(f"'train.csv' 로드 성공: {train_df.shape[0]} 행")
    print(f"'test.csv' 로드 성공: {test_df.shape[0]} 행")

    # (문제 3) 두 파일 하나로 합치기
    all_df = pd.concat([train_df, test_df], ignore_index=True)
    
    # (문제 4) 전체 데이터 수량 파악
    print(f'병합된 전체 데이터 수량: {all_df.shape[0]} 행')

except FileNotFoundError:
    print(f"오류: 'train.csv' 또는 'test.csv' 파일을 찾을 수 없습니다.")
    print(f"'{script_dir}' 폴더에 파일이 있는지 확인해주세요.")
    exit() # 파일 없으면 프로그램 종료


# --- 3. Transported와 가장 관련 높은 항목 찾기 (문제 5) ---

# 상관관계 분석은 'Transported' 컬럼이 있는 train_df로 해야 함
# 원본 데이터를 건드리지 않기 위해 복사본 사용
analysis_df = train_df.copy()

analysis_df['Transported'] = analysis_df['Transported'].astype(float)
analysis_df['CryoSleep'] = analysis_df['CryoSleep'].map({True: 1.0, False: 0.0})
analysis_df['VIP'] = analysis_df['VIP'].map({True: 1.0, False: 0.0})    

# 숫자형 컬럼들 간의 상관관계 계산
corr_matrix = analysis_df.corr(numeric_only=True)

# 'Transported' 컬럼과 다른 컬럼들 간의 상관관계만 뽑아내기
transported_corr = corr_matrix['Transported'].abs().sort_values(ascending=False)

print('\n--- Transported와 상관관계가 높은 항목 ---')
print(transported_corr.head(6))

# 0번은 자기 자신(Transported)이므로 1번 인덱스가 가장 관련 높은 항목
top_feature = transported_corr.index[1]
print(f"\n[결론] 가장 관련성 높은 항목: '{top_feature}'")


# --- 4. 연령대별 Transported 여부 시각화 (문제 6) ---

print('\n--- 연령대별 Transported 여부 시각화 ---')

# 시각화를 위해 'Age'나 'Transported'에 빈 값(NaN)이 있는 행은 제외
plot_df = train_df.dropna(subset=['Age', 'Transported']).copy()

bins = [0, 9, 19, 29, 39, 49, 59, 69, float('inf')]
labels = ['10대 미만', '10대', '20대', '30대', '40대', '50대', '60대', '70대 이상']

# true (19, 29)처럼 오른쪽 숫자(29)가 포함
plot_df['age_group'] = pd.cut(
    plot_df['Age'], 
    bins=bins, 
    labels=labels, 
    right=True
)

# 그래프 그리기
plt.figure(figsize=(12, 7)) 

sns.countplot(
    data=plot_df, 
    x='age_group', 
    hue='Transported', 
    order=labels # x축 순서 고정
)

plt.title('연령대별 Transported 여부', fontsize=16)
plt.xlabel('연령대')
plt.ylabel('승객 수')
plt.legend(title='Transported 여부 (True: 전송됨)')

# PC에서 그래프 창 띄우기
try:
    print("그래프를 화면에 출력합니다...")
    plt.show()
except Exception as e:
    print(f'그래프 출력 중 오류: {e}')