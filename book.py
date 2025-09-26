# 확인 창(버튼 2개)
import sys
from PySide6.QtWidgets import (
    QApplication, QDialog, QLabel, QPushButton,
    QHBoxLayout, QVBoxLayout
)
from PySide6.QtGui import QFont, QPainter, QPainterPath, QColor, QPen
from PySide6.QtCore import Qt

class ConfirmDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 150)

        # 타이틀바 없애고, 배경 투명하게
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 라벨 (메시지)
        label = QLabel("등록하시겠습니까?")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 12, QFont.Bold))

        # 버튼
        yes_btn = QPushButton("Yes")
        no_btn = QPushButton("No")

        yes_btn.setStyleSheet("""
            QPushButton {
                background-color: #d3d3d3;
                padding: 6px 20px;
                border-radius: 5px;
                border: 1px solid black;
            }
        """)
        no_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                padding: 6px 20px;
                border-radius: 5px;
                border: 1px solid black;
            }
        """)

        yes_btn.clicked.connect(self.accept)
        no_btn.clicked.connect(self.reject)

        # 버튼 레이아웃
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(30)
        btn_layout.addStretch()
        btn_layout.addWidget(yes_btn)
        btn_layout.addWidget(no_btn)
        btn_layout.addStretch()

        # 메인 레이아웃
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)  # 여백 설정
        main_layout.addStretch()
        main_layout.addWidget(label)
        main_layout.addStretch()
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

    def paintEvent(self, event):
        """둥근 배경 + 검정색 테두리 그리기"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect().adjusted(1, 1, -2, -2)  # 테두리 고려하여 조정
        radius = 20

        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)

        # 배경 채우기
        painter.fillPath(path, QColor("white"))

        # 테두리 설정
        pen = QPen(QColor("black"))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawPath(path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = ConfirmDialog()
    result = dlg.exec()

    if result == QDialog.Accepted:
        print("등록됨")
    else:
        print("등록 취소됨")

    sys.exit()
