import re
import json
import requests
from tkinter import *
import os
from PIL import Image, ImageTk

class BankingChatbot:
    def __init__(self):
        # Load the knowledge base
        # Specify the file path using a raw string
        knowledge_base_path = r"C:\Users\Anshit\Desktop\knowledge_base.json"

# Load the knowledge base
        with open(knowledge_base_path, "r") as file:
            knowledge_base = json.load(file)

# Load the knowledge base
        self.knowledge_base = json.load(open(knowledge_base_path))
    

        # Initialize the feedback system
        self.feedback_system = FeedbackSystem()

        # Create the GUI
        self.create_gui()

    def create_gui(self):
        self.window = Tk()
        self.window.title("Banking Chatbot")

        # Create and configure the chat window
        self.chat_window = Text(self.window, height=20, width=50)
        self.chat_window.configure(state='disabled')
        self.chat_window.grid(row=0, column=0, padx=10, pady=10, sticky="W")

        # Create the input field
        self.input_field = Entry(self.window, width=50)
        self.input_field.bind("<Return>", self.handle_question)
        self.input_field.grid(row=1, column=0, padx=10, pady=10, sticky="W")

        # Create the send button
        self.send_button = Button(self.window, text="Send", command=self.handle_question)
        self.send_button.grid(row=1, column=1, padx=10, pady=10, sticky="E")

        # Load and display the chatbot image
        self.chatbot_image = Image.open("chatbot_image.png")
        self.chatbot_image = self.chatbot_image.resize((150, 150), Image.ANTIALIAS)
        self.chatbot_photo = ImageTk.PhotoImage(self.chatbot_image)
        self.chatbot_image_label = Label(image=self.chatbot_photo)
        self.chatbot_image_label.grid(row=0, column=1, rowspan=2, padx=10, pady=10)

    def handle_question(self, event=None):
        # Get the user's question
        question = self.input_field.get()
        self.input_field.delete(0, 'end')

        # Preprocess the question
        question = question.lower()
        question = re.sub(r"[^\w\s]", "", question)

        # If the question is about a specific bank account, try to identify the account type
        if re.search(r"(checking|savings|money market|credit|debit) account", question):
            account_type = re.search(r"(checking|savings|money market|credit|debit) account", question).group(1)

            # If the account type is identified, use that information to generate a more specific response
            if account_type is not None:
                answer = self.knowledge_base.get(account_type + " account")

                if answer is not None:
                    self.display_message(answer)
                    return

        # If the answer is not found in the knowledge base, use AI to generate a response
        answer = self.feedback_system.generate_response(question)
        self.display_message(answer)

    def display_message(self, message):
        self.chat_window.configure(state='normal')
        self.chat_window.insert(END, "Chatbot: " + message + "\n")
        self.chat_window.configure(state='disabled')
        self.chat_window.see(END)

    def run(self):
        self.window.mainloop()

class FeedbackSystem:
    def __init__(self):
        # Initialize the feedback database
        self.feedback_database = []

    def generate_response(self, question):
        # Use a large language model (LLM) to generate a response
        response = requests.post("https://api.openai.com/v1/engines/davinci/completions",
                                headers={
                                    "Authorization": "Bearer YOUR_API_KEY"
                                },
                                json={"prompt": question})
        response = json.loads(response.content)["choices"][0]["text"]

        return response

    def process_feedback(self, feedback):
        # Add the feedback to the database
        self.feedback_database.append(feedback)

        # Extract the account type from the feedback, if possible
        account_type = re.search(r"(checking|savings|money market|credit|debit) account", feedback).group(1)

        # If the account type is extracted, use that information to fine-tune the LLM
        if account_type is not None:
            requests.post("https://api.openai.com/v1/engines/davinci/fine-tune",
                           headers={
                               "Authorization": "Bearer YOUR_API_KEY"
                           },
                           files={"data": json.dumps([{"prompt": feedback, "label": account_type}])})

# Add the following questions and answers to the knowledge base
knowledge_base = {
    "what is a bank account?": "A bank account is a place to store your money safely. It allows you to deposit and withdraw money, and to write checks and make payments.",
    "what are the different types of bank accounts?": "Thereare many different types of bank accounts, including checking accounts, savings accounts, and money market accounts. Each type of account has its own advantages and disadvantages.",
    "how do I open a bank account?": "To open a bank account, you will need to provide some basic information, such as your name, address, and Social Security number. You may also need to make a deposit.",
    "what are the benefits of having a bank account?": "There are many benefits to having a bank account, including: * You can keep your money safe. \n * You can easily access your money when you need it.\n * You can earn interest on your savings.\n* You can make and receive payments easily.\n* You can build your credit history.",
    "what is the difference between a checking account and a savings account?": "A checking account is designed for everyday transactions, such as writing checks and making payments. A savings account is designed for saving money and earning interest.",
    "what is a debit card?": "A debit card is a type of payment card that is linked to your checking account. When you use a debit card to make a purchase, the money is deducted from your checking account immediately.",
    "what is a credit card?": "A credit card is a type of payment card that allows you to borrow money from the bank to make purchases. You can then repay the money to the bank over time, with interest.",
    "what is an ATM?": "An ATM stands for automated teller machine. It is a machine that allows you to deposit and withdraw money from your bank account without having to visit a bank branch.",
    "what is a check?": "A check is a written order to your bank to pay a certain amount of money to a person or company. Checks are used to make payments for goods and services, and to transfer money between bank accounts.",
    "what is online banking?": "Online banking is a service that allows you to access your bank account and manage your finances online. You can use online banking to deposit and withdraw money, transfer money, pay bills, and view your account statements.",
}
chatbot = BankingChatbot()

chatbot.run()