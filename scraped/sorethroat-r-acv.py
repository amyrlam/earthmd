from pyquery import PyQuery as pq 
import csv

d = pq(url = 'http://www.earthclinic.com/CURES/sore_throat.html') # starts on http://www.earthclinic.com/CURES/sore_throat4.html#ACV and goes til ?

# with open("sore_throat-remedies-acv.csv", "wb") as f:
# 	fwriter = csv.writer(f, delimiter='\t',
# 						quotechar='"', quoting=csv.QUOTE_ALL)
	
	#fieldnames = ("remedy", "url", "yeas")
	#fwriter.writerow(fieldnames)

div = d("#content-inner2 > div:nth-child(1) > div")

review = d("#content-inner2 > div:nth-child(1)")

	# 1st review on page: nay
	#content-inner2 > div:nth-child(1) > div:nth-child(2) > p:nth-child(6) # why does p also change?

	# 2nd review on page: better but not cured
	#content-inner2 > div:nth-child(1) > div:nth-child(3) > p:nth-child(2)

	# 3rd review on page: better but not cured
	#content-inner2 > div:nth-child(1) > div:nth-child(4) > p:nth-child(2)

	# 4th review on page: yea
	#content-inner2 > div:nth-child(1) > div:nth-child(5) > p:nth-child(2)

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
				
			print vote
			print date
			print username
			print review

		# fwriter.writerow(pq(review.find("div")[i]).html()) # error: the pseudo-class "nth-child is unknown"

	# add sublime find and replace in code?

print "done writing file"
