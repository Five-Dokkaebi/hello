# 확인 창(버튼 1개)
import sys
from PySide6.QtWidgets import (
    QApplication, QDialog, QLabel, QPushButton,
    QVBoxLayout
)
from PySide6.QtGui import QFont, QPainter, QPainterPath, QColor, QPen
from PySide6.QtCore import Qt

class InfoDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 150)

        # 타이틀바 제거 + 투명 배경
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 메시지 라벨
        label = QLabel("등록되었습니다.")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 12, QFont.Bold))

        # 확인 버튼
        ok_btn = QPushButton("확인")
        ok_btn.setFixedWidth(80)
        ok_btn.clicked.connect(self.accept)

        # 버튼 스타일: 테두리만 검정
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1.5px solid black;
                border-radius: 5px;
                padding: 6px 10px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)

        # 전체 레이아웃
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addStretch()
        layout.addWidget(label)
        layout.addStretch()
        layout.addWidget(ok_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def paintEvent(self, event):
        """둥근 배경과 검정 테두리 그리기"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect().adjusted(1, 1, -2, -2)
        radius = 20

        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)

        # 배경 채우기
        painter.fillPath(path, QColor("white"))

        # 테두리 그리기
        pen = QPen(QColor("black"))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawPath(path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = InfoDialog()
    dlg.exec()  # 모달 실행

    sys.exit()
