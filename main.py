import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QRubberBand
from PyQt5.QtCore import QRect, QPoint, QSize, Qt
from PyQt5.QtGui import QPainter, QColor, QBrush
from PIL import ImageGrab, Image
import pytesseract
import pyperclip

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ScreenshotTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Screen Capture Tool')
        self.setGeometry(100, 100, 1920, 1080)

        # 창 배경을 투명하게 설정
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()

        self.showFullScreen()

    def mousePressEvent(self, event):
        self.origin = event.pos()
        self.rubberBand.setGeometry(QRect(self.origin, QSize()))
        self.rubberBand.show()

    def mouseMoveEvent(self, event):
        self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        self.capture_area()

    def capture_area(self):
        x = self.rubberBand.geometry().x()
        y = self.rubberBand.geometry().y()
        width = self.rubberBand.geometry().width()
        height = self.rubberBand.geometry().height()
        if width > 0 and height > 0:
            self.take_screenshot(x, y, width, height)
        self.rubberBand.hide()

    def take_screenshot(self, x, y, width, height):
        try:
            screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            screenshot.save('screenshot.png')
            text = self.extract_text_from_image('screenshot.png')
            print('Extracted Text:', text)
            pyperclip.copy(text)
            self.close()
        except Exception as e:
            print(f"Error capturing screenshot: {e}")

    def extract_text_from_image(self, image_path):
        try:
            image = Image.open(image_path)
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(image, lang='eng+kor', config=custom_config)
            return self.post_process_text(text)
        except Exception as e:
            print(f"Error extracting text from image: {e}")
            return ""

    def post_process_text(self, text):
        # 후처리: 너무 많은 띄어쓰기를 수정하는 간단한 예제
        processed_text = ' '.join(text.split())
        return processed_text

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(255, 255, 255, 10))  # 노란색 반투명 배경
        painter.drawRect(self.rect())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ScreenshotTool()
    sys.exit(app.exec_())