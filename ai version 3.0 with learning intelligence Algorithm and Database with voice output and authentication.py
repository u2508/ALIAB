import openai
import wikipedia
import json
import logging
from voice_recognition_module import Speech, voice
import logging.handlers
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler = logging.handlers.RotatingFileHandler('bot\\ai.log', maxBytes=1024*1024, backupCount=5)
log_handler.setFormatter(log_formatter)
root_logger = logging.getLogger()
root_logger.addHandler(log_handler)
root_logger.setLevel(logging.INFO)
#aliab
class SelfLearningAI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.load_knowledge_base()
        self.gpt3_temperature = 0.7

    def query_gpt3(self, input_text):
        openai.api_key = self.api_key
        logging.info(("chat query processing"))
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
            logging.info(("search query processing"))
            page = wikipedia.page(query).summary(3)
            return page
        except wikipedia.exceptions.DisambiguationError as e:
            # Handle disambiguation errors gracefully
            return str(e.options)

    def standby(self):
        max_attempts = 3
        logging.info(("program initialised for execution."))
        for attempt in range(1, max_attempts + 1):
            try:
                
                Speech("Standby for voice authentication system")
                Speech("Tell the voice authentication password")
                print("Standby for voice authentication system\ntell the voice authentication password")
                passwd = voice()
                keydict = {"jarvis": 1208, "arya": 1312, "gpt 4": 1909}
                if passwd in keydict:
                    Speech("Enter verification key for 2 step authentication")
                    ver = int(input("Type the unique verification key for pass: "))
                    if ver == keydict[passwd]:
                        Speech("do you want voice access or text access")
                        print('do you want voice access or text access??')
                        acc=voice()
                        if "text" in acc:
                            self.chat()
                            
                        elif "voice" in acc:
                            self.chat_voice()
                        logging.info("Speech authentication successful.")
                        break
                else:
                    Speech("Authentication failed. Please try again.")
            except Exception as e:
                logging.error(f"An error occurred during voice authentication: {str(e)}")
                Speech("An error occurred during voice authentication. Please try again.")
            if attempt < max_attempts:
                logging.info(("Authentication failed. Attempt {}/{}".format(attempt, max_attempts)))
        else:
            logging.error("Voice authentication failed after 3 attempts.")
            logging.info(("program  execution terminated."))
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
                    logging.info(("program  execution completed."))
                    break

                if user_input in self.knowledge_base:
                    Speech(self.knowledge_base[user_input])
                    
                    logging.info(("query processing completed."))
                elif user_input.startswith("tell me about "):
                    topic = user_input[14:]
                    Speech("searching on wikipedia")
                    
                    response = self.search_wikipedia(topic)
                    Speech(response)
                    logging.info(("search query processing completed."))
                    Speech("did i answer the question correctly ?")
                    user_feedback = voice().lower()
                    if user_feedback == 'no':
                        user_feedback = voice()
                        self.train(user_input, user_feedback)
                    else:
                        self.train(user_input, response)
                else:
                    response = self.query_gpt3(f"User: {user_input}\nAI:")
                    Speech(response)
                    logging.info(("chat query processing completed."))
                    user_feedback = voice().lower()
                    if user_feedback == 'no':
                        user_feedback = input("enter correct response")
                        self.train(user_input, user_feedback)
                    else:
                        self.train(user_input, response)
            except AttributeError:
                pass
            except Exception as e:
                logging.error(f"An error occurred: {str(e)}")
                Speech("An error occurred. Please try again.")
    def chat(self):
        print("ALIAB: Hello! I AM ALIAB which stands for Ai with learning intelligence Algorithm and Database. \nUtkarsh sir loved his acronyms .\nI have access to all of the internet and also having access to the gpt3 ai model.")
        while True:
            user_input = input("You: ").lower()
            if user_input == 'exit':
                print("ALIAB: Goodbye!")
                logging.info(("program  execution completed."))
                break
            if user_input in self.knowledge_base:
                print(f"ALIAB: {self.knowledge_base[user_input]}")
                logging.info(("query processing completed."))
            elif user_input.startswith("tell me about "):
                topic = user_input[14:]
                print(topic)
                response = self.search_wikipedia(topic)
                print(f"ALIAB: {response}")
                logging.info(("search query processing completed."))
                user_feedback = input("Did that answer your question? (yes/no): ").lower()
                if user_feedback == 'no':
                    user_feedback = input("What's the correct answer then? ")
                    self.train(user_input, user_feedback)
                else:
                    self.train(user_input,response)
            else:
                response = self.query_gpt3(f"User: {user_input}\nAI:")
                print(response)
                print(f"ALIAB: {response[0][0]}")
                logging.info(("chat query processing completed."))
                user_feedback = input("Did that answer your question? (yes/no): ").lower()
                if user_feedback == 'no':
                    user_feedback = input("What's the correct answer then? ")
                    self.train(user_input, user_feedback)
                else:
                    self.train(user_input,response)
    def save_knowledge_base(self):
        with open('bot\\knowledge_base.json', 'w') as file:
            json.dump(self.knowledge_base, file)

    def load_knowledge_base(self):
        try:
            with open('bot\\knowledge_base.json', 'r') as file:
                self.knowledge_base = json.load(file)
        except FileNotFoundError:
            self.knowledge_base = {}

if __name__ == "__main__":
    # Replace 'YOUR_API_KEY' with your actual GPT-3 API key
    api_key = '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'
    ai = SelfLearningAI(api_key)

    # Basic training examples
    ai.train("what's the weather like today?", "I'm not sure. You can check a weather website.")
    ai.train("tell me a joke.", "Sure! Why did the chicken cross the road? To get to the other side.")

    ai.standby()
