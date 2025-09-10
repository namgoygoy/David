import zipfile
# itertools는 이 모든 조합을 메모리에 저장하는 대신, "다음 조합 줘"라고 요청할 때마다 딱 한 개씩만 즉석에서 만들어서 줍니다
import itertools
import time
import multiprocessing
import os
# zlib는 '데이터를 압축(compress)하거나 압축을 푸는(decompress) 역할을 하는 라이브러리'입니다. zip을 다루는 라이브러리이므로 인정 
import zlib 

# --- 설정 변수 ---
ZIP_FILENAME = 'emergency_storage_key.zip'
PASSWORD_TXT_FILENAME = 'password.txt'
PASSWORD_LENGTH = 6
# 비밀번호에 사용될 문자셋 (소문자 + 숫자)
CHARSET = 'abcdefghijklmnopqrstuvwxyz0123456789'
def try_password(process_id, zip_filename, charset_chunk):
    """
    각 프로세스가 실행할 작업 함수.
    할당받은 문자셋(charset_chunk)으로 시작하는 비밀번호를 생성하고 검증합니다.
    """
    print(f"[Process-{process_id}] 작업 시작. 담당 시작 문자: {''.join(charset_chunk[:3])}...")
    
    try:
        zip_file = zipfile.ZipFile(zip_filename)
    except FileNotFoundError:
        print(f"[Process-{process_id}] 오류: '{zip_filename}' 파일을 찾을 수 없습니다.")
        return None, 0

    count = 0
    for start_char in charset_chunk:
        for remaining_chars_tuple in itertools.product(CHARSET, repeat=PASSWORD_LENGTH - 1):
            password = start_char + "".join(remaining_chars_tuple)
            
            try:
                zip_file.extractall(pwd=password.encode('utf-8'))
                
                print(f"\n[Process-{process_id}] ★★★ 비밀번호 찾음! ★★★")
                print(f"[Process-{process_id}] 시도 횟수: {count + 1}")
                return password, count + 1

            # --- 이 부분을 수정했습니다 ---
            except (RuntimeError, zipfile.BadZipFile, zlib.error):
                # 비밀번호가 틀렸을 때 발생하는 모든 예외를 처리합니다.
                count += 1
                if count % 100000 == 0:
                    print(f"[Process-{process_id}] {count}회 시도 중... (현재 비밀번호: {password})")
                    
    print(f"[Process-{process_id}] 담당 구역 탐색 완료. 암호를 찾지 못했습니다.")
    return None, count

def unlock_zip():
    """
    멀티프로세싱을 사용하여 ZIP 파일의 암호를 푸는 메인 함수
    """
    start_time = time.time()
    print(f"--- 비밀번호 찾기 시작 ---")
    print(f"시작 시간: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"대상 파일: {ZIP_FILENAME}")
    
    # 가상으로 zip 파일 생성 (실제 환경에서는 이 부분이 필요 없습니다)
    if not os.path.exists(ZIP_FILENAME):
        print(f"경고: '{ZIP_FILENAME}' 파일이 없어 테스트용으로 생성합니다.")
        try:
            with zipfile.ZipFile(ZIP_FILENAME, 'w', zipfile.ZIP_DEFLATED) as zf:
                zf.writestr("secret_note.txt", b"This is a secret message.")
                zf.setpassword(b'pass01') 
        except Exception as e:
            print(f"테스트 파일 생성 중 오류 발생: {e}")
            return

    # --- 멀티프로세싱 설정 ---
    try:
        # 사용 가능한 CPU 코어 수 확인
        cpu_cores = multiprocessing.cpu_count()
        print(f"사용 가능한 CPU 코어: {cpu_cores}개")
    except NotImplementedError:
        cpu_cores = 1 # cpu_count()를 지원하지 않는 경우 1개로 설정
        print("CPU 코어 수를 확인할 수 없어 1개로 실행합니다.")

    # 각 프로세스에 작업을 분배
    # 예: CHARSET을 4개의 코어에 분배 -> [['a','e','i',...], ['b','f','j',...], ...]
    charset_chunks = [CHARSET[i::cpu_cores] for i in range(cpu_cores)]
    
    # 각 프로세스에 전달할 인자 리스트 생성
    args = [(i, ZIP_FILENAME, chunk) for i, chunk in enumerate(charset_chunks)]

    found_password = None
    total_attempts = 0

    # 프로세스 풀 생성 및 실행
    # with 구문을 사용하여 프로세스 풀을 안전하게 관리
    with multiprocessing.Pool(processes=cpu_cores) as pool:
        # starmap: 각 인자 튜플을 worker 함수에 전달하여 병렬 실행
        results = pool.starmap(try_password, args)
        
        for password, attempts in results:
            total_attempts += attempts
            if password:
                found_password = password
                # 비밀번호를 찾았으므로 다른 프로세스들이 더 이상 작업하지 않도록 종료
                pool.terminate()
                break

    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print("\n--- 비밀번호 찾기 종료 ---")
    if found_password:
        print(f"성공! 찾은 비밀번호: {found_password}")
        try:
            with open(PASSWORD_TXT_FILENAME, 'w') as f:
                f.write(found_password)
            print(f"비밀번호를 '{PASSWORD_TXT_FILENAME}' 파일에 저장했습니다.")
        except IOError as e:
            print(f"오류: 파일 '{PASSWORD_TXT_FILENAME}'에 쓰는 중 문제가 발생했습니다: {e}")
    else:
        print("실패: 모든 조합을 시도했지만 비밀번호를 찾지 못했습니다.")
        
    print(f"총 시도 횟수: {total_attempts:,}")
    print(f"총 소요 시간: {elapsed_time:.2f}초")

if __name__ == '__main__':
    multiprocessing.freeze_support()
    unlock_zip()