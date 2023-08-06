import requests
from fake_useragent import UserAgent
import re
import time
from bs4 import BeautifulSoup
import os
import argparse
import sys
import itertools

def bulk_download_thingiverse(thingurl,savedir):
    import webdriver_selector
    if not thingurl.endswith("/files"):
        thingurl=thingurl+"/files"
    linkcount=0
    linkcountold=0
    finishedloading=False
    driver=webdriver_selector.selector().driver
    driver.get(thingurl)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    spinner = itertools.cycle(['-', '/', '|', '\\'])
    print("Loading page. Please wait...")
    while len(soup.find_all('div', {'class': 'Spinner__spinnerWrapper--3TRqa'}))>0:
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        sys.stdout.write('\b')
        time.sleep(.1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    sys.stdout.write('\x1b[1K\r')
    print("gathering links from page, please wait...")
    while True:
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        sys.stdout.write('\b')

        linkcountold=linkcount
        #this is so inelegant. There has to be something which loads ONLY when the page is complete which we can look for.
        time.sleep(5)
        soup=BeautifulSoup(driver.page_source,'html.parser')
        alldownloads=soup.find_all('a',{'class':re.compile('ThingFile__download*')})
        linkcount=len(alldownloads)
        if linkcount==linkcountold:
            break


    driver.quit()
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    for downloadlink in alldownloads:
        if 'href' in downloadlink.attrs:
            filename=savedir+"/"+downloadlink.attrs['href'].split('/')[-1]
            r = requests.get(downloadlink.attrs['href'], allow_redirects=True, headers={"User-Agent": str(UserAgent().random)})
            with open(filename, 'wb') as myfile:
                myfile.write(r.content)
            print("downloaded "+filename)
    print("Done!")

def main():
    parser = argparse.ArgumentParser(description='thingdl allows you to quickly and easily download all files from a thing page.')
    parser.add_argument('-u', '--url', help='URL to the page where you can download things, ends with /files', required=True)
    parser.add_argument('-d', '--dest', help='Destination folder where you want the files downloaded to', required=True)
    args = vars(parser.parse_args())
    print(args)
    bulk_download_thingiverse(args['url'],args['dest'])

if __name__ == "__main__":
    main()