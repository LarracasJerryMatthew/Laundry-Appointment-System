import sys
from PyQt6.QtCore import Qt, QRectF, QSize
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QFrame, QGridLayout
from PyQt6.QtGui import QPainter, QPen, QColor, QPalette

from pathlib import Path

class StatusDot(QWidget):
    """Small round status light (top-left). Change color with set_color()."""
    def __init__(self, color="#6fd36f", size=24):
        super().__init__()
        self._color = QColor(color)
        self.setFixedSize(size, size)

    def set_color(self, color):
        self._color = QColor(color)
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(QPen(self._color.darker(115), 2))
        p.setBrush(self._color)
        p.drawEllipse(QRectF(self.rect()).adjusted(2, 2, -2, -2))


class WasherWidget(QWidget):
    """The big circle: thick gray ring + light cyan fill."""
    def __init__(self, ring="#c8cfd8", fill="#b8f2ff", ring_width=14):
        super().__init__()
        self._ring = QColor(ring)
        self._fill = QColor(fill)
        self._w = ring_width
        self.setMinimumSize(120, 120)

    def sizeHint(self):
        return QSize(200, 200)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(QPen(self._ring, self._w))
        p.setBrush(self._fill)
        # largest centered square, inset by half the pen so the ring isn't clipped
        side = min(self.width(), self.height()) - self._w
        x = (self.width() - side) / 2
        y = (self.height() - side) / 2
        p.drawEllipse(QRectF(x, y, side, side))


class CustomerCard(QWidget):
    def __init__(self, name, data=None):
        super().__init__()

        
        # --- widgets ---
        self.status = StatusDot()
        self.status.setObjectName("statusDot")

        self.name = QLabel(name)
        font = self.name.font()
        font.setBold(True)
        font.setPointSize(14)
        self.name.setFont(font)
        self.name.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.name.setObjectName("customer_name")

        self.line = QFrame()
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Plain)
        self.line.setLineWidth(2)
        pal = self.line.palette()
        pal.setColor(QPalette.ColorRole.WindowText, QColor("#c8cfd8"))
        self.line.setPalette(pal)

        self.line.setObjectName("cardLine")

        self.washer = WasherWidget()

        # --- layout: 3 rows x 2 columns ---
        #   row 0:  [status] [        name        ]
        #   row 1:  [------------ line -----------]
        #   row 2:  [----------- washer ----------]
        customer_layout = QGridLayout()
        customer_layout.addWidget(self.status, 0, 0)
        customer_layout.addWidget(self.name, 0, 1)
        customer_layout.addWidget(self.line, 1, 0, 1, 2)
        customer_layout.addWidget(self.washer, 2, 0, 1, 2)
        customer_layout.setColumnStretch(1, 1)
        customer_layout.setRowStretch(2, 1)
        self.setLayout(customer_layout)

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Washer_qss = Path(__file__).with_name("Dashboard_style.qss")
    app.setStyleSheet(Washer_qss.read_text())
    card = CustomerCard()
    card.resize(270, 280)
    card.show()
    sys.exit(app.exec())