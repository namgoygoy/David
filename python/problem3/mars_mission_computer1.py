import random
import datetime
import time
import json
from collections import deque

# --- 문제 1에서 작성한 DummySensor 클래스 (수정 없음) ---
class DummySensor:
    """
    화성 기지 환경 데이터 생성을 위한 더미 센서 클래스입니다.
    """
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }
        # print('DummySensor has been initialized.') # 실행 시 출력이 많아져서 주석 처리

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = random.randint(18, 30)
        self.env_values['mars_base_external_temperature'] = random.randint(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.randint(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.randint(500, 715)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 4)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4.0, 7.0), 2)

    def get_env(self):
        # 로그 기능은 문제 1의 보너스 과제이므로 그대로 둡니다.
        now = datetime.datetime.now()
        with open('sensor_log.csv', 'a', encoding='utf-8') as f:
            import os
            if os.path.exists('sensor_log.csv') is False or os.path.getsize('sensor_log.csv') == 0:
                header = '날짜와시간,' + ','.join(self.env_values.keys()) + '\n'
                f.write(header)
            
            log_entry = f"{now.strftime('%Y-%m-%d %H:%M:%S')},{','.join(map(str, self.env_values.values()))}\n"
            f.write(log_entry)
            
        return self.env_values

# --- 문제 2: MissionComputer 클래스 ---
class MissionComputer:
    """
    센서 데이터를 주기적으로 수집하고 출력하는 미션 컴퓨터 클래스입니다.
    """
    def __init__(self):
        """
        MissionComputer를 초기화하고 DummySensor를 인스턴스화합니다.
        """
        self.env_values = {}
        self.ds = DummySensor()
        
        # 보너스 과제(5분 평균)를 위한 변수
        # 최근 5분(300초)의 데이터를 저장할 deque와 마지막 평균 계산 시간
        self.data_history = deque()
        self.last_avg_time = time.time()

    def get_sensor_data(self):
        """
        5초마다 센서 데이터를 가져와 JSON으로 출력하고, 5분마다 평균을 계산합니다.
        """
        print('Mission Computer system started...')
        print('Press Ctrl+C to stop.')
        
        try:
            while True:
                # 1. 센서 값 가져와서 env_values에 담기
                self.ds.set_env()
                self.env_values = self.ds.get_env()
                current_time = time.time()

                # 2. env_values를 json 형태로 화면에 출력
                print('\n--- Current Environment Data ---')
                # indent=4 옵션은 JSON을 예쁘게 들여쓰기 해줍니다.
                print(json.dumps(self.env_values, indent=4))
                
                # --- 보너스 과제 2: 5분 평균 값 출력 ---
                # 현재 시간과 센서 데이터를 기록에 추가
                self.data_history.append({'time': current_time, 'data': self.env_values.copy()})
                
                # 5분(300초)마다 평균 계산
                if current_time - self.last_avg_time >= 300:
                    self.calculate_and_print_average()
                    self.last_avg_time = current_time # 마지막 평균 계산 시간 갱신
                    # 오래된 데이터 정리 (메모리 관리)
                    while self.data_history and current_time - self.data_history[0]['time'] > 300:
                        self.data_history.popleft()

                # 3. 5초에 한번씩 반복
                time.sleep(5)
                
        except KeyboardInterrupt:
            # --- 보너스 과제 1: 특정 키(Ctrl+C) 입력 시 중지 ---
            print('\nSystem stopped....')
            
    def calculate_and_print_average(self):
        """지난 5분간의 데이터 평균을 계산하고 출력합니다."""
        if not self.data_history:
            return

        # 평균 계산을 위한 딕셔너리 초기화
        sum_values = {key: 0 for key in self.env_values.keys()}
        count = len(self.data_history)
        
        for record in self.data_history:
            for key, value in record['data'].items():
                sum_values[key] += value
        
        avg_values = {key: round(value / count, 4) for key, value in sum_values.items()}
        
        print('\n--- 5-Minute Average Environment Data ---')
        print(json.dumps(avg_values, indent=4))


# --- 메인 실행 부분 ---
if __name__ == '__main__':
    # 1. MissionComputer 클래스를 RunComputer 라는 이름으로 인스턴스화
    RunComputer = MissionComputer()

    # 2. get_sensor_data 메소드 호출
    RunComputer.get_sensor_data()