#!/usr/bin/env python

import os
import re
import requests

subscription_key = os.environ["BING_SUBSCRIPTION_KEY"]

def find_photographers():
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
    
    os = 0
    while True:
        headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
        params  = {"q": "photographer san francisco site:instagram.com", "textDecorations":True, "textFormat":"HTML", "count":50, "offset":os, "responseFilter":"Webpages"}
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()

        result_urls = set()
        for v in search_results["webPages"]["value"]:
            print(v)
            m = re.findall("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",v['snippet'])
            for email in m:
                print(v['url'],email)
        os += 50
        print(search_results["webPages"])
        if os > search_results["webPages"]["totalEstimatedMatches"]:
            break

find_photographers()
