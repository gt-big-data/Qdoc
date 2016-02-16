from bs4 import BeautifulSoup, Comment, Doctype, NavigableString
import concurrent.futures as futures # for multithreading
import sys, time, warnings, requests
from dbco import *

warnings.filterwarnings("ignore")

def getUrl(url):
	time1 = time.time()
	try:
		req = requests.get(url, allow_redirects=True, verify=False,timeout=10)
	except Exception as e:
		status_code = str(e)
		return {'soup': BeautifulSoup('', 'html.parser'), 'finalURL': '', 'error': status_code} # some error happened

	html = (req.text).replace('<br>', '<br />')
	return {'soup': BeautifulSoup(html, 'html.parser'), 'finalURL': req.url}

def getURLs(urls):
	with futures.ThreadPoolExecutor(max_workers=100) as executor:
		downloaded_urls = executor.map(getUrl, urls)
		# Force all feeds to download before finishing to prevent weird issues with the
		# ThreadPool shutting down before all of the tasks finishing.
		downloaded_urls = [d for d in downloaded_urls]
	return downloaded_urls

if __name__ == '__main__':
	urls = [a['url'] for a in list(db.qdoc.find({}, {'url': True}).limit(1200))]
	time2 = time.time()
	bla= getURLs(urls)
	print "MULTITHREADING : ", (time.time()-time2) ,"s"