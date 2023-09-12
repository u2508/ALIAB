import openai
import wikipedia
import json
#ALIAB
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
            max_tokens=50,  # Adjust based on desired response length
            temperature=self.gpt3_temperature
        )

        return response.choices[0].text.strip()

    def train(self, user_input, user_feedback):
        self.knowledge_base[user_input] = user_feedback
        self.save_knowledge_base()

    def search_wikipedia(self, query):
        page = wikipedia.page(query).summary
        #if page.exists():
        return page
        #else:
        #    return "I couldn't find information on that topic in Wikipedia."

    def chat(self):
        print("ALIAB: Hello! I AM ALIAB. ")
        while True:
            user_input = input("You: ").lower()
            if user_input == 'exit':
                print("ALIAB: Goodbye!")
                break
            if user_input in self.knowledge_base:
                print(f"ALIAB: {self.knowledge_base[user_input]}")
            elif user_input.startswith("tell me about "):
                topic = user_input[14:]
                print(topic)
                response = self.search_wikipedia(topic)
                print(f"ALIAB: {response}")
                user_feedback = input("Did that answer your question? (yes/no): ").lower()
                if user_feedback == 'no':
                    user_feedback = input("What's the correct answer then? ")
                    self.train(user_input, user_feedback)
                else:
                    self.train(user_input,response)
            else:
                response = self.query_gpt3(f"User: {user_input}\nAI:")
                print(f"ALIAB: {response}")
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
    
    ai.chat()
