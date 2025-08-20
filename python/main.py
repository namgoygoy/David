import json
import os

# --- 보너스 기능 함수 ---

def filter_and_save_critical_logs(logs, base_dir):
    """
    로그 목록에서 위험 키워드가 포함된 로그를 필터링하여 별도 파일에 저장합니다.
    """
    critical_keywords = ['폭발', '누출', '고온', 'Oxygen']
    critical_logs = []
    
    for log in logs:
        message = log['message']
        # keyword에 해당하는 단어 판별해서 추가
        if any(keyword in message for keyword in critical_keywords):
            critical_logs.append(log)
            
    if critical_logs:
        # 해당하는 keyword 확인하여 txt 파일로 저장
        print(f"\n--- [보너스 1] 위험 키워드 감지! ({len(critical_logs)}건) ---")
        output_filename = os.path.join(base_dir, 'critical_logs.txt')
        with open(output_filename, 'w', encoding='utf-8') as file:
            for log in critical_logs:
                file.write(f"{log['timestamp']} | {log['message']}\n")
        print(f"✅ '{output_filename}' 파일에 위험 로그를 저장했습니다.")

def search_logs_from_json(json_path):
    """
    사용자로부터 검색어를 입력받아 JSON 파일에서 해당 로그를 찾아 출력합니다.
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            logs = json.load(file)

        search_term = input("\n--- [보너스 2] 로그 검색어를 입력하세요 (종료하려면 엔터): ")
        if not search_term:
            print("검색을 종료합니다.")
            return
        # 메인함수에서 생성한 json 파일을 읽어와 해당하는 로그가 있는지 확인 

        print(f"\n🔍 '{search_term}' 검색 결과:")
        found_logs = 0
        for log in logs:
            if search_term.lower() in log['message'].lower():
                # 대소문자 구분없이 탐색하기 위하여 모두 소문자로 바꿈
                print(f"  - {log['timestamp']} | {log['message']}")
                found_logs += 1
                # 해당하는 로그를 찾아 출력
        
        if found_logs == 0:
            print("  검색된 로그가 없습니다.")

    except FileNotFoundError:
        print(f"🚨 '{os.path.basename(json_path)}' 파일이 없어 검색을 수행할 수 없습니다.")
    except Exception as e:
        print(f"🚨 검색 중 오류 발생: {e}")


# --- 메인 분석 함수 ---

def analyze_log_file():
    """
    로그 파일을 읽고 분석하여 JSON 파일로 저장하는 메인 함수.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_file_name = os.path.join(script_dir, 'mission_computer_main.log')
    output_json_name = os.path.join(script_dir, 'mission_computer_main.json')

    try:
        print(f'--- [1] 원본 로그 파일({os.path.basename(log_file_name)}) 내용 ---')
        with open(log_file_name, 'r', encoding='utf-8') as file:
            # with 구문, 작업 후 파일 자동으로 닫아 줌 
            lines = file.readlines()
            # 필요할 때마다 내용 전부를 가지고 오는 것보다 한 줄씩 가지고 오는 것이 효율 적이기 떄문 
            for line in lines:
                print(line.strip())

        log_list = []
        for line in lines:
            if ',' in line:
                parts = line.strip().split(',', 1)
                # 'YYYY-MM-DD HH:MM:SS' 형식을 필터링하기 위해서, 해당하는 것만 append함
                if len(parts[0]) == 19 and parts[0][4] == '-':
                    log_list.append(parts)
        print('\n--- [2] 리스트 객체로 변환된 내용 ---')
        print(log_list)

        # x는 ['2023-08-27 12:00:00', '...']을 의미 x[0]은 타임 스탬프 즉, 타임 스탬프를 기준으로 역순으로 정렬 
        log_list.sort(key=lambda x: x[0], reverse=True)
        print('\n--- [3] 시간 역순으로 정렬된 리스트 ---')
        print(log_list)

        log_dicts = []
        for timestamp, message in log_list:
            log_dicts.append({'timestamp': timestamp, 'message': message})
            # 딕셔너리 리스트로 전환
        with open(output_json_name, 'w', encoding='utf-8') as json_file:
            json.dump(log_dicts, json_file, indent=4, ensure_ascii=False)
            # json 파일로 저장 ,를 기준으로 4칸씩 들여쓰기 가독성 향상을 위함
        print(f"\n✅ 성공: '{os.path.basename(output_json_name)}' 파일이 생성되었습니다.")
        
        # --- 보너스 기능 실행 ---
        filter_and_save_critical_logs(log_dicts, script_dir)
        search_logs_from_json(output_json_name)

    except FileNotFoundError:
        print(f"\n🚨 오류: '{os.path.basename(log_file_name)}' 파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f'\n🚨 예상치 못한 오류가 발생했습니다: {e}')


if __name__ == '__main__':
    analyze_log_file()