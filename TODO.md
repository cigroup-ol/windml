## Python 3 compatibility


* iteritem, map, values, xrange, keys, filter ... : replace where necessary	

* execfile (rm in py3) : use `exec(open(thefile).read())` for instance

* file(pathname) ==> open(filename)

* imports which override base library

* urllib2 ==> urllib.request

