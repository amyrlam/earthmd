from pyquery import PyQuery as pq 
import csv

# an ailment (9) from homepage
d = pq(url = 'http://www.earthclinic.com/CURES/sore_throat.html')

# remedies = d("tbody").find("a").html() # REMEDY, but finding first "a" only
# remedy = d("#content-inner > table:nth-child(12) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > strong:nth-child(1) > span:nth-child(1) > a:nth-child(1)").text()

# d("#content-inner > table:nth-child(12) > tbody:nth-child(1)").find("a")[0].text
# > 'Cayenne'

# /sinus_infection.html
#content-inner > table:nth-child(17) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > strong:nth-child(1) > span:nth-child(1) > a:nth-child(1)
#content-inner > table:nth-child(17) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > b:nth-child(1)

# /sore_throat.html
#content-inner > table:nth-child(12) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > strong:nth-child(1) > span:nth-child(1) > a:nth-child(1)
#content-inner > table:nth-child(12) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > b:nth-child(1)

# /bacterial_vaginosis.html
#content-inner > table:nth-child(10) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > strong:nth-child(1) > span:nth-child(1) > a:nth-child(1)
#content-inner > table:nth-child(10) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > b:nth-child(1)

# /fungus.html
#content-inner > table:nth-child(17) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > strong:nth-child(1) > span:nth-child(1) > a:nth-child(1)

# /tongue.html
#content-inner > table:nth-child(15) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > strong:nth-child(1) > span:nth-child(1) > a:nth-child(1)

# /kidney_stones.html
#content-inner > table:nth-child(17) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > strong:nth-child(1) > span:nth-child(1) > a:nth-child(1)

# /sinus_congestion.html
#content-inner > table:nth-child(16) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > strong:nth-child(1) > span:nth-child(1) > a:nth-child(1)

# /gallbladder-attack-treatment.html
#content-inner > table:nth-child(16) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1)
# CONT CAUSE PAGE IS WEIRD... .style22 > a:nth-child(1)

# acid_reflux.html
#content-inner > table:nth-child(15) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > strong:nth-child(1) > span:nth-child(1) > a:nth-child(1)

### 

# home > most popular remedies (9), probably have different table:nth-child(#) as well

for i in range(0, len(d("#content-inner > table:nth-child(12) > tbody:nth-child(1)"))-1): # why not working (list index out of range) but (0,19 works)
	d("#content-inner > table:nth-child(12) > tbody:nth-child(1)").find("a")[i].text # how to call these lines into output.writerow
	d("#content-inner > table:nth-child(12) > tbody:nth-child(1)").find("a")[i].values()
	d("#content-inner > table:nth-child(12) > tbody:nth-child(1)").find("b")[i].text

with open("scraper.tsv", "w") as f:
	fieldnames = ("remedy", "url", "yeas")
	output = csv.writer (f, delimiter = "\t")

	output.writerow(fieldnames)
	output.writerow(remedy)

print "done writing file"

