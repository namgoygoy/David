PASSWORD_FILENAME = 'password 2.txt' 
RESULT_FILENAME = 'result.txt'

def caesar_cipher_decode(target_text):
    """
    대소문자가 섞인 카이사르 암호를 해독하는 수정된 함수.
    """
    decrypted_results = {}
    
    print(f"원본 암호: '{target_text}'\n")
    print("--- 카이사르 암호 해독 시도 (1-26) ---")

    for shift in range(1, 27):
        decrypted_text = ''
        for char in target_text:
            # 소문자
            if 'a' <= char <= 'z': 
                shifted_char_code = ord(char) - shift
                if shifted_char_code < ord('a'):
                    shifted_char_code += 26
                decrypted_text += chr(shifted_char_code)
                # 대문자
            elif 'A' <= char <= 'Z':
                shifted_char_code = ord(char) - shift
                if shifted_char_code < ord('A'):
                    shifted_char_code += 26
                decrypted_text += chr(shifted_char_code)
            # 알파벳이 아닌 문자(공백, 숫자 등)는 그대로 유지
            else:
                decrypted_text += char
        
        decrypted_results[shift] = decrypted_text
        print(f"{shift:2d}번째 이동: {decrypted_text}")

    print("\n[!] 직접 정답을 선택해주세요.")
    return decrypted_results


if __name__ == '__main__':
    # 1. 'password 2.txt' 파일 읽어오기
    try:
        with open(PASSWORD_FILENAME, 'r', encoding='utf-8') as f:
            encrypted_password = f.read().strip()
    except FileNotFoundError:
        print(f"오류: '{PASSWORD_FILENAME}'을 찾을 수 없습니다.")
        # 파일이 없을 경우, 제공된 텍스트로 테스트를 진행합니다.
        encrypted_password = 'B ehox Ftkl' 
        print(f"파일을 찾지 못해, '{encrypted_password}'로 테스트를 진행합니다.")
    except Exception as e:
        print(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        exit()

    # 2. 카이사르 암호 해독 함수 호출
    results = caesar_cipher_decode(encrypted_password)

    final_result = ''

    # 3. 사용자가 직접 정답 선택
    while True:
        try:
            user_choice = int(input(">> 의미있는 문장이 나온 번호를 입력하세요 (1-26): "))
            if 1 <= user_choice <= 26:
                final_result = results.get(user_choice)
                if final_result:
                    print(f"최종 해독 결과: {final_result}")
                    break
                else:
                    print("오류: 결과를 찾을 수 없습니다.")
            else:
                print("1에서 26 사이의 숫자를 입력해주세요.")
        except ValueError:
            print("오류: 숫자를 입력해야 합니다.")
    
    # 4. 최종 결과를 result.txt 파일로 저장
    try:
        with open(RESULT_FILENAME, 'w', encoding='utf-8') as f:
            f.write(final_result)
        print(f"\n성공: 최종 암호를 '{RESULT_FILENAME}' 파일에 저장했습니다.")
    except IOError as e:
        print(f"파일을 저장하는 중 오류가 발생했습니다: {e}")