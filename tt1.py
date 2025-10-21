import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QHBoxLayout, QFrame, QHeaderView, QTextEdit, QFormLayout
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt, QSize


# --- '도서 등록창' 클래스 ---
class RegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("도서등록")
        self.setGeometry(200, 200, 550, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            /* --- 이 부분이 수정되었습니다 --- */
            QLabel {
                font-size: 10pt;
                border: none; /* 라벨의 테두리를 명시적으로 제거합니다. */
            }
            QLineEdit, QTextEdit {
                background-color: white;
                border: 1px solid #a0a0a0;
                font-size: 10pt;
            }
            QPushButton {
                background-color: #e1e1e1;
                border: 1px solid #adadad;
                padding: 5px;
            }
            /* 이미지와 똑같은 창 닫기 버튼 스타일 */
            QPushButton#close_button {
                background-color: red;
                color: white;
                font-weight: bold;
                border: 1px solid darkred;
                font-size: 12pt;
                qproperty-iconSize: 0px; /* 아이콘 크기를 0으로 만들어 텍스트만 보이게 함 */
            }
            QLabel#image_placeholder {
                background-color: white;
                border: 1px solid #a0a0a0;
                min-width: 200px; /* 최소 너비 */
                min-height: 250px; /* 최소 높이 */
            }
        """)

        # --- 전체 창 레이아웃 ---
        window_layout = QVBoxLayout(self)
        window_layout.setContentsMargins(0, 0, 0, 10)  # 창 여백 (하단만 10)

        # --- 1. 커스텀 타이틀바 ---
        title_bar = QWidget()
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(10, 5, 5, 5)

        title_label = QLabel("도서등록")
        title_label.setStyleSheet("font-weight: bold;")

        close_button = QPushButton("X")
        close_button.setObjectName("close_button")
        close_button.setFixedSize(30, 30)
        close_button.clicked.connect(self.close)  # 버튼 클릭 시 창 닫기

        title_bar_layout.addWidget(title_label)
        title_bar_layout.addStretch(1)
        title_bar_layout.addWidget(close_button)
        window_layout.addWidget(title_bar)

        # --- 2. 메인 콘텐츠 프레임 ---
        main_frame = QFrame()
        main_frame.setStyleSheet("background-color: #f0f0f0; border: 1px solid #a0a0a0; border-radius: 8px;")
        main_frame.setContentsMargins(15, 15, 15, 15)
        window_layout.addWidget(main_frame, 1)  # 남은 공간을 모두 차지하도록 stretch = 1

        # 메인 프레임의 전체 레이아웃
        main_layout = QVBoxLayout(main_frame)

        # --- 3. 상단(65%) / 하단(35%) 분할 ---
        top_layout = QHBoxLayout()  # 65% 차지
        bottom_layout = QVBoxLayout()  # 35% 차지

        main_layout.addLayout(top_layout, 65)
        main_layout.addLayout(bottom_layout, 35)

        # --- 3-1. 상단 레이아웃 채우기 (좌/우 50% 분할) ---
        left_pane_layout = QVBoxLayout()
        right_pane_layout = QFormLayout()  # 라벨-입력창 쌍에 최적화된 레이아웃

        top_layout.addLayout(left_pane_layout, 50)
        top_layout.addLayout(right_pane_layout, 50)

        # 좌측: 사진 영역
        image_placeholder = QLabel()  # 사진이 보일 라벨
        image_placeholder.setObjectName("image_placeholder")
        image_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)

        photo_select_button = QPushButton("사진선택")

        left_pane_layout.addWidget(image_placeholder)
        left_pane_layout.addWidget(photo_select_button)

        # 우측: 도서 정보 입력 영역
        right_pane_layout.setSpacing(10)
        right_pane_layout.addRow("제목", QLineEdit())
        right_pane_layout.addRow("저자", QLineEdit())
        right_pane_layout.addRow("출판사", QLineEdit())
        right_pane_layout.addRow("가격", QLineEdit())
        right_pane_layout.addRow("링크", QLineEdit())
        right_pane_layout.addRow("ISBN", QLineEdit())

        # --- 3-2. 하단 레이아웃 채우기 ---
        book_desc_label = QLabel("책 설명")
        book_desc_edit = QTextEdit()

        bottom_layout.addWidget(book_desc_label)
        bottom_layout.addWidget(book_desc_edit)

        # 하단 버튼/라벨 영역
        footer_layout = QHBoxLayout()
        # '잔여권수' 라벨 (rich text를 사용해 ':'만 빨간색으로)
        remaining_label = QLabel("잔여권수<b><font color='red'>:</font></b> 2")
        register_button = QPushButton("등록")

        footer_layout.addWidget(remaining_label)
        footer_layout.addStretch(1)  # 중간에 공간을 밀어넣음
        footer_layout.addWidget(register_button)

        bottom_layout.addLayout(footer_layout)

        # 기본 윈도우 프레임을 숨겨서 커스텀 타이틀바만 보이게 함
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)


# --- 메인 윈도우 클래스 (이전과 동일) ---
class BookManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # ... (이전 코드와 동일한 내용이므로 생략) ...
        # (이 코드를 실행하려면 아래 주석을 풀고 이전 단계의 코드를 여기에 붙여넣으세요)
        self.setWindowTitle("도서 관리 프로그램")
        self.setGeometry(100, 100, 850, 550)

        self.setStyleSheet("""
            QMainWindow { background-color: #f0f0f0; }
            QLabel#title { font-size: 16pt; font-weight: bold; }
            QLineEdit { font-size: 10pt; height: 28px; }
            QPushButton { font-size: 9pt; background-color: #e1e1e1; border: 1px solid #adadad; padding: 5px; }
            QPushButton:hover { background-color: #e5e5e5; }
            QFrame#main_frame { background-color: white; border: 1px solid #a0a0a0; border-radius: 8px; }
            QPushButton#tab_active { background-color: #D0D0D0; font-weight: bold; border-bottom: 1px solid #D0D0D0; }
            QPushButton#tab_inactive { background-color: #f0f0f0; }
            QTableWidget { border: 1px solid #c0c0c0; gridline-color: #d0d0d0; background-color: #E8E8E8; font-size: 10pt; }
            QHeaderView::section { background-color: black; color: white; font-weight: bold; padding: 5px; border: 0px; }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 10, 20, 20)
        main_layout.setSpacing(10)
        title_label = QLabel("도서 관리 프로그램")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        main_layout.addSpacing(5)
        search_layout = QHBoxLayout()
        search_entry = QLineEdit()
        search_entry.setPlaceholderText("제목 또는 저자를 입력하십시오.")
        search_layout.addWidget(search_entry)
        search_button = QPushButton("검색")
        search_layout.addWidget(search_button)
        main_layout.addLayout(search_layout)
        main_frame = QFrame()
        main_frame.setObjectName("main_frame")
        main_frame.setFrameShape(QFrame.Shape.StyledPanel)
        main_layout.addWidget(main_frame)
        frame_layout = QVBoxLayout(main_frame)
        frame_layout.setContentsMargins(15, 15, 15, 15)
        top_bar_layout = QHBoxLayout()
        book_tab_button = QPushButton("도서관리")
        book_tab_button.setObjectName("tab_active")
        member_tab_button = QPushButton("회원관리")
        member_tab_button.setObjectName("tab_inactive")
        top_bar_layout.addStretch(1)
        top_bar_layout.addWidget(book_tab_button)
        top_bar_layout.addWidget(member_tab_button)
        top_bar_layout.addStretch(1)
        register_button_container = QWidget()
        register_layout = QHBoxLayout(register_button_container)
        register_layout.setContentsMargins(0, 0, 0, 0)
        register_layout.addStretch()
        register_button = QPushButton("도서등록")
        register_button.clicked.connect(self.open_registration_window)
        register_layout.addWidget(register_button)
        top_bar_layout.addWidget(register_button_container)
        frame_layout.addLayout(top_bar_layout)
        frame_layout.addSpacing(15)
        table = QTableWidget()
        table.setRowCount(5)
        table.setColumnCount(5)
        headers = ["제목", "ISBN", "저자", "가격", "출판사"]
        table.setHorizontalHeaderLabels(headers)
        table.verticalHeader().setVisible(False)
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        for i in range(table.rowCount()):
            table.setRowHeight(i, 35)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        frame_layout.addWidget(table)

    def open_registration_window(self):
        self.reg_window = RegistrationWindow()
        self.reg_window.show()


# --- 프로그램 실행 ---
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BookManagerWindow()
    window.show()
    sys.exit(app.exec())

