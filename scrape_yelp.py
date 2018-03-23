#!/usr/bin/env python

# Performs scraping and analysis on businesses retrieved via get_yelp.py.

import db
import urllib3
import whois
import re
from bs4 import BeautifulSoup
import time

http = urllib3.PoolManager()

def get_urls(limit=1):
        dbi = db.get_db()
        cur = dbi.cursor()
        cur.execute("select * from yelp_load where yelp_url_scraped = 0 order by rand() limit %s", (limit,))
        rows = cur.fetchall()
        urls = []
        rowLookup = {}
        for row in rows:
            urls.append(row[3])
            rowLookup[row[3]] = row
        websites = []
        ids = []
        for url in urls:
            requrl = url.split("?")[0]
            try:
                r = http.request('GET', requrl)
                print("MADE REQUEST",requrl,r.status)
                if r.status == 200:
                    websiteList = get_website_from_text(r.data)
                    print("ABOUT TO YIELD")
                    yield websiteList, rowLookup[url][0]
            except:
                print("FAILED TO FETCH DOMAIN")


def get_website_from_text(txt):
    soup = BeautifulSoup(txt, 'html.parser')
    websites = []
    for wsBlock in soup.find_all("span", class_="biz-website"):
        ws = wsBlock.a.get_text()
        websites.append(ws)
    return websites

def get_whois_emails(domain):
    w = None
    goodEmails = set()

    try:
        w = whois.whois(domain)
        e = w.emails
    except:
        return goodEmails
    if not w or not w.emails:
        return goodEmails
    for email in w.emails:
        if re.match("DOMAINSBYPROXY\.COM$",email,re.IGNORECASE):
            continue
        if re.match("godaddy\.com$",email,re.IGNORECASE):
            continue
        if re.match("^abuse@",email,re.IGNORECASE):
            continue
        if not email:
            continue
        if re.match("(gmail\.com|aol\.com|comcast\.net|hushmail\.com|outlook\.com|googlemail\.com|yahoo\.com|mail\.com)", email, re.IGNORECASE):
            goodEmails.add(email)
        else:
            dp = domain.split(".")
            if len(dp) >= 2:
                dregex = dp[-2] + "." + dp[-1] + "$"
            if re.match(dregex, email):
                goodEmails.add(email)
    return goodEmails

def get_scrape_emails(domain, depth = 1):
   
   emails = set()
   r = None
   try:
       r = http.request('GET', domain) 
   except:
       return emails
   if r.status == 200:
       soup = BeautifulSoup(r.data, 'html.parser')
       mailtos = soup.select('a[href^=mailto]')
       for i in mailtos:
           emails.add(i['href'].split(":")[1])
       for el in soup.find_all():
           for possible in el.get_text().strip().split(" "):
               if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", possible):
                  emails.add(possible.lower())
       if depth > 1:
           links = []
           for link in soup.findAll('a'):
               l = link.get('href')
               if l.startswith('http'):
                   links.append(l)
               elif l.find(":") == -1:
                   if l[0] == '/':
                       links.append(domain + l)
                   else:
                       if domain[-1] == '/':
                           links.append(domain + l)
                       else:
                           links.append(domain + '/' + l)
           for l in links:
               emails = emails.union(get_scrape_emails(l, depth - 1))
   return emails

def get_emails(domain):
    emails = set()
    emails = emails.union(get_whois_emails(domain))
    emails = emails.union(get_scrape_emails(domain))
    return list(emails)

def save_emails(yelp_id, domain, emails):
    dbi = db.get_db()
    sql = "insert into yelp_load_emails(yelp_load_id,domain,email) values(%s,%s,%s)"
    for email in emails:
        cursor = dbi.cursor()
        cursor.execute(sql, (yelp_id, domain, email))
    cursor = dbi.cursor()
    cursor.execute("update yelp_load set yelp_url_scraped=1 where id=%s", (yelp_id,))
    dbi.commit()

def main():
    for (websites, ourid) in get_urls(1000):
        time.sleep(0.01)
        print("DATA",websites, ourid)
        for domain in websites:
            print("DOMAIN",domain)
            emails = get_emails(domain)
            print("EMAILS",emails)
            save_emails(ourid, domain, emails)

main()
#print(get_emails("rodionmath.club"))
