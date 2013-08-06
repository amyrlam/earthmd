from pyquery import PyQuery as pq 
import csv

# an ailment (9) from homepage
d = pq(url = 'http://www.earthclinic.com/CURES/sinus_infection.html')

with open("sinus_infection-remedies.csv", "wb") as f:
	fwriter = csv.writer(f, delimiter='\t',
						quotechar='"', quoting=csv.QUOTE_ALL)
	
	fieldnames = ("remedy", "url", "yeas")
	fwriter.writerow(fieldnames)

	#content-inner > table:nth-child(17) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > strong:nth-child(1) > span:nth-child(1) > a:nth-child(1)
	#content-inner > table:nth-child(17) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > strong:nth-child(1) > span:nth-child(1) > a:nth-child(1)

	table = d("#content-inner > table:nth-child(17) > tbody:nth-child(1) > tr")

	row = d("#content-inner > table:nth-child(17) > tbody:nth-child(1)")

	for i in range(0, len(table)):
		fwriter.writerow([row.find("a")[i].text, row.find("a")[i].values(), row.find("b")[i].text]) # is there singular values because it returns ['']

	# add sublime find and replace in code?

print "done writing file"

# file identical to sore_throat.py except table is (17)...why not working?!?