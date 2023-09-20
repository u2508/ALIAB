import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import *
from ai_version_6_ALIAB_backend import VoiceInteractionHandler
api = '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'
class SettingsDialog(QDialog):
    def __init__(self, ai):
        super().__init__()
        self.ai = ai
        self.setWindowTitle("Settings")
        self.setGeometry(300, 300, 400, 200)
        self.init_ui()
        

    def init_ui(self):
        layout = QVBoxLayout()

        # Label and input field for adjusting temperature
        temperature_label = QLabel("AI Temperature:")
        self.temperature_input = QLineEdit()
        self.temperature_input.setText(str(self.ai.gpt3_temperature))

        # Slider for adjusting temperature
        temperature_slider = QSlider(Qt.Horizontal)
        temperature_slider.setMinimum(0)
        temperature_slider.setMaximum(100)
        temperature_slider.setValue(int(self.ai.gpt3_temperature * 100))
        temperature_slider.valueChanged.connect(self.update_temperature_input)

        # Save button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)

        layout.addWidget(temperature_label)
        layout.addWidget(self.temperature_input)
        layout.addWidget(temperature_slider)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def update_temperature_input(self, value):
        # Update the temperature input field when the slider value changes
        self.temperature_input.setText(str(value / 100.0))

    def save_settings(self):
        # Save the settings when the "Save" button is clicked
        try:
            new_temperature = float(self.temperature_input.text())
            if 0.0 <= new_temperature <= 1.0:
                self.ai.gpt3_temperature = new_temperature
                self.close()
            else:
                QMessageBox.warning(self, "Invalid Input", "Temperature must be between 0.0 and 1.0")
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Invalid temperature value")




class VoiceBotGUI(QMainWindow):
    def __init__(self, voice):
        super().__init__()
        self.setWindowTitle("Voice Bot GUI")
        self.interaction_history = ['\n',]
        self.init_ui()
        self.voice_handler=voice
    def init_ui(self):
        label = QLabel(self)
        pixmap_bg = QPixmap("C:\\Users\\utkar\\OneDrive\\vscode\\bot\\ai_bg.jpg")
        label.setPixmap(pixmap_bg)
        self.setCentralWidget(label)
        self.feedback_label = QLabel("Click 'Start' to begin voice interaction", self)
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setFont(QFont("Helvetica", 24))
        self.feedback_label.setStyleSheet("color: white;")
        self.feedback_label.setGeometry(312, 0, 600, 100)
        self.resize(pixmap_bg.width(), pixmap_bg.height())
        self.indicator = QLabel(self)
        self.indicator.setGeometry(475, 160, 250, 250)
        pixmap_mic0 = QPixmap("C:/Users/utkar/OneDrive/vscode/bot/mic00.png")
        self.indicator.setStyleSheet("background-color:white ; border-radius: 120px;")
        self.indicator.setPixmap(pixmap_mic0)
        self.start_button = QPushButton("Start", self)
        self.start_button.setGeometry(400, 450, 150, 80)
        self.start_button.setFont(QFont("Helvetica", 32))
        self.start_button.setStyleSheet("background-color: green; color: white; border: none;")
        self.start_button.clicked.connect(self.start_voice_interaction)
        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setGeometry(700, 450, 150, 80)
        self.stop_button.setFont(QFont("Helvetica", 32))
        self.stop_button.setStyleSheet("background-color: red; color: white; border: none;")
        self.stop_button.setDisabled(True)
        self.stop_button.clicked.connect(self.stop_voice_interaction)
        # Create a text area for interaction history
        self.history_text = QTextEdit(self)
        self.history_text.setGeometry(890, 50, 300, 500)
        self.history_text.setFont(QFont("Helvetica", 14))
        self.history_text.setReadOnly(True)
        self.history_text.setStyleSheet("background-color: rgba(0,0,0, 208);")
        self.history=QLabel("history".upper(), self)
        self.history.setAlignment(Qt.AlignCenter)
        self.history.setFont(QFont("Helvetica", 24))
        self.history.setStyleSheet("color: red;")
        self.history.setGeometry(890, 40, 300, 100)
        history_text = "\n".join(self.interaction_history)
        self.history_text.setPlainText(history_text)
        settings_frame = QFrame(self)
        settings_frame.setGeometry(20, 40, 300, 500)
        settings_frame.setStyleSheet("background-color: rgba(0, 0, 0, 208);")
        self.options=QLabel("options".upper(), settings_frame)
        self.options.setAlignment(Qt.AlignCenter)
        self.options.setFont(QFont("Helvetica", 24))
        self.options.setStyleSheet("color: red;background-color: rgba(0, 0, 0, 00);")
        self.options.setGeometry(0, 6, 300, 80)
        # Create a settings button
        self.settings_button = QPushButton("Settings",settings_frame)
        self.settings_button.setGeometry(30, 120, 240, 80)
        self.settings_button.setFont(QFont("Helvetica", 32))
        self.settings_button.setStyleSheet("background-color: orange; color: white; border: none;")
        self.settings_button.clicked.connect(self.open_settings)
        exit_button = QPushButton("Exit", settings_frame)
        exit_button.setGeometry(30, 300, 240, 80)
        exit_button.setFont(QFont("Helvetica", 32))
        exit_button.setStyleSheet("background-color: Orchid; color: white; border: none;")
        exit_button.clicked.connect(self.on_exit_button_click)

    def open_settings(self):
        settings_dialog = SettingsDialog(self.ai)
        settings_dialog.exec_()
    def on_exit_button_click(self):
        self.stop_voice_interaction()
        exit()
    def start_voice_interaction(self):
        if not self.voice_handler.is_listening:
            
            self.update_feedback("Listening... Speak now")
            self.start_button.setDisabled(True)
            self.stop_button.setEnabled(True)
            self.update_indicator("C:/Users/utkar/OneDrive/vscode/bot/mic01.png")
            try:
                global count
                print(count)
                self.voice_handler.start_listening(count)
            except NameError:
                self.voice_handler.start_listening(0)
                print(0)
            
            

    def stop_voice_interaction(self):
        if self.voice_handler.is_listening:
            self.update_feedback("Voice interaction stopped")
            self.start_button.setEnabled(True)
            self.stop_button.setDisabled(True)
            self.update_indicator("C:/Users/utkar/OneDrive/vscode/bot/mic02.png")
            global count
            count=self.voice_handler.stop_listening()

    def update_feedback(self, message):
        self.feedback_label.setText(message)

    def update_indicator(self, pixpath):
        self.indicator.setPixmap(QPixmap(pixpath))

def voice_interaction():
        global count
        count=0
        app = QApplication(sys.argv)
        window = VoiceBotGUI(VoiceInteractionHandler(api))
        window.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    voice_interaction()  