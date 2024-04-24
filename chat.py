from openai import OpenAI
from dotenv import load_dotenv
import os
from tenacity import retry, wait_random_exponential, stop_after_attempt
from shoprite import call_shoprite_function_by_name
from target import call_target_function_by_name
from termcolor import colored
import json

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

GPT_MODEL = "gpt-3.5-turbo"

prompt: str = '''
You are a voice activated digital assistant for ordering groceries from ShopRite.
If there is ambiguity about which item a user wants, ask clarifying questions.
Do not ask follow up questions after calling a function.

After adding an item, if the user clarifies and says they meant a different item, remove the original item and add the new one.

The abbreviation 'oz' should be replaced with 'ounces'.
'''

messages = [{"role": "system", "content": prompt}]


@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        response_message = response.choices[0].message
        messages.append(response_message)

        if response_message.tool_calls:
            for tool_call in response_message.tool_calls:
                # Which function call was invoked
                function_name = tool_call.function.name

                # Extracting the arguments
                function_args = json.loads(tool_call.function.arguments)

                # function_response = call_shoprite_function_by_name(function_name, function_args)
                function_response = call_target_function_by_name(function_name, function_args)

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": function_response
                    }
                )
            response_after_calls = client.chat.completions.create(
                model=model,
                messages=messages
            )
            print(response_after_calls)
            messages.append(response_after_calls.choices[0].message)
            response_message = response_after_calls.choices[0].message

        return response_message
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e


def pretty_print_conversation(messages):
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "function": "magenta",
    }

    for message in messages:
        try:
            role = message.role

            if role == "system":
                print(colored(f"system: {message.content}\n", role_to_color[role]))
            elif role == "user":
                print(colored(f"user: {message.content}\n", role_to_color[role]))
            elif role == "assistant" and message.function_call:
                print(colored(f"assistant: {message.function_call}\n", role_to_color[role]))
            elif role == "assistant" and not message.function_call:
                print(colored(f"assistant: {message.content}\n", role_to_color[role]))
            elif role == "function":
                print(colored(f"function ({message.name}): {message.content}\n", role_to_color[role]))
        except:
            role = message["role"]
            if role == "system":
                print(colored(f"system: {message['content']}\n", role_to_color[role]))
            elif role == "user":
                print(colored(f"user: {message['content']}\n", role_to_color[role]))
            elif role == "assistant" and message.get("function_call"):
                print(colored(f"assistant: {message['function_call']}\n", role_to_color[role]))
            elif role == "assistant" and not message.get("function_call"):
                print(colored(f"assistant: {message['content']}\n", role_to_color[role]))
            elif role == "function":
                print(colored(f"function ({message['name']}): {message['content']}\n", role_to_color[role]))

# messages.append({"role": "user", "content": "Add blueberries to my ShopRite cart"})
# chat_response = chat_completion_request(
#     messages, tools=shoprite_tools
# )
# pretty_print_conversation(messages)
