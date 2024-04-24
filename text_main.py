from shoprite import shoprite_tools
from chat import messages, chat_completion_request

while True:
    text = input("$")
    completion = chat_completion_request(messages, tools=shoprite_tools)
    print(completion.content)

