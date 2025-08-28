import random
import datetime
import time
import json
from collections import deque
import platform
import psutil
import threading      # 멀티쓰레딩 라이브러리
import multiprocessing # 멀티프로세싱 라이브러리
import sys

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
        # 로그 기능은 그대로 유지
        return self.env_values

# --- 문제 2, 3, 4: MissionComputer 클래스 (주기적 실행 및 중지 기능 추가) ---
class MissionComputer:
    def __init__(self, stop_event=None):
        """
        클래스 초기화 시, 외부에서 받은 stop_event를 멤버 변수로 저장합니다.
        이를 통해 여러 쓰레드/프로세스가 동일한 중지 신호를 공유할 수 있습니다.
        """
        self.env_values = {}
        self.ds = DummySensor()
        self.data_history = deque()
        self.last_avg_time = time.time()
        self.stop_event = stop_event

    def get_sensor_data(self):
        """5초마다 센서 데이터를 가져와 출력합니다."""
        print('[Sensor Thread/Process] Started.')
        while not self.stop_event.is_set():
            self.ds.set_env()
            self.env_values = self.ds.get_env()
            print('\n--- Current Environment Data ---', flush=True)
            print(json.dumps(self.env_values, indent=4), flush=True)
            # 5분 평균 계산 로직 (간소화하여 포함)
            current_time = time.time()
            if current_time - self.last_avg_time >= 300:
                 # 실제 프로젝트에서는 평균 계산 로직을 여기에 추가
                 self.last_avg_time = current_time
            time.sleep(5)
        print('[Sensor Thread/Process] Stopped.')

    def get_mission_computer_info(self):
        """20초마다 시스템 정보를 가져와 출력합니다."""
        print('[Info Thread/Process] Started.')
        while not self.stop_event.is_set():
            print('\n--- Mission Computer System Info ---', flush=True)
            try:
                info = {
                    'os_name': platform.system(), 'os_version': platform.version(),
                    'cpu_type': platform.processor(), 'cpu_cores': psutil.cpu_count(logical=True),
                    'memory_size_gb': round(psutil.virtual_memory().total / (1024**3), 2)
                }
                print(json.dumps(info, indent=4), flush=True)
            except Exception as e:
                print(f"Error getting system info: {e}", flush=True)
            time.sleep(20)
        print('[Info Thread/Process] Stopped.')

    def get_mission_computer_load(self):
        """20초마다 시스템 부하를 가져와 출력합니다."""
        print('[Load Thread/Process] Started.')
        while not self.stop_event.is_set():
            print('\n--- Mission Computer System Load ---', flush=True)
            try:
                load_info = {
                    'cpu_usage_percent': psutil.cpu_percent(interval=1),
                    'memory_usage_percent': psutil.virtual_memory().percent
                }
                print(json.dumps(load_info, indent=4), flush=True)
            except Exception as e:
                print(f"Error getting system load: {e}", flush=True)
            # info와 주기를 맞추되, 약간의 시간차를 두어 출력이 겹치지 않게 함
            time.sleep(19) 
        print('[Load Thread/Process] Stopped.')

# --- 메인 실행 부분 ---
if __name__ == '__main__':

    # --- 방법 1: 멀티쓰레드로 실행하기 ---
    def run_with_multithreading():
        print("--- Starting with Multi-threading ---")
        print("Press Enter to stop all threads.\n")
        
        stop_event = threading.Event()
        
        # 1. runComputer 인스턴스 하나 생성
        runComputer = MissionComputer(stop_event)
        
        # 2. 각 메소드를 타겟으로 하는 쓰레드 3개 생성
        thread1 = threading.Thread(target=runComputer.get_mission_computer_info)
        thread2 = threading.Thread(target=runComputer.get_mission_computer_load)
        thread3 = threading.Thread(target=runComputer.get_sensor_data)
        
        threads = [thread1, thread2, thread3]
        
        # 3. 모든 쓰레드 시작
        for t in threads:
            t.start()
            
        # 4. (보너스 과제) 사용자 입력을 기다려 중지 신호 보내기
        input() # 사용자가 Enter를 누를 때까지 여기서 대기
        print("Stopping signal received. Shutting down threads gracefully...")
        stop_event.set()
        
        # 5. 모든 쓰레드가 종료될 때까지 대기
        for t in threads:
            t.join()
        
        print("\nAll threads have been stopped. System shutdown.")

    # --- 방법 2: 멀티프로세스로 실행하기 ---
    def run_with_multiprocessing():
        print("--- Starting with Multi-processing ---")
        print("Press Enter to stop all processes.\n")
        
        stop_event = multiprocessing.Event()
        
        # 1. 3개의 별도 인스턴스 생성
        runComputer1 = MissionComputer(stop_event)
        runComputer2 = MissionComputer(stop_event)
        runComputer3 = MissionComputer(stop_event)
        
        # 2. 각 인스턴스의 메소드를 타겟으로 하는 프로세스 3개 생성
        process1 = multiprocessing.Process(target=runComputer1.get_mission_computer_info)
        process2 = multiprocessing.Process(target=runComputer2.get_mission_computer_load)
        process3 = multiprocessing.Process(target=runComputer3.get_sensor_data)
        
        processes = [process1, process2, process3]
        
        # 3. 모든 프로세스 시작
        for p in processes:
            p.start()
        
        # 4. (보너스 과제) 사용자 입력을 기다려 중지 신호 보내기
        input()
        print("Stopping signal received. Shutting down processes gracefully...")
        stop_event.set()

        # 5. 모든 프로세스가 종료될 때까지 대기
        for p in processes:
            p.join()
            
        print("\nAll processes have been stopped. System shutdown.")


    # --- 실행할 방법을 선택하세요 ---
    # run_with_multithreading()
    run_with_multiprocessing()