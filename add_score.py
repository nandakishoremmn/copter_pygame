import urllib,urllib2
def post_score(name='unnamed',score=0):
	mydata=[('name',name),('score',score)]
	mydata=urllib.urlencode(mydata)
	path='http://nandakishore.host56.com/copter/update.php'
	req=urllib2.Request(path,mydata)
	req.add_header("Content-type","application/x-www-form-urlencoded")
	page=urllib2.urlopen(req).readline().split()[0]
	return page
if __name__=='__main__':
	n,s=raw_input("Name : "),raw_input("Score : ")
	print str(post_score(n,s))
	raw_input()
