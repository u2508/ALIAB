import openai
import wikipedia
import json
from voice_recognition_module import Speech, voice

#aliab
class SelfLearningAI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.load_knowledge_base()
        self.gpt3_temperature = 0.7
        self.ai_call_thread = threading.Thread(target=self.chat_voice)

    def query_gpt3(self, input_text):
        openai.api_key = self.api_key
        response = openai.Completion.create(
            engine="davinci",
            prompt=input_text,
            max_tokens=50,  # Adjust based on desired response length
            temperature=self.gpt3_temperature
        )

        return response.choices[0].text.strip()

    def train(self, user_input, user_feedback):
        self.knowledge_base[user_input] = user_feedback
        self.save_knowledge_base()

    def search_wikipedia(self, query):
        try:
            page = wikipedia.page(query).summary(3)
            return page
        except wikipedia.exceptions.DisambiguationError as e:
            # Handle disambiguation errors gracefully
            self.query_gpt3(query)
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
            if attempt < max_attempts:
                pass
        else:
            Speech("Voice authentication failed after 3 attempts. Exiting.")

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
                    break

                if user_input in self.knowledge_base:
                    Speech(self.knowledge_base[user_input])
                    print(self.knowledge_base[user_input])
                elif user_input.startswith("tell me about "):
                    topic = user_input[14:]
                    Speech("searching on wikipedia")

                    response = self.search_wikipedia(topic)
                    Speech(response)
                    print("ALIAB: ",response)
                    Speech("did i answer the question correctly ?")
                    user_feedback = voice().lower()
                    if user_feedback == 'no':
                        Speech("enter correct response")
                        user_feedback = input("enter correct response")
                        self.train(user_input, user_feedback)
                    else:
                        self.train(user_input, response)
                else:
                    response = self.query_gpt3(f"User: {user_input}\nAI:")
                    Speech(response)
                    print("ALIAB: ",response)
                    user_feedback = voice().lower()
                    if user_feedback == 'no':
                        Speech("enter correct response")
                        user_feedback = input("enter correct response")
                        self.train(user_input, user_feedback)
                    else:
                        self.train(user_input, response)
            except AttributeError:
                pass
            except Exception as e:
                Speech("An error occurred. Please try again.")
        else:
            self.ai_call_thread.join()
        
    def save_knowledge_base(self):
        with open('bot\\knowledge_base.json', 'w') as file:
            json.dump(self.knowledge_base, file)
    
    def load_knowledge_base(self):
        try:
            with open('bot\\knowledge_base.json', 'r') as file:
                self.knowledge_base = json.load(file)
        except FileNotFoundError:
            self.knowledge_base = {}

if __name__:
    # Replace 'YOUR_API_KEY' with your actual GPT-3 API key
    api_key = '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'
    ai = SelfLearningAI(api_key)
    