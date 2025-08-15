import json

def analyze_log_file():
    """
    로그 파일을 읽고 분석하여 JSON 파일로 저장하는 메인 함수.
    """
    log_file_name = 'mission_computer_main.log'
    output_json_name = 'mission_computer_main.json'

    try:
        # mission_computer_main.log 파일을 읽고 전체 내용을 화면에 출력
        print(f'--- [1] 원본 로그 파일({log_file_name}) 내용 ---')
        with open(log_file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                print(line.strip())

        # 로그 내용을 콤마(,) 기준으로 분리하여 리스트(List) 객체로 전환
        log_list = []
        for line in lines:
            # 첫 번째 콤마를 기준으로 분리 (헤더 및 형식 안 맞는 줄 제외)
            if ',' in line:
                parts = line.strip().split(',', 1)
                # 타임스탬프 형식인지 간단히 확인 (YYYY-MM-DD HH:MM:SS)
                if len(parts[0]) == 19 and parts[0][4] == '-':
                    log_list.append(parts)

        # 변환된 리스트 객체를 화면에 출력
        print('\n--- [2] 리스트 객체로 변환된 내용 ---')
        print(log_list)

        # 리스트 객체를 시간 역순으로 정렬하여 출력
        log_list.sort(key=lambda x: x[0], reverse=True)
        print('\n--- [3] 시간 역순으로 정렬된 리스트 ---')
        print(log_list)

        # 정렬된 리스트를 사전(Dict) 객체의 리스트로 변환
        log_dicts = []
        for timestamp, message in log_list:
            log_dicts.append({'timestamp': timestamp, 'message': message})

        # 변환된 Dict 객체를 mission_computer_main.json 파일로 저장
        with open(output_json_name, 'w', encoding='utf-8') as json_file:
            json.dump(log_dicts, json_file, indent=4, ensure_ascii=False)

        print(f"\n✅ 성공: '{output_json_name}' 파일이 생성되었습니다.")

    # 예외 상황(파일 없음, 디코딩 오류 등) 처리
    except FileNotFoundError:
        print(f"\n🚨 오류: '{log_file_name}' 파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f'\n🚨 예상치 못한 오류가 발생했습니다: {e}')


if __name__ == '__main__':
    analyze_log_file()