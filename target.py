import requests
import json


# make the http GET request to RedCircle API
def search_by_item_name(item_name):
    # set up the request parameters
    params = {
        'api_key': '474ADD0A02554F418ECFE00470CCBF92',
        'type': 'search',
        'search_term': item_name,
        'sort_by': 'best_seller'
    }

    api_result = requests.get('https://api.redcircleapi.com/request', params)
    return json.dumps(api_result.json()["search_results"][:10])


# print the JSON response from RedCircle API
# print(json.dumps(api_result.json()))

target_tools = [
    {
        "type": "function",
        "function": {
            "name": "search_by_item_name",
            "description": "Search the Target API for an item. Returns a JSON object.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_name": {
                        "type": "string",
                        "description": "The name of the item to search for."
                    }
                },
                "required": ["item_name"]
            }
        }
    }
]

target_functions = {
    "search_by_item_name": search_by_item_name,
}


def call_target_function_by_name(function_name, function_args):
    function_to_call = target_functions[function_name]

    try:
      return function_to_call(*list(function_args.values()))
    except Exception as e:
      return "Failed to call function " + function_name
