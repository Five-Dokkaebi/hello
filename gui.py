import sys
from PySide6.QtWidgets import (
    QApplication, QDialog, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFrame, QTableWidget,
    QTableWidgetItem, QHeaderView, QWidget
)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt, QSize


class BookDetailDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('도서 정보와 대출 정보')
        self.setFixedSize(650, 450)
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 5px;
            }
            QLabel {
                color: #333333;
            }
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #cccccc;
                border-radius: 3px;
                padding: 5px 10px;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QLineEdit {
                border: 1px solid #cccccc;
                border-radius: 3px;
                padding: 3px;
            }
            QTableWidget {
                border: 1px solid #cccccc;
                gridline-color: #e0e0e0;
                selection-background-color: #aaddff;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 5px;
                border: 1px solid #cccccc;
                border-left: none;
                border-top: none;
            }
            QTableWidget QTableCornerButton::section {
                background-color: #f0f0f0;
                border: 1px solid #cccccc;
                border-left: none;
                border-top: none;
            }
        """)

        self.setWindowFlags(Qt.FramelessWindowHint)

        main_overall_layout = QVBoxLayout(self)
        main_overall_layout.setContentsMargins(10, 10, 10, 10)
        main_overall_layout.setSpacing(10)

        title_bar_layout = QHBoxLayout()
        title_bar_layout.setContentsMargins(0, 0, 0, 0)
        title_bar_label = QLabel("도서 정보와 대출 정보")
        title_bar_label.setFont(QFont("Arial", 10, QFont.Bold))
        title_bar_label.setStyleSheet("color: black;")

        self.close_button = QPushButton("X")
        self.close_button.setFixedSize(24, 24)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #FF0000;
                color: white;
                border: none;
                border-radius: 0px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #CC0000;
            }
        """)
        self.close_button.clicked.connect(self.reject)

        title_bar_layout.addWidget(title_bar_label)
        title_bar_layout.addStretch()
        title_bar_layout.addWidget(self.close_button)
        main_overall_layout.addLayout(title_bar_layout)

        info_section_layout = QHBoxLayout()
        info_section_layout.setSpacing(20)

        book_info_section_layout = QVBoxLayout()
        book_info_section_layout.setSpacing(5)

        book_info_title_label = QLabel("도서정보")
        book_info_title_label.setFont(QFont("Arial", 12, QFont.Bold))
        book_info_section_layout.addWidget(book_info_title_label, alignment=Qt.AlignLeft)

        title_separator = QFrame()
        title_separator.setFrameShape(QFrame.HLine)
        title_separator.setFrameShadow(QFrame.Sunken)
        title_separator.setFixedHeight(1)
        title_separator.setStyleSheet("background-color: #cccccc;")
        book_info_section_layout.addWidget(title_separator)

        book_details_layout = QGridLayout()
        book_details_layout.setContentsMargins(0, 10, 0, 0)
        book_details_layout.setSpacing(5)

        book_cover_label = QLabel()
        book_cover_label.setFixedSize(120, 160)
        book_cover_label.setStyleSheet("border: 1px solid #cccccc;")
        book_cover_label.setAlignment(Qt.AlignCenter)

        try:
            pixmap = QPixmap('book_cover.png')
            if pixmap.isNull():
                book_cover_label.setText("책 표지 이미지")
            else:
                book_cover_label.setPixmap(pixmap.scaled(120, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        except Exception:
            book_cover_label.setText("책 표지 이미지")

        title_text_label = QLabel("제목 :")
        title_value_label = QLabel("사랑학개론")
        author_text_label = QLabel("저자 :")
        author_value_label = QLabel("김승호")
        publisher_text_label = QLabel("출판사 :")
        publisher_value_label = QLabel("AGAPE")

        font = QFont("Malgun Gothic", 10)
        title_text_label.setFont(font);
        title_value_label.setFont(font)
        author_text_label.setFont(font);
        author_value_label.setFont(font)
        publisher_text_label.setFont(font);
        publisher_value_label.setFont(font)

        book_details_layout.addWidget(book_cover_label, 0, 0, 4, 1, alignment=Qt.AlignTop | Qt.AlignLeft)
        book_details_layout.addWidget(title_text_label, 0, 1)
        book_details_layout.addWidget(title_value_label, 0, 2)
        book_details_layout.addWidget(author_text_label, 1, 1)
        book_details_layout.addWidget(author_value_label, 1, 2)
        book_details_layout.addWidget(publisher_text_label, 2, 1)
        book_details_layout.addWidget(publisher_value_label, 2, 2)
        book_details_layout.setColumnStretch(2, 1)

        book_info_section_layout.addLayout(book_details_layout)

        book_description_label = QLabel("책 설명")
        book_description_label.setFont(font)
        book_description_label.setContentsMargins(0, 10, 0, 0)
        book_info_section_layout.addWidget(book_description_label, alignment=Qt.AlignTop | Qt.AlignLeft)

        isbn_label = QLabel("ISBN: 59-29309-49095")
        isbn_label.setFont(font)
        isbn_label.setContentsMargins(0, 10, 0, 0)
        book_info_section_layout.addWidget(isbn_label, alignment=Qt.AlignBottom | Qt.AlignLeft)

        book_info_section_layout.addStretch(1)

        loan_info_section_layout = QVBoxLayout()
        loan_info_section_layout.setSpacing(5)

        loan_info_title_label = QLabel("대출정보")
        loan_info_title_label.setFont(QFont("Arial", 12, QFont.Bold))
        loan_info_section_layout.addWidget(loan_info_title_label, alignment=Qt.AlignLeft)

        loan_title_separator = QFrame()
        loan_title_separator.setFrameShape(QFrame.HLine)
        loan_title_separator.setFrameShadow(QFrame.Sunken)
        loan_title_separator.setFixedHeight(1)
        loan_title_separator.setStyleSheet("background-color: #cccccc;")
        loan_info_section_layout.addWidget(loan_title_separator)

        loan_status_label = QLabel("대출가능")
        loan_status_label.setStyleSheet("color: green;")
        loan_status_label.setFont(font)
        loan_info_section_layout.addWidget(loan_status_label)

        search_widget = QWidget()
        search_layout = QHBoxLayout(search_widget)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_input = QLineEdit()
        search_input.setPlaceholderText("회원이름 또는 회원번호")
        search_input.setFont(font)
        search_button = QPushButton("검색")
        search_button.setFont(font)
        search_button.setFixedSize(50, 24)
        search_layout.addWidget(search_input)
        search_layout.addWidget(search_button)
        loan_info_section_layout.addWidget(search_widget)

        loan_table = QTableWidget()
        loan_table.setColumnCount(4)
        loan_table.setHorizontalHeaderLabels(['회원번호', '여부', '상태', '선택'])
        loan_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        loan_table.verticalHeader().setVisible(False)
        loan_table.setRowCount(1)
        loan_table.setFont(font)

        # QTableWidgetItem을 생성하고 읽기 전용으로 설정
        item1 = QTableWidgetItem("000001")
        item1.setFlags(item1.flags() & ~Qt.ItemIsEditable)  # 편집 불가능하게 설정
        loan_table.setItem(0, 0, item1)

        item2 = QTableWidgetItem("대출중")
        item2.setFlags(item2.flags() & ~Qt.ItemIsEditable)
        loan_table.setItem(0, 1, item2)

        item3 = QTableWidgetItem("가능")
        item3.setFlags(item3.flags() & ~Qt.ItemIsEditable)
        loan_table.setItem(0, 2, item3)

        select_button = QPushButton("선택")
        select_button.setFont(font)
        select_button.setStyleSheet("padding: 2px 5px; min-width: 40px;")
        loan_table.setCellWidget(0, 3, select_button)

        loan_info_section_layout.addWidget(loan_table)
        loan_info_section_layout.addStretch(1)

        info_section_layout.addLayout(book_info_section_layout, 1)
        info_section_layout.addLayout(loan_info_section_layout, 2)

        main_overall_layout.addLayout(info_section_layout)

        bottom_button_layout = QHBoxLayout()
        bottom_button_layout.addStretch()

        modify_button = QPushButton("수정")
        delete_button = QPushButton("삭제")

        modify_button.setFont(font)
        delete_button.setFont(font)

        bottom_button_layout.addWidget(modify_button)
        bottom_button_layout.addWidget(delete_button)

        main_overall_layout.addLayout(bottom_button_layout)

        self.old_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.close_button.geometry().contains(event.pos()) is False:
            self.old_pos = event.globalPos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPos() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.old_pos = None
        super().mouseReleaseEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = BookDetailDialog()
    dialog.exec()
    sys.exit(app.exec())