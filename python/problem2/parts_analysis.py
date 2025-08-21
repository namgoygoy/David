import numpy as np
import os

def analyze_parts_data():
    """
    여러 CSV 파일의 부품 데이터를 통합하고 분석하여 보강이 필요한 부품을 찾아냅니다.
    """
    try:
        # --- [준비] 파일 경로 설정 ---
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_names = [
            'mars_base_main_parts-001.csv',
            'mars_base_main_parts-002.csv',
            'mars_base_main_parts-003.csv'
        ]
        file_paths = [os.path.join(script_dir, name) for name in file_names]
        output_csv = os.path.join(script_dir, 'parts_to_work_on.csv')

        # 1. 세 개의 CSV 파일을 NumPy로 읽기
        # 첫 번째 파일에서 부품 이름(문자열)과 첫 번째 강도 데이터(숫자)를 읽음
        part_names = np.genfromtxt(file_paths[0], delimiter=',', skip_header=1, dtype=str, usecols=0)
        arr1 = np.genfromtxt(file_paths[0], delimiter=',', skip_header=1, usecols=1)
        
        # 나머지 파일에서는 강도 데이터만 읽음
        arr2 = np.genfromtxt(file_paths[1], delimiter=',', skip_header=1, usecols=1)
        arr3 = np.genfromtxt(file_paths[2], delimiter=',', skip_header=1, usecols=1)

        # 2. 세 배열을 병합하여 parts라는 ndarray 생성
        # 각 부품의 3회차 강도 데이터를 하나의 2D 배열로 합침
        parts = np.column_stack((arr1, arr2, arr3))
        print("--- [1] 병합된 부품 강도 데이터 (parts) ---")
        print(parts)

        # 3. 항목별 평균값 계산
        # axis=1 : 각 행(부품)별로 평균을 계산
        average_strengths = np.mean(parts, axis=1)
        print("\n--- [2] 항목별 평균 강도 ---")
        print(average_strengths)

        # 4. 평균값이 50보다 작은 항목만 필터링
        filter_mask = average_strengths < 50
        parts_to_work_on_names = part_names[filter_mask]
        parts_to_work_on_averages = average_strengths[filter_mask]
        
        print("\n--- [3] 평균 강도 50 미만인 보강 필요 부품 ---")
        for name, avg in zip(parts_to_work_on_names, parts_to_work_on_averages):
            print(f"{name}: {avg:.3f}")

        # 5. 필터링 결과를 parts_to_work_on.csv로 저장 (예외 처리 포함)
        try:
            # 저장할 데이터를 이름과 평균 강도로 구성
            output_data = np.column_stack((parts_to_work_on_names, parts_to_work_on_averages))
            header = 'Part Name,Average Strength'
            # fmt='%s': 모든 데이터를 문자열 형식으로 저장
            np.savetxt(output_csv, output_data, delimiter=',', header=header, fmt='%s', comments='')
            print(f"\n✅ '{os.path.basename(output_csv)}' 파일이 성공적으로 저장되었습니다.")
        except Exception as e:
            print(f"\n🚨 파일 저장 중 오류 발생: {e}")

        # --- 보너스 과제 ---
        # 1. parts_to_work_on.csv를 다시 읽어서 parts2로 저장
        parts2 = np.genfromtxt(output_csv, delimiter=',', skip_header=1, dtype=str)
        print("\n--- [보너스 1] 저장된 CSV 파일 다시 읽기 (parts2) ---")
        print(parts2)

        # 2. parts2의 전치 행렬(transpose)을 구하여 parts3로 저장하고 출력
        parts3 = parts2.T
        print("\n--- [보너스 2] 전치 행렬 (parts3) ---")
        print(parts3)

    except FileNotFoundError as e:
        print(f"\n🚨 오류: 데이터 파일을 찾을 수 없습니다. ({e.filename})")
    except Exception as e:
        print(f"\n🚨 예상치 못한 오류가 발생했습니다: {e}")


if __name__ == '__main__':
    analyze_parts_data()
