from pyquery import PyQuery as pq 
import csv

# an ailment (9) from homepage
d = pq(url = 'http://www.earthclinic.com/CURES/sore_throat.html')

with open("remedies-sore_throat.csv", "wb") as f:
	fwriter = csv.writer(f, delimiter='\t',
						quotechar='"', quoting=csv.QUOTE_ALL)
	
	fieldnames = ("remedy", "url", "yeas")

	fwriter.writerow(fieldnames)

	table = d("#content-inner > table:nth-child(12) > tbody:nth-child(1) > tr")
	row = d("#content-inner > table:nth-child(12) > tbody:nth-child(1)")

	for i in range(0, len(table) - 1):
		fwriter.writerow([row.find("a")[i].text, row.find("a")[i].values(), row.find("b")[i].text]) # is there singular values
		# fwriter.writerow(row.find("a")[i].values())

# add sublime find and replace in code?


# http://www.earthclinic.com/CURES/sore_throat15.html#CAYENNE
# ratings and reviews for overview


print "done writing file"
