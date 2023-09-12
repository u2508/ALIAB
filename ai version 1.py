from transformers import pipeline, GPT2LMHeadModel, GPT2Tokenizer
class EnhancedChatbot:
    def __init__(self, model_name, dataset_file):
        self.text_generator = pipeline('text-generation', model=model_name, tokenizer=GPT2Tokenizer.from_pretrained(model_name))
        self.dataset = self.load_dataset(dataset_file)
        self.user_feedback = {}

    def load_dataset(self, dataset_file):
        with open(dataset_file, 'r',encoding='utf-8') as file:
            dataset = [line.strip().split('|') for line in file.readlines()]
        return dataset

    def generate_response(self, user_input):
        response = self.text_generator(f"User: {user_input}\nChatbot:", max_length=500, num_return_sequences=1, temperature=0.7)
        #exit(print(response))
        return response[0]['generated_text'].replace("User:", "").strip()


    def learn_from_user(self, user_input, user_feedback):
        self.user_feedback[user_input] = user_feedback

    def chat(self):
        print("Chatbot: Hello! How can I assist you?")
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                print("Chatbot: Goodbye!")
                break

            if user_input in self.user_feedback:
                print(f"Chatbot: {self.user_feedback[user_input]}")
            else:
                speech_response = self.generate_response(user_input)
                print("Chatbot:")
                print(speech_response)
                user_feedback = input("Did that answer your question? (yes/no): ").lower()
                if user_feedback == 'no':
                    user_feedback = input("What's the correct answer then? ")
                    self.learn_from_user(user_input, user_feedback)

if __name__ == "__main__":
    # You can replace 't5-small' with other SpeechT5 model variants if needed
    model_name = "gpt2"
    dataset_file = "dataset.txt"
    chatbot = EnhancedChatbot(model_name, dataset_file)
    chatbot.chat()
