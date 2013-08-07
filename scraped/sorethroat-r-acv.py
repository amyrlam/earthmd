from pyquery import PyQuery as pq 
import csv

for i in range(4, 14):
	base_url = "http://www.earthclinic.com/CURES/sore_throat"
	all_urls = base_url + str(i) + ".html"
	#print all_urls

	d = pq(url = all_urls) 

# """ 
# START: 
# http://www.earthclinic.com/CURES/sore_throat4.html#ACV # does not start scraping at #ACV
# #content-inner2 > div:nth-child(1) > div:nth-child(16) > p:nth-child(6)

# END:
# http://www.earthclinic.com/CURES/sore_throat13.html
# #content-inner2 > div:nth-child(1) > div:nth-child(15) > p:nth-child(2)

# WHAT TO DO IF:
# errors sore_throat4, 13
# list index out of range bc no vote, no date

# """

# with open("sore_throat-remedies-acv.csv", "wb") as f:
# 	fwriter = csv.writer(f, delimiter='\t',
# 						quotechar='"', quoting=csv.QUOTE_ALL)
	
	#fieldnames = ("remedy", "url", "yeas")
	#fwriter.writerow(fieldnames)

	div = d("#content-inner2 > div:nth-child(1) > div")

	# review = d("#content-inner2 > div:nth-child(1)")
	#print div
	for i in range(0, len(div)):

		p = pq(d("#content-inner2 > div:nth-child(1) > div:nth-child(" + str(i) + ") > p[align=left]")) # each review is in a <p> tag
		
		if p.text() is not None:
			if p.text().strip()[0] == "[":
				print "---"
				# print p.text()
				try:
					review = p.text()
					vote = review.split("]", 1)[0] # do 1x, return first value (index 0) only
					review = review.split("]", 1)[1]
					date = review.split(":", 1)[0]
					review = review.split(":", 1)[1]
					username = review.split(":", 1)[0]
					review = review.split(":", 1)[1] # comment return
				except: 
					pass # pass instead of continue?	

				vote = vote.replace("[", "").strip()
				date = date.strip()
				username = username.strip()
				review = review.strip().strip('"') # review.strip(' "')
				
				print str(i+1) # id
				print vote
				print date
				print username
				print review

			# fwriter.writerow(pq(review.find("div")[i]).html()) # error: the pseudo-class "nth-child is unknown"

print "---"
print "done writing file"
