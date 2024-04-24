import requests
import json

url = "https://www.staples.com/_next/api/hf/searchPage/"


def get_search_results(item_name):
    res = requests.get(url + item_name)
    json_data = res.json()
    print(json_data)


get_search_results("logitech mx master 3s")
