import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QTextEdit,
    QFormLayout, QSplitter, QHeaderView, QSizePolicy
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor, QPalette

class BookLoanApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('도서 정보와 대출 정보') # 타이틀 설정
        self.setGeometry(100, 100, 1000, 600)
        
        self.initUI()
        self.applyStyles()

    def initUI(self):
        # --- 전체 레이아웃 (수평 스플리터) ---
        main_layout = QVBoxLayout(self) # 전체 창의 레이아웃 (타이틀 바 역할 포함)
        
        # --- 상단 타이틀 바 역할 (커스텀 닫기 버튼 포함) ---
        title_bar_widget = QWidget()
        title_bar_layout = QHBoxLayout(title_bar_widget)
        title_bar_layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QLabel("도서 정보와 대출 정보")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        # 배경색이 밝으므로 텍스트 색상을 검정색(black)으로 설정
        title_label.setStyleSheet("color: black;") 
        
        # 빨간색 원형 닫기 버튼 (시뮬레이션)
        close_button = QPushButton("X")
        close_button.setFixedSize(80, 30) # 원형을 위해 가로세로 동일하게
        close_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white; /* 이미지처럼 X는 흰색 유지 */
                border-radius: 15px; /* 원형 */
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ff3333;
            }
        """)
        close_button.clicked.connect(self.close) # 실제 창 닫기 기능 연결

        title_bar_layout.addWidget(title_label)
        title_bar_layout.addStretch() # 타이틀을 왼쪽으로, 버튼을 오른쪽으로
        title_bar_layout.addWidget(close_button)
        
        # 전체 레이아웃에 커스텀 타이틀 바 추가
        main_layout.addWidget(title_bar_widget)

        # 메인 스플리터 (도서정보와 대출정보)
        content_splitter = QSplitter(Qt.Horizontal)
        
        # --- 1. 왼쪽: 도서정보 (전체 가로의 40%) ---
        book_info_group = QGroupBox("도서정보")
        # 그룹박스 타이틀 스타일 (폰트 크기 조절)
        book_info_group.setStyleSheet("QGroupBox::title { font-size: 20pt; font-weight: bold; color: black; }")
        
        book_splitter = QSplitter(Qt.Vertical) # 도서정보 내부 수직 스플리터

        # 1-1. 도서정보 (상단 50%)
        top_book_widget = QWidget()
        top_book_layout = QHBoxLayout(top_book_widget)
        
        # 책 표지 이미지 (임시 라벨)
        image_label = QLabel("책 표지 이미지")
        image_label.setFixedSize(150, 200) # 이미지 크기 고정 (예시)
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setStyleSheet("border: 1px solid black; background-color: #f0f0f0; color: black;")
        image_label.setFont(QFont("Arial", 10))

        # 제목, 저자, 출판사 (Form 레이아웃)
        details_widget = QWidget()
        details_layout = QFormLayout(details_widget)
        details_layout.setContentsMargins(10, 0, 0, 0) # 왼쪽 패딩
        
        # QLabel에 텍스트와 폰트 설정
        title_val = QLabel("사랑학개론")
        author_val = QLabel("김승호")
        publisher_val = QLabel("AGAPE")

        # 폰트 굵게, 크기 조정, 색상 검정
        font_bold = QFont("Arial", 10, QFont.Bold)
        title_val.setFont(font_bold)
        title_val.setStyleSheet("color: black;")
        author_val.setFont(font_bold)
        author_val.setStyleSheet("color: black;")
        publisher_val.setFont(font_bold)
        publisher_val.setStyleSheet("color: black;")

        details_layout.addRow(QLabel("제목:"), title_val)
        details_layout.addRow(QLabel("저자:"), author_val)
        details_layout.addRow(QLabel("출판사:"), publisher_val)
        
        # 폼 레이아웃의 라벨들도 폰트 및 색상 조정
        for i in range(details_layout.rowCount()):
            label_widget = details_layout.itemAt(i, QFormLayout.LabelRole).widget()
            if isinstance(label_widget, QLabel):
                label_widget.setFont(QFont("Arial", 10))
                label_widget.setStyleSheet("color: black;")

        top_book_layout.addWidget(image_label)
        top_book_layout.addWidget(details_widget) # 위젯으로 감싸서 추가

        # 1-2. 도서정보 (하단 50%)
        bottom_book_widget = QWidget()
        bottom_book_layout = QVBoxLayout(bottom_book_widget)
        
        book_desc_label = QLabel("책 설명")
        book_desc_label.setFont(QFont("Arial", 10, QFont.Bold))
        book_desc_label.setStyleSheet("color: black;")
        bottom_book_layout.addWidget(book_desc_label)
        
        description_text = QTextEdit()
        description_text.setReadOnly(True)
        description_text.setText("ISBN: 59-29309-49095\n\n여기에 긴 책 설명이 들어갈 수 있습니다. 이 부분은 스크롤 가능합니다.")
        description_text.setFont(QFont("Arial", 10))
        description_text.setStyleSheet("border: 1px solid #ccc; background-color: white; color: black;")
        
        bottom_book_layout.addWidget(description_text)

        book_splitter.addWidget(top_book_widget)
        book_splitter.addWidget(bottom_book_widget)
        book_splitter.setSizes([300, 300]) # 상하 50:50 비율 유지

        book_info_main_layout = QVBoxLayout(book_info_group)
        book_info_main_layout.addWidget(book_splitter)
        
        # --- 2. 오른쪽: 대출정보 (전체 가로의 60%) ---
        loan_info_group = QGroupBox("대출정보")
        loan_info_group.setStyleSheet("QGroupBox::title { font-size: 14pt; font-weight: bold; color: black; }")
        loan_info_layout = QVBoxLayout(loan_info_group)

        # 대출 가능 여부
        loan_status_label = QLabel("대출가능")
        loan_status_label.setFont(QFont("Arial", 14, QFont.Bold))
        # 이미지처럼 '대출가능'은 녹색(green)으로 유지
        loan_status_label.setStyleSheet("color: green; margin-bottom: 10px;") 
        loan_info_layout.addWidget(loan_status_label)

        # 회원 검색
        search_layout = QHBoxLayout()
        search_input = QLineEdit()
        search_input.setPlaceholderText("회원이름 또는 회원번호")
        search_input.setFont(QFont("Arial", 10))
        search_input.setStyleSheet("padding: 5px; border: 1px solid #ccc; background-color: white; color: black;")
        
        search_button = QPushButton("검색")
        search_button.setFixedSize(QSize(60, 30)) # 검색 버튼 크기
        search_button.setFont(QFont("Arial", 10, QFont.Bold))
        search_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1px solid black;
                border-radius: 3px;
                padding: 5px;
                color: black; /* 버튼 텍스트 검정 */
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        
        search_layout.addWidget(search_input)
        search_layout.addWidget(search_button)
        loan_info_layout.addLayout(search_layout)

        # 대여 회원 리스트 (테이블)
        member_table = QTableWidget()
        member_table.setColumnCount(4)
        member_table.setHorizontalHeaderLabels(["회원번호", "이름", "상태", "선택"])
        member_table.setFont(QFont("Arial", 10))
        member_table.setStyleSheet("QTableWidget { background-color: white; border: 1px solid #ccc; color: black; }"
                                   "QHeaderView::section { background-color: #e0e0e0; font-weight: bold; color: black; }"
                                   "QTableWidgetItem { padding: 5px; }")
        
        # 예시 데이터 추가 (이미지 참조)
        member_table.setRowCount(1)
        member_table.setItem(0, 0, QTableWidgetItem("000001"))
        member_table.setItem(0, 1, QTableWidgetItem("홍길동"))
        member_table.setItem(0, 2, QTableWidgetItem("가능")) 

        # *** [수정됨] ***
        # '선택' 항목 (이미지처럼 파란색 텍스트로)
        select_item = QTableWidgetItem("선택")
        select_item.setForeground(QColor(0, 0, 255)) # 파란색 (이미지 참조)
        select_font = QFont()
        select_font.setUnderline(True)
        select_font.setBold(True)
        select_font.setFamily("Arial")
        select_font.setPointSize(10)
        select_item.setFont(select_font)
        select_item.setTextAlignment(Qt.AlignCenter) # 가운데 정렬
        member_table.setItem(0, 3, select_item)
        
        member_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        loan_info_layout.addWidget(member_table)

        # 수정, 삭제 버튼 (오른쪽 하단)
        button_layout = QHBoxLayout()
        button_layout.addStretch(1) # 왼쪽에 빈 공간을 추가하여 버튼을 오른쪽으로 밀어냄
        
        modify_button = QPushButton("수정")
        delete_button = QPushButton("삭제")

        # 버튼 크기 및 스타일 조정
        button_width = 80
        button_height = 35
        button_font = QFont("Arial", 10, QFont.Bold)
        button_style = """
            QPushButton {
                background-color: white;
                border: 2px solid black; /* 테두리 두껍게 */
                border-radius: 5px;
                padding: 5px 10px;
                color: black; /* 버튼 텍스트 검정 */
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """
        
        modify_button.setFixedSize(QSize(button_width, button_height))
        modify_button.setFont(button_font)
        modify_button.setStyleSheet(button_style)

        delete_button.setFixedSize(QSize(button_width, button_height))
        delete_button.setFont(button_font)
        delete_button.setStyleSheet(button_style)
        
        button_layout.addWidget(modify_button)
        button_layout.addWidget(delete_button)
        
        loan_info_layout.addLayout(button_layout)
        
        # 메인 스플리터에 좌/우 그룹박스 추가
        content_splitter.addWidget(book_info_group)
        content_splitter.addWidget(loan_info_group)

        # 초기 스플리터 비율 설정 (40:60)
        content_splitter.setSizes([400, 600])

        # 전체 레이아웃에 내용 스플리터 추가
        main_layout.addWidget(content_splitter)

    def applyStyles(self):
        # 전체 위젯의 배경색을 하얀색으로 설정
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255)) # 하얀색
        self.setPalette(palette)
        
        # 기본 텍스트 색상을 검정으로 설정
        palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
        self.setPalette(palette)

        # 그룹박스 테두리 스타일 설정
        self.setStyleSheet("""
            QGroupBox {
                border: 1px solid lightgray; /* 옅은 회색 테두리 */
                border-radius: 5px;
                margin-top: 1ex; /* 타이틀이 테두리 위로 올라오도록 */
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left; /* 타이틀 위치 */
                padding: 0 3px;
                background-color: transparent; /* 타이틀 배경 투명 */
                color: black; /* 그룹박스 타이틀 검정 */
            }
        """)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BookLoanApp()
    ex.show()
    sys.exit(app.exec_())