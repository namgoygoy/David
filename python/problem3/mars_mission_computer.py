import random
import datetime

class DummySensor:
    """
    화성 기지 환경 데이터 생성을 위한 더미 센서 클래스입니다.
    """
    def __init__(self):
        """
        클래스가 인스턴스화될 때 env_values 딕셔너리를 초기화합니다.
        """
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }
        print('DummySensor has been initialized.')

    def set_env(self):
        """
        지정된 범위 내에서 랜덤 환경 값을 생성하여 env_values에 저장합니다.
        """
        self.env_values['mars_base_internal_temperature'] = random.randint(18, 30)
        self.env_values['mars_base_external_temperature'] = random.randint(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.randint(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.randint(500, 715)
        # 소수점 값을 위해 uniform 사용
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 4) 
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4.0, 7.0), 2)
        print('New sensor data has been set.')

    def get_env(self):
        """
        현재 저장된 env_values를 반환하고, 로그 파일에 기록합니다.
        """
        # --- 보너스 과제: 로그 남기기 ---
        now = datetime.datetime.now()
        # 'a' 모드는 파일이 없으면 생성하고, 있으면 내용을 덧붙입니다.
        with open('sensor_log.csv', 'a', encoding='utf-8') as f:
            # 헤더가 파일에 없는 경우 추가 (파일이 비어있을 때)
            import os
            if os.path.getsize('sensor_log.csv') == 0:
                header = '날짜와시간,' + ','.join(self.env_values.keys()) + '\n'
                f.write(header)
            
            # 현재 데이터 쓰기
            log_entry = f"{now.strftime('%Y-%m-%d %H:%M:%S')},{','.join(map(str, self.env_values.values()))}\n"
            f.write(log_entry)
            
        print('Sensor data has been logged.')
        return self.env_values

# --- 메인 실행 부분 ---
if __name__ == '__main__':
    # 1. DummySensor 클래스를 ds라는 이름으로 인스턴스화
    ds = DummySensor()

    # 2. set_env() 메소드 호출하여 랜덤 값 생성
    ds.set_env()

    # 3. get_env() 메소드 호출하여 값 확인 및 로그 저장
    current_environment = ds.get_env()

    # 4. 결과 출력
    print('\n--- Current Mars Base Environment ---')
    print(current_environment)
    print('------------------------------------')