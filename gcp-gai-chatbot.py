import os
os.getcwd()
p = 'c:\\Users\\jainp\\Downloads\\'
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='C:\\work\\projects\\GCP-GAI\\doc\\gai87546-4b61133715b1.json'

from vertexai.language_models import ChatModel
model_name = 'chat-bison'
model = ChatModel.from_pretrained(model_name)
context = '''You are customer support bot in charge of return policy.
Items can be returned if item was purchased within the last 30 days and unused.
Ask the customer follow-up questions to determine if their item can be returned or not.
Make sure to confirm that item is both unused and has been purchased in the last 30 days.
'''
chat = model.start_chat(context=context)

input_text = ''
print("Hi! Welcome to our return customer support bot")
print("To end the chat type 'end'")
while input_text.lower() != 'end':
    input_text = input()
    response = chat.send_message(input_text)
    print(response.text)
print("Thank you, have a nice day.")