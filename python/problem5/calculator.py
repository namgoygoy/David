import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout
# 이벤트 처리, 위젯 창, 텍스트 라벨, 버튼, 레이아웃 배치
from PyQt5.QtCore import Qt
# 숫자와 문자 위치 구분

class Calculator:
    """계산기의 모든 비즈니스 로직을 담당하는 클래스"""
    def __init__(self):
        self.reset()

    def reset(self):
        self.current_input = ''
        self.first_operand = None
        self.operator = None
        self.result = None

    def add_digit(self, digit):
        # 소수점 여러개 찍히는 거 방지
        if '.' in self.current_input and digit == '.':
            return self.current_input
        self.current_input += digit
        return self.current_input

    def set_operator(self, op):
        # 첫번쨰 연산한 수를 임시 저장하고 그 다음 수를 준비하기 위한 함수
        if self.first_operand is not None and self.current_input:
             self.calculate()
        if self.current_input:
            self.first_operand = float(self.current_input)
        self.operator = op
        self.current_input = ''

    def calculate(self):
        # '=' 눌렀을 떄 호출, 
        if self.first_operand is None or not self.current_input or self.operator is None:
            # 하나만 있을 때 현재 입력한 수 반환, 없을 떄는 0 반환
            return self.current_input if self.current_input else '0'
        second_operand = float(self.current_input)
        try:
            if self.operator == '+': self.result = self.first_operand + second_operand
            elif self.operator == '-': self.result = self.first_operand - second_operand
            # 기본적인 알파벳과 곱섭을 위한 유니코드문자를 구별하기 위한 박스
            elif self.operator == '×': self.result = self.first_operand * second_operand
            elif self.operator == '÷':
                # 0인 경우에는 오류 처리
                if second_operand == 0: return '오류'
                self.result = self.first_operand / second_operand
        # 파이썬이 감당하는 범위 초과 발생 시
        except OverflowError:
            return '오류'
        # 12.0 = 12
        if self.result == int(self.result): self.current_input = str(int(self.result))
        # 12.5 = 12.5
        else: self.current_input = str(self.result)
        
        # 연산한 값 저장
        self.first_operand = self.result 
        self.operator = None 
        return self.current_input

    def toggle_sign(self):
        # 음수와 양수를 바꾸기 위한 함수
        if self.current_input:
            # startswith() 지정한 문자인지 판별 스택보다 더 깔끔하게 구현 가능
            if self.current_input.startswith('-'): self.current_input = self.current_input[1:]
            else: self.current_input = '-' + self.current_input
        return self.current_input
    
    def apply_percentage(self):
        if self.current_input:
            value = float(self.current_input) / 100
            self.current_input = str(value)
        return self.current_input

# Calculator 클래스를 상속받아 기능을 확장합니다.
class EngineeringCalculator(Calculator):
    """공학용 계산기 기능을 추가로 구현한 클래스"""
    def __init__(self):
        super().__init__() # 부모 클래스(Calculator)의 __init__을 호출

    def unary_operation(self, operation):
        """하나의 숫자에 바로 적용되는 연산 (sin, cos, x² 등)을 처리합니다."""
        if not self.current_input:
            return '0'
        try:
            value = float(self.current_input)
            if operation == 'sin': result = math.sin(math.radians(value))
            elif operation == 'cos': result = math.cos(math.radians(value))
            elif operation == 'tan': result = math.tan(math.radians(value))
            elif operation == 'sinh': result = math.sinh(math.radians(value))
            elif operation == 'cosh': result = math.cosh(math.radians(value))
            elif operation == 'tanh': result = math.tanh(math.radians(value))
            elif operation == 'x²': result = value ** 2
            elif operation == 'x³': result = value ** 3
            else: return self.current_input

            # 1,2,3 을 123으로 받기 위해 
            if result == int(result): self.current_input = str(int(result))
            else: self.current_input = str(result)
            return self.current_input
        # ValueError 케이스: 음수의 제곱일 때
        except (ValueError, OverflowError):
            return '오류'

    def set_constant(self, constant):
        """파이(π)와 같은 상수를 입력합니다."""
        if constant == 'π':
            self.current_input = str(math.pi)
        return self.current_input


class EngineeringCalculatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.calculator = EngineeringCalculator() # EngineeringCalculator 인스턴스 생성
        self.init_ui()

    def init_ui(self):
        # 나중에 다시 찾아오기 위해서 라벨링, QLabel: 도화지를 준비
        self.result_label = QLabel('0', self)
        self.result_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.result_label.setStyleSheet('font-size: 35px; border: 1px solid gray; padding: 10px;')
        self.result_label.setMinimumHeight(80)
        
        #격자판(grid) 생성
        grid = QGridLayout()
        self.setLayout(grid)

        buttons = {
            # 키로 바로 값을 찾을 수 있는 딕셔너리가 유리
            '(': (1, 0), ')': (1, 1), 'mc': (1, 2), 'm+': (1, 3), 'm-': (1, 4), 'mr': (1, 5), 'AC': (1, 6), '+/-': (1, 7), '%': (1, 8), '÷': (1, 9),
            '2nd': (2, 0), 'x²': (2, 1), 'x³': (2, 2), 'xʸ': (2, 3), 'eˣ': (2, 4), '10ˣ': (2, 5), '7': (2, 6), '8': (2, 7), '9': (2, 8), '×': (2, 9),
            '¹/x': (3, 0), '√x': (3, 1), '∛x': (3, 2), 'ʸ√x': (3, 3), 'ln': (3, 4), 'log₁₀': (3, 5), '4': (3, 6), '5': (3, 7), '6': (3, 8), '-': (3, 9),
            'x!': (4, 0), 'sin': (4, 1), 'cos': (4, 2), 'tan': (4, 3), 'e': (4, 4), 'EE': (4, 5), '1': (4, 6), '2': (4, 7), '3': (4, 8), '+': (4, 9),
            'Rad': (5, 0), 'sinh': (5, 1), 'cosh': (5, 2), 'tanh': (5, 3), 'π': (5, 4), 'Rand': (5, 5), '0': (5, 6, 1, 2), '.': (5, 8), '=': (5, 9),
        }
        
        # 위젯 배치 초기값 
        grid.addWidget(self.result_label, 0, 0, 1, 10)

        # items() 딕셔너리에서 쌍으로 가져 옴
        for text, pos in buttons.items():
            # 버튼 생성
            button = QPushButton(text, self)
            button.setStyleSheet('font-size: 18px; height: 50px;')
            button.clicked.connect(self.on_button_click)
            # 버튼의 좌표 len((1, 6))는 2이므로 (1, 6)이라면 pos[0] = 1 pos[1] = 6
            if len(pos) == 2: grid.addWidget(button, pos[0], pos[1])
            
            else: grid.addWidget(button, pos[0], pos[1], pos[2], pos[3])

        self.setWindowTitle('공학용 계산기')
        self.setGeometry(100, 100, 900, 450)
        self.show()

    def on_button_click(self):
        sender = self.sender()
        button_text = sender.text()
        display_text = self.result_label.text()

        # 공학용 계산 기능 버튼들
        unary_operations = ['sin', 'cos', 'tan', 'sinh', 'cosh', 'tanh', 'x²', 'x³']

        if button_text.isdigit() or button_text == '.':
            display_text = self.calculator.add_digit(button_text)
        elif button_text in ['+', '-', '×', '÷']:
            self.calculator.set_operator(button_text)
            display_text = str(self.calculator.first_operand) if self.calculator.first_operand is not None else '0'
        elif button_text == '=':
            display_text = self.calculator.calculate()
        elif button_text == 'AC':
            self.calculator.reset()
            display_text = '0'
        elif button_text == '+/-':
            display_text = self.calculator.toggle_sign()
        elif button_text == '%':
            display_text = self.calculator.apply_percentage()
        elif button_text in unary_operations:
            display_text = self.calculator.unary_operation(button_text)
        elif button_text == 'π':
            display_text = self.calculator.set_constant('π')

        self.result_label.setText(str(display_text))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EngineeringCalculatorApp()
    sys.exit(app.exec_())