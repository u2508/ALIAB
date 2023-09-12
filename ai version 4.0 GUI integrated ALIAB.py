import sys
import multiprocessing
import json
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import *
import openai
import wikipedia
from voice_recognition_module import Speech, voice
import logging

api_key = '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'
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
logging.basicConfig(filename='bot/ai.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

class SelfLearningAI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.load_knowledge_base()
        self.gpt3_temperature = 0.7

    def query_gpt3(self, input_text):
        openai.api_key = self.api_key
        response = openai.Completion.create(
            engine="davinci",
            prompt=input_text,
            max_tokens=50,
            temperature=self.gpt3_temperature
        )
        return response.choices[0].text.strip()

    def train(self, user_input, user_feedback):
        self.knowledge_base[user_input] = user_feedback
        self.save_knowledge_base()

    def search_wikipedia(self, query):
        try:
            page = wikipedia.page(query).summary(3)
            print(page)
            return page
        except wikipedia.exceptions.DisambiguationError:
            return None

    def standby(self):
        max_attempts = 3
        for attempt in range(1, max_attempts + 1):
            try:
                Speech("Standby for voice authentication system")
                Speech("Tell the voice authentication password")
                print("Standby for voice authentication system\ntell the voice authentication password")
                passwd = voice()
                keydict = {"jarvis": 1208, "arya": 1312, "gpt 4": 1909}
                if passwd in keydict:
                    self.chat_voice()
                else:
                    Speech("Authentication failed. Please try again.")
            except Exception as e:
                Speech("An error occurred during voice authentication. Please try again.")
                print(e)
            if attempt < max_attempts:
                pass
        else:
            Speech("Voice authentication failed after 3 attempts. Exiting.")
            window.stop_voice_interaction()
    def chat_voice(self):
        Speech("Hello! I AM ALIAB which stands for Ai with learning intelligence Algorithm and Database. \nUtkarsh sir loved his acronyms")
        Speech("I have access to all of the internet and also having access to the gpt3 ai model.")
        while True:
            try:
                Speech("what can i do for you today")
                user_input = voice().lower()
                print("You: " + user_input)
                if user_input == 'exit':
                    Speech("Goodbye!")
                    print("ALIAB: Goodbye!")
                    window.log_interaction(user_input, response)
                    break

                if user_input in self.knowledge_base:
                    Speech(self.knowledge_base[user_input])
                    print(self.knowledge_base[user_input])
                    window.log_interaction(user_input, response)
                else:
                    response = self.query_gpt3(f"User: {user_input}\nAI:")
                    Speech(response)
                    print("ALIAB: ", response)
                    user_feedback = voice().lower()
                    if user_feedback == 'no':
                        Speech("enter correct response")
                        user_feedback = input("enter correct response")
                        self.train(user_input, user_feedback)
                        response=user_feedback
                    else:
                        self.train(user_input, response)
                    window.log_interaction(user_input, response)
            except Exception as e:
                Speech("An error occurred. Please try again.")
        else:
            window.stop_voice_interaction()
    def chat_stop(self):
        self.ai_call_thread.join()
    def save_knowledge_base(self):
        with open('knowledge_base.json', 'w') as file:
            json.dump(self.knowledge_base, file)

    def load_knowledge_base(self):
        try:
            with open('knowledge_base.json', 'r') as file:
                self.knowledge_base = json.load(file)
        except FileNotFoundError:
            self.knowledge_base = {}


class VoiceBotGUI(QMainWindow):
    def __init__(self, ai):
        super().__init__()
        self.voice_bot = VoiceBot(ai)
        self.setWindowTitle("Voice Bot GUI")
        self.interaction_history = ['\n',]
        self.init_ui()
    def log_interaction(self, user_input, ai_response):
        # Log user input and AI response in the history list
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp}\nUser: {user_input}\nAI: {ai_response}\n\n"
        self.interaction_history.append(log_entry)

        # Update the history text area with the complete history
        history_text = "".join(self.interaction_history)
        self.history_text.setPlainText(history_text)
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
        settings_dialog = SettingsDialog(ai)
        settings_dialog.exec_()
    def on_exit_button_click(self):
        exit()
    def start_voice_interaction(self):
        if not self.voice_bot.is_listening:
            self.voice_bot.start_listening()
            self.update_feedback("Listening... Speak now")
            self.start_button.setDisabled(True)
            self.stop_button.setEnabled(True)
            self.update_indicator("C:/Users/utkar/OneDrive/vscode/bot/mic01.png")

    def stop_voice_interaction(self):
        if self.voice_bot.is_listening:
            self.update_feedback("Voice interaction stopped")
            self.start_button.setEnabled(True)
            self.stop_button.setDisabled(True)
            self.update_indicator("C:/Users/utkar/OneDrive/vscode/bot/mic02.png")
            self.voice_bot.stop_listening()

    def update_feedback(self, message):
        self.feedback_label.setText(message)

    def update_indicator(self, pixpath):
        self.indicator.setPixmap(QPixmap(pixpath))

def voice_interaction():
    ai = SelfLearningAI(api_key)
    app = QApplication(sys.argv)
    voice_bot = VoiceBot(ai)
    window = VoiceBotGUI(ai)
    window.show()
    sys.exit(app.exec_())

class VoiceBot:
    def __init__(self, ai):
        self.is_listening = False
        self.ai = ai

    def start_listening(self):
        if not self.is_listening:
            self.is_listening = True
            self.callback_process = multiprocessing.Process(target=self.ai.standby)
            self.callback_process.start()

    def stop_listening(self):
        if self.is_listening:
            self.is_listening = False
            self.callback_process.terminate()  # Terminate the process
if __name__ == "__main__":
    logging.basicConfig(filename='bot\\ai.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
    

    # Start voice interaction in a separate process
    voice_process = multiprocessing.Process(target=voice_interaction)
    voice_process.start()
    voice_process.join()  
    # Wait for the voice interaction process to finish