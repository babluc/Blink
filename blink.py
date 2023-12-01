#!/usr/local/bin/python3
# Requires: pip install pyqt5
import sys
import signal
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSizePolicy
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush
from PyQt5.QtCore import QTimer, Qt

OLIVE_GREEN = QColor(107, 142, 35)
DARK_OLIVE_GREEN = QColor(85, 107, 47)
LIGHT_GRAY = QColor(211, 211, 211)

class BlinkingCircleApp(QWidget):
    def __init__(self, 
                 window_height=100, 
                 window_width=100, 
                 background_color=Qt.white, 
                 circle_color=DARK_OLIVE_GREEN, 
                 slowdown_period=600_000):
        super().__init__()
        self.window_height = window_height
        self.window_width = window_width
        self.background_color = background_color
        self.slowdown_period = slowdown_period
        self.circle_color = circle_color
        self.setMouseTracking(False)
        self.initUI()

        
    def initUI(self):
        self.setWindowTitle('Blinking Circle')
        self.setGeometry(300, 300, self.window_width , self.window_height)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.label = QLabel(self)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.pixmap = QPixmap(self.window_width , self.window_height)
        self.pixmap.fill(self.background_color)
        self.label.setPixmap(self.pixmap)
        self.visible = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.blink_circle)
        self.timer_interval = 250
        self.timer.start(self.timer_interval)
        self.time_elapsed = 0
        self.time_limit = self.slowdown_period 
        self.show()

    def resizeEvent(self, event):
        size = event.size()
        side = (min(size.width(), size.height()))
        self.resize (side, side)
        self.pixmap = QPixmap(self.width(), self.height())
        self.pixmap.fill(self.background_color)
        self.label.setPixmap(self.pixmap)
        self.label.resize(self.width(), self.height())
        self.blink_circle()

    def blink_circle(self):
        painter = QPainter(self.pixmap)
        diameter = int(min(self.width(), self.height()))
        top_left = 0,0
        if self.visible:
            painter.setBrush(QBrush(self.background_color, Qt.SolidPattern))
        else:
            painter.setBrush(QBrush(self.circle_color, Qt.SolidPattern))
        painter.drawEllipse(*top_left, diameter, diameter)
        self.label.setPixmap(self.pixmap)
        self.visible = not self.visible
        self.time_elapsed += self.timer_interval

        # Calculate the new interval as a linear interpolation between 250 and 500
        progress = min(self.time_elapsed / self.time_limit, 1)
        self.timer_interval = int(250 + progress * (500 - 250))

        # Set the new interval
        self.timer.setInterval(self.timer_interval)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BlinkingCircleApp(background_color=LIGHT_GRAY)
    signal.signal(signal.SIGINT, lambda *args: app.quit())
    sys.exit(app.exec_())
