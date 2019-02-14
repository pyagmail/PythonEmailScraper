# Import libraries
import re
import requests
import requests.exceptions
import csv
import signal
import sys
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
from colorama import *
init()

# starting url. replace google with your own url.
starting_url = 'https://www.neti.ee/cgi-bin/teema/ARI/Byrooteenused/'

# UNCOMMENT THIS ON PRODUCTION
# print(Fore.YELLOW + "~~~~Email Scraper v1~~~~" 
# starting_url = input("Enter Website Link to Scrape: ")
# print("Starting scraper.." + Fore.WHITE)

# a queue of urls to be crawled
unprocessed_urls = deque([starting_url])

# set of already crawled urls for email
processed_urls = set()

# a set of fetched emails
emails = set()

# process urls one by one from unprocessed_url queue until queue is empty
while len(unprocessed_urls):

    # move next url from the queue to the set of processed urls
    url = unprocessed_urls.popleft()
    processed_urls.add(url)

    # extract base url to resolve relative links
    parts = urlsplit(url)
    base_url = "{0.scheme}://{0.netloc}".format(parts)
    path = url[:url.rfind('/')+1] if '/' in parts.path else url

    # get url's content
    print(Fore.CYAN + "Crawling URL %s" % url + Fore.WHITE)
    try:
        response = requests.get(url)
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        # ignore pages with errors and continue with next url
        continue

        # Check for CTRL+C interruption
    except KeyboardInterrupt:
        print(Back.GREEN + Bar('=', 100) + Back.BLACK)
        print("[[Session Stopped]]")
        print("Emails Found:")
        print(emails)
        print(Back.GREEN + Bar('=', 50) + Back.BLACK)
        session_continue = input("Would you Like to continue?[Y/N]:")
        if session_continue is 'Y':
            # Continue from last url and
            # unprocessed url set
        elif session_continue is 'N':
            session_choice = input("Save emails as .CSV?").upper()
            if session_choice is 'Y':
                # Sae
        

        sys.exit()

    # extract all email addresses and add them into the resulting set
    # You may edit the regular expression as per your requirement
    new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
    emails.update(new_emails)
    
    if len(new_emails) is 0:
        print(Back.RED)        
        print("No emails found")
        print(Back.BLACK)
    else:
        print(Back.GREEN) 
        print(new_emails)
        print("Email Count: ", len(emails))
        print(Back.BLACK)
    
    # create a beutiful soup for the html document
    soup = BeautifulSoup(response.text, 'lxml')

    # Once this document is parsed and processed, now find and process all the anchors i.e. linked urls in this document
    for anchor in soup.find_all("a"):
        # extract link url from the anchor
        link = anchor.attrs["href"] if "href" in anchor.attrs else ''
        # resolve relative links (starting with /)
        if link.startswith('/'):
            link = base_url + link
        elif not link.startswith('http'):
            link = path + link
        # add the new url to the queue if it was not in unprocessed list nor in processed list yet
        if not link in unprocessed_urls and not link in processed_urls:
            unprocessed_urls.append(link)

# This is for writing a csv file
'''
with open('_EMAILS.csv', 'w') as emails_file:
    writer = csv.writer(emails_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    writer.writerow(emails)
'''

# A fancy bar
def Bar(string_to_expand, length):
    return (string_to_expand * (int(length/len(string_to_expand))+1))[:length]

print(Back.GREEN + Bar('=', 100) + Back.BLACK)
print("Emails Found:")
print(emails)




