from pyquery import PyQuery as pq 
import csv

d = pq(url = 'http://www.earthclinic.com/CURES/sore_throat15.html#CAYENNE') # starts on http://www.earthclinic.com/CURES/sore_throat4.html#ACV and goes til ?

""" 
START: 
http://www.earthclinic.com/CURES/sore_throat15.html#CAYENNE 
# weird tabs: ratings & reviews PLUS treatment
#content-inner2 > div:nth-child(1) > div:nth-child(5) > p:nth-child(2)

END:
http://www.earthclinic.com/CURES/sore_throat40.html
full page

WHAT TO DO IF:
errors sore_throat15, 40
list index out of range bc no vote, no date

- manually skip <p>'s?
- if no review ... skip?
"""

# with open("sore_throat-remedies-acv.csv", "wb") as f:
# 	fwriter = csv.writer(f, delimiter='\t',
# 						quotechar='"', quoting=csv.QUOTE_ALL)
	
	#fieldnames = ("remedy", "url", "yeas")
	#fwriter.writerow(fieldnames)

div = d("#content-inner2 > div:nth-child(1) > div")

# review = d("#content-inner2 > div:nth-child(1)")

for i in range(0, len(div)):
	p = pq(d("#content-inner2 > div:nth-child(1) > div:nth-child(" + str(i) + ") > p[align=left]")) # each review is in a <p> tag
	if p.text() is not None:
		if p.text().strip()[0] == "[":
			print "---"
			# print p.text()
			review = p.text()
			vote = review.split("]", 1)[0] # do 1x, return first value only
			review = review.split("]", 1)[1]
			date = review.split(":", 1)[0]
			review = review.split(":", 1)[1]
			username = review.split(":", 1)[0]
			review = review.split(":", 1)[1] # comment return

			vote = vote.replace("[", "").strip()
			date = date.strip()
			username = username.strip()
			review = review.strip().strip('"') # review.strip(' "')
			
			print str(i+1) 
			print vote
			print date
			print username
			print review

		# fwriter.writerow(pq(review.find("div")[i]).html()) # error: the pseudo-class "nth-child is unknown"

print "---"
print "done writing file"
