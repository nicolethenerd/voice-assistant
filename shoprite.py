import requests
import json

request_headers = {

}

def get_sku_by_name(item_name):
    res = requests.get("https://storefrontgateway.brands.wakefern.com/api/stores/139/search?q=" + item_name + "&skip=0&take=10&misspelling=true", headers=request_headers)
    json_data = res.json()
    return json_data['items'][0]['sku']

def add_item_to_cart_by_sku(sku):
    request_body = {
      "quantity": 1,
      "sku": sku,
      "source": {
        "type": 'catalog',
        "shoppingModeId": '11111111-1111-1111-1111-111111111111'
      }
    }
    
    requests.post("https://storefrontgateway.brands.wakefern.com/api/stores/139/cart", headers=request_headers, data=json.dumps(request_body))

def add_item_to_cart_by_name(item_name):
    sku = get_sku_by_name(item_name)
    # print(sku)
    add_item_to_cart_by_sku(sku)

# add_item_to_cart_by_name('blueberries')
# add_item_to_cart_by_name('strawberries')
# add_item_to_cart_by_name('bananas')
# add_item_to_cart_by_name('spinach')

