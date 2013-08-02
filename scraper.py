from pyquery import PyQuery as pq 
import csv

# an ailment
d = pq(url = 'http://www.earthclinic.com/CURES/sore_throat.html')

# remedies = d("tbody").find("a").html() # REMEDY, but finding first "a" only
# remedy = d("#content-inner > table:nth-child(12) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > strong:nth-child(1) > span:nth-child(1) > a:nth-child(1)").text()
# d("#content-inner > table:nth-child(12) > tbody:nth-child(1)").find("a")[0].text
# > 'Cayenne'

#content-inner > table:nth-child(12) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > strong:nth-child(1) > span:nth-child(1) > a:nth-child(1)
#content-inner > table:nth-child(12) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > b:nth-child(1)

for i in range(0, len(d("#content-inner > table:nth-child(12) > tbody:nth-child(1)"))-1):
	d("#content-inner > table:nth-child(12) > tbody:nth-child(1)").find("a")[i].text
	d("#content-inner > table:nth-child(12) > tbody:nth-child(1)").find("a")[i].values()
	d("#content-inner > table:nth-child(12) > tbody:nth-child(1)").find("b")[i].text

with open("scraper.tsv", "w") as f:
	fieldnames = ("remedy", "url", "yeas")
	output = csv.writer (f, delimiter = "\t")

	output.writerow(fieldnames)
	output.writerow(remedy)

print "done writing file"

