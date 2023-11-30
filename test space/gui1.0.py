import sys
import time
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton

class VoiceBotGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.voice_bot = VoiceBot()

        self.setWindowTitle("Voice Bot GUI")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.init_ui()

    def init_ui(self):
        self.central_widget.setStyleSheet("background-color: black;")

        self.feedback_label = QLabel("Click 'Start' to begin voice interaction", self)
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setFont(QFont("Helvetica", 24))
        self.feedback_label.setStyleSheet("color: white;")
        self.feedback_label.setGeometry(100, 100, 600, 100)

        self.indicator = QLabel(self)
        self.indicator.setGeometry(350, 250, 100, 100)
        self.indicator.setStyleSheet("background-color: black; border-radius: 50px;")

        self.start_button = QPushButton("Start", self)
        self.start_button.setGeometry(250, 400, 100, 50)
        self.start_button.setFont(QFont("Helvetica", 16))
        self.start_button.setStyleSheet("background-color: green; color: white; border: none;")
        self.start_button.clicked.connect(self.start_voice_interaction)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setGeometry(450, 400, 100, 50)
        self.stop_button.setFont(QFont("Helvetica", 16))
        self.stop_button.setStyleSheet("background-color: red; color: white; border: none;")
        self.stop_button.setDisabled(True)
        self.stop_button.clicked.connect(self.stop_voice_interaction)

    def start_voice_interaction(self):
        if not self.voice_bot.is_listening:
            self.voice_bot.start_listening()
            self.update_feedback("Listening... Speak now")
            self.start_button.setDisabled(True)
            self.stop_button.setEnabled(True)
            self.update_indicator("green")

    def stop_voice_interaction(self):
        if self.voice_bot.is_listening:
            self.voice_bot.stop_listening()
            self.update_feedback("Voice interaction stopped")
            self.start_button.setEnabled(True)
            self.stop_button.setDisabled(True)
            self.update_indicator("red")

    def update_feedback(self, message):
        self.feedback_label.setText(message)

    def update_indicator(self, color):
        self.indicator.setStyleSheet(f"background-color: {color}; border-radius: 50px;")

class VoiceBot:
    def __init__(self):
        self.is_listening = False

    def start_listening(self):
        if not self.is_listening:
            self.is_listening = True

    def stop_listening(self):
        if self.is_listening:
            self.is_listening = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VoiceBotGUI()
    window.show()
    sys.exit(app.exec_())
