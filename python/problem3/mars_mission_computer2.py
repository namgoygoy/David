import random
import datetime
import time
import json
from collections import deque
import platform  # 시스템 기본 정보
import psutil    # 시스템 상세 정보 및 부하 측정

# --- 문제 1: DummySensor 클래스 (변경 없음) ---
class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0, 'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0, 'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0, 'mars_base_internal_oxygen': 0
        }
    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = random.randint(18, 30)
        self.env_values['mars_base_external_temperature'] = random.randint(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.randint(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.randint(500, 715)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 4)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4.0, 7.0), 2)
    def get_env(self):
        now = datetime.datetime.now()
        with open('sensor_log.csv', 'a', encoding='utf-8') as f:
            import os
            if os.path.exists('sensor_log.csv') is False or os.path.getsize('sensor_log.csv') == 0:
                header = '날짜와시간,' + ','.join(self.env_values.keys()) + '\n'
                f.write(header)
            log_entry = f"{now.strftime('%Y-%m-%d %H:%M:%S')},{','.join(map(str, self.env_values.values()))}\n"
            f.write(log_entry)
        return self.env_values

# --- 문제 2, 3: MissionComputer 클래스 (기능 추가) ---
class MissionComputer:
    def __init__(self):
        self.env_values = {}
        self.ds = DummySensor()
        self.data_history = deque()
        self.last_avg_time = time.time()

    def get_sensor_data(self):
        # (이전 코드와 동일)
        print('Mission Computer system started...')
        print('Press Ctrl+C to stop.')
        try:
            while True:
                self.ds.set_env()
                self.env_values = self.ds.get_env()
                current_time = time.time()
                print('\n--- Current Environment Data ---')
                print(json.dumps(self.env_values, indent=4))
                self.data_history.append({'time': current_time, 'data': self.env_values.copy()})
                if current_time - self.last_avg_time >= 300:
                    self.calculate_and_print_average()
                    self.last_avg_time = current_time
                    while self.data_history and current_time - self.data_history[0]['time'] > 300:
                        self.data_history.popleft()
                time.sleep(5)
        except KeyboardInterrupt:
            print('\nSystem stopped....')
            
    def calculate_and_print_average(self):
        # (이전 코드와 동일)
        if not self.data_history: return
        sum_values = {key: 0 for key in self.env_values.keys()}
        count = len(self.data_history)
        for record in self.data_history:
            for key, value in record['data'].items():
                sum_values[key] += value
        avg_values = {key: round(value / count, 4) for key, value in sum_values.items()}
        print('\n--- 5-Minute Average Environment Data ---')
        print(json.dumps(avg_values, indent=4))

    # --- 문제 3: 신규 추가된 메소드 1 ---
    def get_mission_computer_info(self):
        """미션 컴퓨터의 시스템 정보를 가져와 JSON으로 출력합니다."""
        print('\n--- Mission Computer System Info ---')
        try:
            # 전체 정보 수집
            all_info = {
                'os_name': platform.system(),
                'os_version': platform.version(),
                'cpu_type': platform.processor(),
                'cpu_cores': psutil.cpu_count(logical=True),
                # 바이트(B) 단위를 기가바이트(GB)로 변환
                'memory_size_gb': round(psutil.virtual_memory().total / (1024**3), 2)
            }
            
            # --- 보너스 과제: setting.txt 파일로 출력 항목 제어 ---
            try:
                with open('setting.txt', 'r') as f:
                    # 파일에서 한 줄씩 읽어와 리스트로 만듦 (양 끝 공백 제거)
                    selected_keys = [line.strip() for line in f if line.strip()]
                # setting.txt에 명시된 키만으로 새로운 딕셔너리 생성
                output_info = {key: all_info[key] for key in selected_keys if key in all_info}
            except FileNotFoundError:
                # setting.txt 파일이 없으면 모든 정보 출력
                print("Info: 'setting.txt' not found. Displaying all system info.")
                output_info = all_info
            
            print(json.dumps(output_info, indent=4))

        except Exception as e:
            # 예외 처리
            print(f"Error getting system info: {e}")

    # --- 문제 3: 신규 추가된 메소드 2 ---
    def get_mission_computer_load(self):
        """미션 컴퓨터의 실시간 부하 정보를 가져와 JSON으로 출력합니다."""
        print('\n--- Mission Computer System Load ---')
        try:
            load_info = {
                # interval을 1로 주어 1초간의 CPU 사용량을 측정
                'cpu_usage_percent': psutil.cpu_percent(interval=1),
                'memory_usage_percent': psutil.virtual_memory().percent
            }
            print(json.dumps(load_info, indent=4))

        except Exception as e:
            # 예외 처리
            print(f"Error getting system load: {e}")

# --- 메인 실행 부분 (문제 3의 요구사항에 맞게 수정) ---
if __name__ == '__main__':
    # 1. MissionComputer 클래스를 runComputer 라는 이름으로 인스턴스화
    runComputer = MissionComputer()

    # 2. get_mission_computer_info(), get_mission_computer_load() 메소드 호출 확인
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()

    # 3. 이전 단계의 센서 데이터 수집 기능은 잠시 주석 처리
    # print("\nStarting sensor data collection...")
    # runComputer.get_sensor_data()