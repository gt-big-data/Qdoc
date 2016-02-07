from difflib import SequenceMatcher
from dbco import *
import sys, time

def similar(a, b):
	rat = len(a)/float(len(b))
	if rat < 0.9 or rat > 1.1:
		return 0
	return SequenceMatcher(None, a, b).ratio()

def good(val):
	return val and len(val) > 0

def isValid(a):
	"""Check if the article has enough data to be considered "crawled"."""
	if not good(a.get('guid', '')):
		return False
	if not good(a.get('title', '')):
		return False
	if not good(a.get('url', '')):
		return False
	if a.get('timestamp', 0) < 500:
		return False
	if not good(a.get('source', '')):
		return False
	if not good(a.get('feed', '')):
		return False
	if not good(a.get('content', '')):
		return False
	return True

def isDuplicate(content, title, source):
	last = db.qdoc.find({'source': source, 'timestamp': {'$gte': (time.time()-3*86400)}}).sort('timestamp', -1) # last 3 days
	content = unicode(content)
	for a in last:
		if title == a['title'] or similar(content, unicode(a['content'])) > 0.9:
			return a['_id']
	return None