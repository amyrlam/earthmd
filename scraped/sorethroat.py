from pyquery import PyQuery as pq 
#import csv

# an ailment (9) from homepage
d = pq(url = 'http://www.earthclinic.com/CURES/sore_throat.html')

# with open("sore_throat-remedies.csv", "wb") as f:
# 	fwriter = csv.writer(f, delimiter='\t',
# 						quotechar='"', quoting=csv.QUOTE_ALL)
	
	#fieldnames = ("remedy", "url", "yeas")
	#fwriter.writerow(fieldnames)

table = d("#content-inner > table:nth-child(12) > tbody:nth-child(1) > tr")
row = d("#content-inner > table:nth-child(12) > tbody:nth-child(1)")

#content-inner > table:nth-child(12) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > strong:nth-child(1) > span:nth-child(1) > a:nth-child(1)
#content-inner > table:nth-child(12) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > strong:nth-child(1) > span:nth-child(1) > a:nth-child(1)

for i in range(0, len(table)):
	#print "---"
	remedy = row.find("a")[i].text
	#remedy = pq(d("#content-inner > table:nth-child(12) > tbody:nth-child(1) > tr:nth-child(" + str(i) + ") > td:nth-child(1) > strong:nth-child(1) > span:nth-child(1) > a:nth-child(1)"))

	url = row.find("a")[i].values()
	num_yeas = row.find("b")[i].text

	url = str(url).strip("['").strip("']")
	num_yeas = num_yeas.strip(" YEAS")

	print str(i+1)+","+remedy+","+url+","+num_yeas
	#print url+"*",
	#print num_yeas

	# fwriter.writerow([row.find("a")[i].text, row.find("a")[i].values(), row.find("b")[i].text]) # is there singular values?
	# fwriter.writerow(row.find("a")[i].values()) # this was the individual way

	# add sublime find and replace in code?

#print "done writing file"
