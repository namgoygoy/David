import csv
# 이진 파일 처리 (예: .bin, .jpg, .exe)
import pickle
import os

def manage_inventory():
    """
    Mars 기지 적재물 목록을 분석하고 위험물을 분류하여 저장합니다.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_csv = os.path.join(script_dir, 'Mars_Base_Inventory_List.csv')
    danger_csv = os.path.join(script_dir, 'Mars_Base_Inventory_danger.csv')
    output_bin = os.path.join(script_dir, 'Mars_Base_Inventory_List.bin')

    try:
        # 1. CSV 파일(Mars_Base_Inventory_List.csv)의 내용을 읽어서 화면에 출력
        print(f'--- [1] 원본 CSV 파일 ({os.path.basename(input_csv)}) 내용 ---')
        with open(input_csv, 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)
        
        # 2. CSV 내용을 List 객체로 변환
        inventory_list = []
        header = [] # 항목을 읽어 오기 위해서
        with open(input_csv, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader) # 항목을 읽어 오기 위해서
            for row in reader:
                # 'Flammability' 값을 float으로 변환 시도, 실패 시 0.0으로 처리
                try:
                    # CSV 파일의 5번째 열(인덱스 4)을 float으로 변환
                    row[4] = float(row[4])
                except (ValueError, IndexError):
                    # 값이 비어있거나 잘못된 경우 0.0으로 기본값 설정
                    if len(row) > 4:
                        row[4] = 0.0
                    else:
                        # Flammability 열 자체가 없는 경우를 대비
                        while len(row) < 5:
                            row.append(None)
                        row[4] = 0.0
                inventory_list.append(row)

        # 3. 인화성 지수(Flammability)를 기준으로 내림차순 정렬
        inventory_list.sort(key=lambda x: x[4], reverse=True)
        print('\n--- [2] 인화성 지수 기준 정렬 결과 ---')
        print(header)
        for item in inventory_list:
            print(item)

        # 4. 인화성 지수가 0.7 이상인 항목만 필터링
        danger_list = [item for item in inventory_list if item[4] >= 0.7]
        
        print('\n--- [3] 인화성 지수 0.7 이상 위험물 목록 ---')
        print(header)
        for item in danger_list:
            print(item)

        # 5. 필터링 결과를 Mars_Base_Inventory_danger.csv로 저장
        with open(danger_csv, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(danger_list)
        print(f"\n✅ '{os.path.basename(danger_csv)}' 파일이 성공적으로 저장되었습니다.")

        # --- 보너스 과제 ---
        # 1. 정렬된 전체 목록을 이진 파일로 저장 Mars_Base_Inventory_List.bin wb의 b는 바이너리 데이터로 변경 
        with open(output_bin, 'wb') as file:
            pickle.dump(inventory_list, file)
        print(f"✅ '{os.path.basename(output_bin)}' 이진 파일이 성공적으로 저장되었습니다.")

        # 2. 저장한 이진 파일을 다시 읽어서 내용 출력
        with open(output_bin, 'rb') as file:
            loaded_list = pickle.load(file)
        print(f'\n--- [보너스] 이진 파일 ({os.path.basename(output_bin)}) 로드 결과 ---')
        for item in loaded_list:
            print(item)

    except FileNotFoundError:
        print(f"\n🚨 오류: '{os.path.basename(input_csv)}' 파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"\n🚨 예상치 못한 오류가 발생했습니다: {e}")


if __name__ == '__main__':
    manage_inventory()
