#!/usr/bin/env python

import requests
import re
import csv
import os
import urllib3
import certifi
from bs4 import BeautifulSoup

subscription_key = os.environ["BING_SUBSCRIPTION_KEY"]

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

def get_biz_url(biz_name):
    """ Get a list of biz urls """
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"

    headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
    params  = {"q": biz_name, "textDecorations":True, "textFormat":"HTML"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    result_urls = set()
    for v in search_results["webPages"]["value"]:
        words = re.split(" ", biz_name)
        lw = len(words)
        nw = 0
        m = re.match("https?://([^/]+)/.*", v["url"])
        url = m.group(1)
        for w in words:
            if w.lower() in url.lower():
                nw += 1
        pct = (nw + 0.0)/lw
        if pct >= .5:
            if check_if_cali(url):
                result_urls.add(url)
    return list(result_urls)

def check_if_cali(url, depth=1):
    try:
        r = http.request('GET', url) 
    except:
        return False

    if re.search("San Francisco", r.data.decode('utf-8'), re.IGNORECASE) or re.search(", ?CA",r.data.decode('utf-8'), re.IGNORECASE):
        return True
    if depth == 0:
        return False
    soup = BeautifulSoup(r.data, 'html.parser')
    links = []
    for link in soup.findAll('a'):
        l = link.get('href')
        links.append(l)
    for link in links:
        if check_if_cali(link, depth - 1):
            return True
    return False

def main():
    n = 0
    writer = csv.writer(open("output.csv", "w"))

    with open("Registered_Business_Locations_-_San_Francisco.csv","r") as csvfile:
        reader = csv.reader(csvfile)
        first = True
        for row in reader:
            if first:
                first = False
            else:
                if re.match("Private Education and Health Services" ,row[17]) or re.match("Administrative", row[17]):
                    if not re.search("(inc|corp|inst|llc|center|university|clinic|practice|medical|foundation|charit|organization|assoc|health|school|hlth|training|ctr|archdi|agency|trust|family|svcs| cal |california|hospital|md|&|academy)", row[2], re.IGNORECASE) and not re.search("md",row[3]) and row[9] == "" and row[11] == "":
                        try:
                            urls = get_biz_url(row[3])
                            print([row[0],row[1],row[2],row[3],row[16],row[17],";".join(urls)])
                            writer.writerow([row[0],row[1],row[2],row[3],row[16],row[17],";".join(urls)])
                        except:
                            pass
                    #print(get_biz_url(row[2]))

main()
#check_if_cali("sancarloshousecleaning.com")
