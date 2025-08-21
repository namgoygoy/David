import math

# --- 전역 변수: 재질별 밀도 (g/cm³) ---
MATERIAL_DENSITIES = {
    'glass': 2.4,
    'aluminum': 2.7,
    'carbon_steel': 7.85
}

def sphere_area(diameter, material, thickness=1.0):
    """
    반구체 돔의 표면적과 화성에서의 무게를 계산합니다.

    Args:
        diameter (float): 돔의 지름 (m).
        material (str): 돔의 재질 ('glass', 'aluminum', 'carbon_steel').
        thickness (float, optional): 돔의 두께 (cm). 기본값은 1.0cm.

    Returns:
        tuple: (표면적, 화성에서의 무게) 또는 오류 발생 시 (None, None).
    """
    # --- 보너스 과제: 유효하지 않은 파라미터 값에 대한 예외 처리 ---
    if not isinstance(diameter, (int, float)) or diameter <= 0:
        raise ValueError("오류: 지름은 0보다 큰 숫자여야 합니다.")
    if material not in MATERIAL_DENSITIES:
        raise ValueError(f"오류: 지원하지 않는 재질입니다. ({', '.join(MATERIAL_DENSITIES.keys())} 중 선택)")
    if not isinstance(thickness, (int, float)) or thickness <= 0:
        raise ValueError("오류: 두께는 0보다 큰 숫자여야 합니다.")

    # 1. 표면적 계산 (반구체이므로 구의 겉넓이 / 2)
    radius_m = diameter / 2
    surface_area_m2 = (4 * math.pi * radius_m**2) / 2

    # 2. 부피 계산 (표면적 * 두께)
    # 단위를 cm로 통일하여 계산
    surface_area_cm2 = surface_area_m2 * 10000  # m² to cm²
    volume_cm3 = surface_area_cm2 * thickness

    # 3. 지구에서의 무게(질량) 계산 (부피 * 밀도)
    density_g_cm3 = MATERIAL_DENSITIES[material]
    earth_weight_g = volume_cm3 * density_g_cm3
    earth_weight_kg = earth_weight_g / 1000

    # 4. 화성에서의 무게 계산 (지구 무게 * 0.38)
    mars_weight_kg = earth_weight_kg * 0.38

    return surface_area_m2, mars_weight_kg

def main():
    """
    사용자 입력을 받아 돔 설계 프로그램을 반복 실행하는 메인 함수.
    """
    while True:
        try:
            # 1. 사용자로부터 지름과 재질 입력받기
            diameter_input = input("돔의 지름(m)을 입력하세요 (종료하려면 'exit' 입력): ")
            if diameter_input.lower() == 'exit':
                print("프로그램을 종료합니다.")
                break

            material_input = input(f"재질을 선택하세요 ({', '.join(MATERIAL_DENSITIES.keys())}): ").lower()
            
            # 2. 입력값을 숫자로 변환
            diameter_float = float(diameter_input)

            # 3. sphere_area 함수 호출하여 계산
            area, weight = sphere_area(diameter=diameter_float, material=material_input)

            # 4. 결과 출력
            if area is not None and weight is not None:
                print("\n--- 계산 결과 ---")
                print(f"재질 ⇒ {material_input}, 지름 ⇒ {diameter_float}, 두께 ⇒ 1.0, "
                      f"면적 ⇒ {area:.3f} ㎡, 화성 무게 ⇒ {weight:.3f} kg\n")

        # 5. 잘못된 입력에 대한 예외 처리
        except ValueError as e:
            # sphere_area 함수에서 발생한 오류 또는 float 변환 오류 처리
            print(f"{e}\n")
        except Exception as e:
            # 그 외 예상치 못한 모든 오류 처리
            print(f"알 수 없는 오류가 발생했습니다: {e}\n")

if __name__ == '__main__':
    main()
