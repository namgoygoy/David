import zipfile
import itertools
# itertools의 핵심 철학은 메모리를 효율적으로 사용하는 것입니다. 모든 결과를 미리 만들어두는 게 아니라, 필요할 때마다 하나씩 꺼내 쓸 수 있는 '반복기(iterator)'
import time
import multiprocessing
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
        # product 함수 5개의 다이얼을 첫 번째 조합인 aaaaa부터 마지막 조합인 99999까지 순서대로 하나씩 돌려가며 모든 가능한 조합을 만들어 낸다.
        for remaining_chars_tuple in itertools.product(CHARSET, repeat=PASSWORD_LENGTH - 1):
            # start_char에서 하나씩 받아 옴 + 5 = 6자리
            password = start_char + "".join(remaining_chars_tuple)
            
            try:
                # extractall() 압축을 해제하는 함수, 기존의 비밀번호를 인코딩하여 해제 
                zip_file.extractall(pwd=password.encode('utf-8'))
                print(f"\n[Process-{process_id}] ★★★ 비밀번호 찾음! ★★★")
                print(f"[Process-{process_id}] 시도 횟수: {count + 1}")
                return password, count + 1

            except (RuntimeError, zipfile.BadZipFile, zlib.error):
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
    
    # ... (zip 파일 생성 부분은 동일) ...

    # --- 멀티프로세싱 설정 ---
    try:
        cpu_cores = multiprocessing.cpu_count()
        print(f"사용 가능한 CPU 코어: {cpu_cores}개")
    except NotImplementedError:
        cpu_cores = 1
        print("CPU 코어 수를 확인할 수 없어 1개로 실행합니다.")

    # 한 장씩 돌아가며 카드를 나눠주는 방식([i::cpu_cores])
    charset_chunks = [CHARSET[i::cpu_cores] for i in range(cpu_cores)]
    # (번호, 파일 이름, 담당할 문자 묶음)을 튜플로 만듬 // 그대로 try_password 함수에 사용됨
    args = [(i, ZIP_FILENAME, chunk) for i, chunk in enumerate(charset_chunks)]

    found_password = None
    total_attempts = 0
    
    pool = None 
    try:
        # 프로세스를 미리 만들어 놓고 재사용하기 위해서 직접 지정하는 방식이 아니라 Pool을 사용한다고 함 
        pool = multiprocessing.Pool(processes=cpu_cores)
        # starmap() 여러 개의 인자를 필요로 하는 함수(try_password)를 병렬로 실행
        results = pool.starmap(try_password, args)
        
        for password, attempts in results:
            total_attempts += attempts
            if password:
                found_password = password
                pool.terminate()
                break
    
    except KeyboardInterrupt:
        print("\n\n[!] 사용자 요청으로 작업을 중단합니다...")
        if pool:
            pool.terminate() # 모든 자식 프로세스를 강제 종료
            pool.join()      # 자식 프로세스가 완전히 종료될 때까지 대기 
            # 메인프로세스가 자식프로세스를 기다리지 않고 종료하면 자식프로세스들은 좀비프로세스가 됨 / 불필요한 자리 차지

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
        # KeyboardInterrupt로 종료된 경우 실패 메시지를 수정할 수 있습니다.
        print("작업이 중단되었거나, 모든 조합을 시도했지만 비밀번호를 찾지 못했습니다.")
        
    print(f"총 시도 횟수: {total_attempts:,}")
    print(f"총 소요 시간: {elapsed_time:.2f}초")

if __name__ == '__main__':
    # Windows나 macOS에서 파이썬 스크립트를 하나의 실행 파일(.exe 등)로 만들 때 멀티프로세싱 기능이 올바르게 동작하도록 지원
    # 이 함수를 호출하지 않으면 에러가 발생하는 경우가 많음
    multiprocessing.freeze_support()
    unlock_zip()