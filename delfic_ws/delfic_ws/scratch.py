__author__ = 'scorpio'

from business.xgoogle.search import GoogleSearch, SearchError

try:
  gs = GoogleSearch("african minerals engineering limited", tld='co.uk')
  gs.results_per_page = 50
  results = gs.get_results()
  for res in results:
    print res.title.encode("utf8")
    print res.desc.encode("utf8")
    print res.url.encode("utf8")
    print
except SearchError, e:
  print "Search failed: %s" % e
