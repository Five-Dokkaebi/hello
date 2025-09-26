#도서 반납 창
import sys
from PySide6.QtWidgets import (
    QApplication, QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QWidget
)
from PySide6.QtGui import QFont, QPainter, QPainterPath, QColor, QPen
from PySide6.QtCore import Qt

class ReturnDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 400)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setup_ui()

    def setup_ui(self):
        # ===== Title & Close =====
        title_layout = QHBoxLayout()
        title_label = QLabel("반납할 도서를 선택하세요.")
        title_label.setFont(QFont("Arial", 11, QFont.Bold))

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 30)
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                border: none;
                font-weight: bold;
                font-size: 14px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)

        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(close_btn)

        # ===== Search =====
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("도서 또는 저자를 입력하세요.")
        self.search_input.setStyleSheet("padding: 5px;")
        search_btn = QPushButton("검색")
        search_btn.setFixedWidth(60)
        search_btn.clicked.connect(self.search_books)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)

        # ===== Table =====
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["책이름", "ISBN", "대여일", "반납예정일", "반납기간"])
        self.table.setColumnCount(6)  # 마지막은 체크박스용
        self.table.setHorizontalHeaderLabels(["책이름", "ISBN", "대여일", "반납예정일", "반납기간", "선택"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: black; 
            }
            QHeaderView::section {
                border: 1px solid black;      
                background-color: black; 
                color: white;
            }
        """)

        self.load_dummy_data()

        # ===== Return Button =====
        return_btn = QPushButton("반납하기")
        return_btn.setFixedWidth(100)
        return_btn.clicked.connect(self.return_books)
        return_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1.5px solid black;
                padding: 6px 12px;
                border-radius: 5px;
            }
        """)

        # ===== Main Layout =====
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.addLayout(title_layout)
        main_layout.addSpacing(10)
        main_layout.addLayout(search_layout)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.table)
        main_layout.addSpacing(10)
        main_layout.addWidget(return_btn, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

    def load_dummy_data(self):
        # 예시용 데이터
        data = [
            ["책읽는여우", "567864", "2025.05.26 13:00", "2025.06.12 15:00", "14일 남음"],
            ["파이썬코딩", "123456", "2025.05.20 10:30", "2025.06.10 10:30", "6일 남음"]
        ]
        self.table.setRowCount(len(data))
        for row, row_data in enumerate(data):
            for col, item in enumerate(row_data):
                self.table.setItem(row, col, QTableWidgetItem(item))

            # 체크박스 추가
            checkbox = QCheckBox()
            checkbox_widget = QWidget()
            layout = QHBoxLayout(checkbox_widget)
            layout.addWidget(checkbox)
            layout.setAlignment(Qt.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)
            self.table.setCellWidget(row, 5, checkbox_widget)

    def search_books(self):
        # TODO: DB 검색 로직 연결
        keyword = self.search_input.text()
        print(f"검색: {keyword}")

    def return_books(self):
        # TODO: 선택된 책 DB 업데이트
        selected_books = []
        for row in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(row, 5).findChild(QCheckBox)
            if checkbox and checkbox.isChecked():
                title = self.table.item(row, 0).text()
                selected_books.append(title)
        print("반납할 도서:", selected_books)

    def paintEvent(self, event):
        # 둥근 배경 + 테두리
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect().adjusted(1, 1, -2, -2)
        path = QPainterPath()
        path.addRoundedRect(rect, 20, 20)

        painter.fillPath(path, QColor("white"))
        pen = QPen(QColor("black"))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawPath(path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = ReturnDialog()
    dlg.exec()
    sys.exit()
