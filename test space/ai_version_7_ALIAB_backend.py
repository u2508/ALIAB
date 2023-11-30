import multiprocessing
import pyrebase,json
import openai
import wikipedia as wk
from voice_recognition_module import Speech, voice
import requests
from requests.exceptions import HTTPError, RequestException

class VoiceInteractionHandler:
    def __init__(self, api):
        self.is_listening = False
        self.count=0
        self.api_key = api
        self.gpt3_temperature = 0.7
        self.firebase_config = {
            "apiKey": "AIzaSyCsM6DAGXAZTyE1Haml-qV54r4y9_EPVl0",
            "authDomain": "aliab-be691.firebaseapp.com",
            "databaseURL": "https://console.firebase.google.com/u/0/project/aliab-be691/database/aliab-be691-default-rtdb/data/~2F",
            "projectId": "aliab-be691",
            "storageBucket": "aliab-be691.appspot.com",
            "messagingSenderId": "49413450121",
            "appId": "1:49413450121:web:fe951b137e75c66209d958",
        }
        self.initialise()
        self.save_knowledge_base()
        
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
            wk.set_lang("en")
            page = wk.page(query)
            if page.pageid!='':
                return page.summary
        except wk.exceptions.DisambiguationError as e:
            return 'disambiguity error'
    def save_knowledge_base(self):
        try:
            firebase = pyrebase.initialize_app(self.firebase_config)
            db = firebase.database()
            print(self.knowledge_base)
            response = db.child("knowledge_base").set(self.knowledge_base)
            print("Response content:", response.content)
            # Check for HTTP errors
            response.raise_for_status()

            print("Knowledge base saved successfully.")
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            print(f"Response content: {response.content}")
        except RequestException as req_err:
            print(f"Request exception occurred: {req_err}")
        except Exception as e:
            print(f"Error saving knowledge base: {e}")

    def load_knowledge_base(self):
        try:
            firebase = pyrebase.initialize_app(self.firebase_config)
            db = firebase.database()
            knowledge_base = db.child("knowledge_base").get().val()
            if knowledge_base:
                self.knowledge_base = knowledge_base
        except Exception as e:
            print(f"Error loading knowledge base: {e}")
    def start_listening(self,count):
        
        if not self.is_listening:
            self.is_listening = True
            self.callback_process = multiprocessing.Process(target=self.listen)
            
            self.callback_process.start()
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
                    self.count += 1                    
                    self.listen()
                else:
                    Speech("Authentication failed. Please try again.")
            except Exception as e:
                Speech("An error occurred during voice authentication. Please try again.")
                print(e)
            if attempt < max_attempts:
                pass
        else:
            Speech("Voice authentication failed after 3 attempts. Exiting.")
            self.exit()
            
    def listen(self):
        Speech("Hello! I AM ALIAB which stands for Ai with learning intelligence Algorithm and Database.")
        Speech("I have access to all of the internet and also having access to the gpt3 ai model.")
        while True:
            try:
                Speech("what can i do for you today")
                user_input = voice().lower()
                print("You: " + user_input)
                if 'exit' in user_input:
                    self.exit()

                if user_input in self.knowledge_base:
                    Speech(self.knowledge_base[user_input])
                    print("ALIAB: ", self.knowledge_base[user_input])
                elif user_input.startswith("tell me about "):
                    topic = user_input.re
                    Speech("searching on wikipedia")

                    response = self.search_wikipedia(topic)
                    Speech(response)
                    print("ALIAB: ", response)
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
                    print("ALIAB: ", response)
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
                Speech(e)
    
    def stop_listening(self):
        self.is_listening = False
        self.callback_process.terminate()
        
    def exit(self):
        self.stop_listening()
        exit(Speech('goodbye'))
    def initialise(self):
        with open(r'knowledge_base.json', 'r') as file:
            self.knowledge_base = json.load(file)
        