#!/usr/bin/env python

# Performs searches on Yelp, storing URLs for later scraping and analysis.

import csv
import json
import os
import pickle
import db
import re
import db

from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import argparse

CONSUMER_KEY = os.environ["YELP_CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["YELP_CONSUMER_SECRET"]
TOKEN = os.environ["YELP_TOKEN"]
TOKEN_SECRET = os.environ["YELP_TOKEN_SECRET"]

auth = Oauth1Authenticator(
    consumer_key=YELP_CONSUMER_KEY,
    consumer_secret=YELP_CONSUMER_SECRET,
    token=YELP_TOKEN,
    token_secret=YELP_TOKEN_SECRET
)

def fetch(location='San Francisco', category='private tutors', start=0, pages=1000):
    client = Client(auth)
    results = []
    i=start
    while i < pages: 
        businesses = client.search(location, term=category, offset=i).businesses
        results.append(businesses)
        print (i)
        if (len(businesses)<20):
            break
        i+=20

    dicts_to_output = [
        {
            'Source': 'Yelp',
            'Position': '',
            'Phone': biz.display_phone,
            'Yelp_ID': biz.id,
            'Yelp_URL': biz.url,
            'Business_Name': biz.name,
            'Website': '',
            'Email': '',
            'Individual?': '',
            'First_Name': '',
            'Last_Name': '',
            'Has_booking_on_website?': '',
            'Address': biz.location.address,
            'City': biz.location.city,
            'State': biz.location.state_code,
            'Zip_Code': biz.location.postal_code,
            'Yelp_Top_Category': biz.categories[0].alias if biz.categories else '',
            'Yelp_Review_Count': biz.review_count,
            'Yelp_Rating': biz.rating
        }
        for biz in [item for sublist in results for item in sublist]
    ]
    return dicts_to_output



def write_dicts(output, output_file = 'my_output_file.csv'):
    csv_keys = ['Source', 'Position','Phone','Yelp_ID','Yelp_URL', 'Business_Name','Website','Email', 'Individual?','First_Name','Last_Name','Has_booking_on_website?','Address','City','State','Zip_Code','Yelp_Top_Category','Yelp_Review_Count','Yelp_Rating']
    with open(output_file, 'w', encoding='utf8') as output_file:
        dict_writer = csv.DictWriter(output_file, csv_keys, quoting=csv.QUOTE_NONNUMERIC)
        dict_writer.writeheader()
        dict_writer.writerows(dicts_to_output)

def write_to_db(output):
    database=db.get_db()
    sql = "insert ignore into yelp_load(phone, yelp_id, yelp_url, business_name, address, city, state, zip_code, yelp_top_category, yelp_review_count, yelp_rating) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    for c in output:
        try:
            cur = database.cursor()
            cur.execute(sql, (c['Phone'], c['Yelp_ID'], c['Yelp_URL'], c['Business_Name'], "\n".join(c['Address']), c['City'], c['State'], c['Zip_Code'], str(c['Yelp_Top_Category']), str(c['Yelp_Review_Count']), str(c['Yelp_Rating'])))
            database.commit()
        except:
            pass
    

def main():
    parser = argparse.ArgumentParser(description='Scrape from yelp and add to database')
    parser.add_argument("--scrape", nargs=2, help='City and type of listings to scrape')
    parser.add_argument("--pages", nargs=1, default="1")
    parser.add_argument("--start", nargs=1, default="0")
    parser.add_argument("--output", nargs=1)
    parser.add_argument("--pickle", nargs=1)
    parser.add_argument("--savedb", action='store_true')
    r = parser.parse_args()
    print(r)
    results = None
    if r.scrape:
        results = fetch(r.scrape[0], r.scrape[1], int(r.start[0]), int(r.pages[0]))
        if r.output:
            pickle.dump(results, open(r.output[0], "wb"))
    if r.pickle:
        results = pickle.load(open(r.pickle[0],"rb"))
    if r.savedb:
        write_to_db(results)

main()
