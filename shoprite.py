import requests
import json
from requests.auth import HTTPBasicAuth 

bearer_token = "C1B5CE442E850082D9909E18ADD5F546E72DE8C46DABB7BE810B3B5F83504736"

# def get_new_token():
#   auth_server_url = "https://sts.shoprite.com/connect/token"  
#   payload = 'refresh_token=36B7EDEBD930FAEC64765D00510580D6D2B227FA336ABE22397C3557282A3ABB&grant_type=refresh_token&client_id=mwg.ecm.storefrontui&client_secret=secret'
#   headers = {
#     'authority': 'sts.shoprite.com',
#     'accept': '*/*',
#     'accept-language': 'en-US,en;q=0.9',
#     'content-type': 'application/x-www-form-urlencoded',
#     'origin': 'https://www.shoprite.com',
#     'referer': 'https://www.shoprite.com/',
#     'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"macOS"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-site',
#     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
#   }

shoprite_tools = [
  {
    "type": "function",
    "function": {
      "name": "get_item_by_name",
      "description": "Get information about a grocery item by its name.",
      "parameters": {
        "type": "object",
        "properties": {
          "item_name": {
            "type": "string",
            "description": "The name of the item to retrieve information for."
          }
        },
        "required": ["item_name"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "add_item_to_cart_by_sku",
      "description": "Add an item to the cart by SKU.",
      "parameters": {
        "type": "object",
        "properties": {
          "sku": {
            "type": "string",
            "description": "The SKU of the item to add to the cart."
          }
        },
        "required": ["sku"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "add_item_to_cart_by_name",
      "description": "Add an item to the cart by its name.",
      "parameters": {
        "type": "object",
        "properties": {
          "item_name": {
            "type": "string",
            "description": "The name of the item to add to the cart."
          }
        },
        "required": ["item_name"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "remove_line_item_from_cart",
      "description": "Remove an item from the cart by SKU.",
      "parameters": {
        "type": "object",
        "properties": {
          "sku": {
            "type": "string",
            "description": "The SKU of the item to remove from the cart."
          }
        },
        "required": ["sku"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "get_items_in_cart",
      "description": "Get a list of all items in the cart.",
      "parameters": {}
    }
  }
]

# function_names = [tool["function"]["name"] for tool in shoprite_tools if tool["type"] == "function"]


request_headers = {
  'authority': 'storefrontgateway.brands.wakefern.com',
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'en-US,en;q=0.9',
  'authorization': 'Bearer ' + bearer_token,
  'customerid': '44ac7e0e-3314-4304-93eb-6fea23edb31b',
  'origin': 'https://www.shoprite.com',
  'referer': 'https://www.shoprite.com/',
  'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'cross-site',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
  'x-shopping-mode': '11111111-1111-1111-1111-111111111111',
  'x-site-host': 'https://www.shoprite.com',
  'x-site-location': 'HeadersBuilderInterceptor'
}

def get_item_by_name(item_name):
    res = requests.get("https://storefrontgateway.brands.wakefern.com/api/stores/139/search?q=" + item_name + "&skip=0&take=10&misspelling=true", headers=request_headers)
    json_data = res.json()
    return json_data['items'][0]

def add_item_to_cart_by_sku(sku):
    request_body = {
      "quantity": 1,
      "sku": sku,
      "source": {
        "type": 'catalog',
        "shoppingModeId": '11111111-1111-1111-1111-111111111111'
      }
    }
    
    res = requests.post("https://storefrontgateway.brands.wakefern.com/api/stores/139/cart", 
      headers={ **request_headers, 
              'content-type': 'application/vnd.cart.v1+json;domain-model=AddProductLineItemToCart'}, 
      data=json.dumps(request_body))

def add_item_to_cart_by_name(item_name):
    item = get_item_by_name(item_name)
    add_item_to_cart_by_sku(item['sku'])
    return 'Added ' +  item['name'] + ' to your ShopRite cart'

def remove_line_item_from_cart(sku):
    request_body = {
      "sku": sku,
    }
    
    res = requests.post("https://storefrontgateway.brands.wakefern.com/api/stores/139/cart", 
      headers={ **request_headers, 
              'content-type': 'application/vnd.cart.v1+json;domain-model=RemoveLineItemFromCart'}, 
      data=json.dumps(request_body))
    print(res.json())

def get_items_in_cart():
  res = requests.get("https://storefrontgateway.brands.wakefern.com/api/stores/139/cart", 
      headers={ **request_headers})
  #TODO Handle unauthorized calls
  return res.json()["lineItems"]

def remove_item_from_cart_by_name(item_name):
  # TODO Search the cart for item
  cart = get_items_in_cart()



  remove_line_item_from_cart()


# add_item_to_cart_by_name('blueberries')

shoprite_functions = {
  "get_item_by_name": get_item_by_name,
  "add_item_to_cart_by_name": add_item_to_cart_by_name,
  "add_item_to_cart_by_sku": add_item_to_cart_by_sku,
  "remove_line_item_from_cart": remove_line_item_from_cart,
  "get_items_in_cart": get_items_in_cart
}

def call_shoprite_function_by_name(function_called, function_args):
  function_to_call = shoprite_functions[function_called]

  return function_to_call(*list(function_args .values()))
