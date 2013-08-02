from pyquery import PyQuery as pq 
import csv

# with open('scraper.csv', 'wb') as csvfile:
#     spamwriter = csv.writer(csvfile, delimiter='\t',
#                             quotechar='"', quoting=csv.QUOTE_ALL)
#     spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
#     spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])





# an ailment (9) from homepage
d = pq(url = 'http://www.earthclinic.com/CURES/sore_throat.html')

with open("scraper.csv", "wb") as f:
	fwriter = csv.writer(f, delimiter='\t',
						quotechar='"', quoting=csv.QUOTE_ALL)
	
	fieldnames = ("remedy", "url", "yeas")

	fwriter.writerow(fieldnames)

	table = d("#content-inner > table:nth-child(12) > tbody:nth-child(1) > tr")
	row = d("#content-inner > table:nth-child(12) > tbody:nth-child(1)")

	for i in range(0, len(table) - 1):
		fwriter.writerow([row.find("a")[i].text, row.find("a")[i].values(), row.find("b")[i].text]) # is there singular values
		#fwriter.writerow(row.find("a")[i].values())

		# use one writerow command for all three? but writerow only takes one arg?
		#fwriter.writerow(d("#content-inner > table:nth-child(12) > tbody:nth-child(1)").find("a")[i].values())
		#fwriter.writerow(d("#content-inner > table:nth-child(12) > tbody:nth-child(1)").find("b")[i].text) # adjust to get # only not YEAS - parse or delete YEAS

print "done writing file"

#content-inner > table:nth-child(12) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > strong:nth-child(1) > span:nth-child(1) > a:nth-child(1)
#content-inner > table:nth-child(12) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > strong:nth-child(1) > span:nth-child(1) > a:nth-child(1)