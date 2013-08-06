from pyquery import PyQuery as pq 
import csv

# url for reach sore throat remedy is row.find("a")[i].values()
d = pq(url = 'http://www.earthclinic.com/CURES/sore_throat15.html#CAYENNE')

with open("remedies-sore_throat-cayenne.csv", "wb") as f:
	fwriter = csv.writer(f, delimiter='\t',
						quotechar='"', quoting=csv.QUOTE_ALL)
	
	fieldnames = ("yeas", "date", "user from x", "description")
	fwriter.writerow(fieldnames)

	# yeas = #content-inner2 > div:nth-child(1) > div:nth-child(5) > p:nth-child(2) > font:nth-child(1) > b:nth-child(1)
	# date = 
	
	review = d("#content-inner2 > div:nth-child(1)").find("p:nth-child(2)")
	fwriter.writerow(review)

	# fwriter.writerow(d("#content-inner2 > div:nth-child(1) > div:nth-child(5) > p:nth-child(2)")
	# p contains date before ":"
	# p contains user from x after ":"
	# p contains description after <!--writes--> and another lone :

	#content-inner2 > div:nth-child(1) > div:nth-child(5) > p:nth-child(2)
	#content-inner2 > div:nth-child(1) > div:nth-child(6) > p:nth-child(2)
	#content-inner2 > div:nth-child(1) > div:nth-child(7) > p:nth-child(2)

print "done writing file"

# ???

# should yea / nay / better but with side effects / better but not cured / worked temporarily / warning! / side effects
