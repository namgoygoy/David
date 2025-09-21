import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class LabelExample(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 1. 비교용 기본 라벨: 이름표 없이 생성한 순수한 모습
        # 이 라벨은 만들고 나서 다시 제어하기 어렵습니다.
        basic_label = QLabel("↑ 위쪽이 QLabel() 생성 직후의 기본 모습입니다.", self)
        basic_label.setAlignment(Qt.AlignCenter) # 글자만 중앙 정렬

        # 2. 사용자 코드: 'self.result_label' 이름표를 붙여서 생성
        self.result_label = QLabel('0', self)


        # --- 이제 이름표를 붙인 'self.result_label'만 골라서 꾸며줍니다 ---

        # 이름표(self.result_label)를 이용해 라벨을 찾아가...
        # A. 정렬을 맞춥니다.
        self.result_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # B. 스타일을 적용합니다.
        self.result_label.setStyleSheet('''
            font-size: 35px;
            border: 1px solid gray;
            padding: 10px;
            background-color: #f0f0f0; /* 눈에 띄게 배경색 추가 */
        ''')

        # C. 최소 높이를 지정합니다.
        self.result_label.setMinimumHeight(80)


        # --- 위젯들을 화면에 배치하기 ---
        # QVBoxLayout은 위젯을 위에서 아래로 차곡차곡 쌓아줍니다.
        vbox = QVBoxLayout()
        vbox.addWidget(basic_label)      # 1번 라벨(기본)을 상자에 추가
        vbox.addWidget(self.result_label) # 2번 라벨(꾸민 것)을 상자에 추가

        self.setLayout(vbox) # 창의 최종 레이아웃으로 설정

        self.setWindowTitle('QLabel 생성 예제')
        self.setGeometry(300, 300, 400, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LabelExample()
    sys.exit(app.exec_())