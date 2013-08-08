#!flask/bin/python

from app import db, models
from pyquery import PyQuery as pq 
from datetime import datetime

# ailment sore throat, remedy apple cider vinegar

# TO CHANGE:
# adjust URLs for each remedy
# manually delete reviews not for remedy in SQL

# START: 
# http://www.earthclinic.com/CURES/sore_throat4.html#ACV # does not start scraping at acv, starts at top of url
# #content-inner2 > div:nth-child(1) > div:nth-child(16) > p:nth-child(6)

# END:
# http://www.earthclinic.com/CURES/sore_throat13.html
# #content-inner2 > div:nth-child(1) > div:nth-child(15) > p:nth-child(2)

# table ailment
name = "Sore Throat"
timestamp = datetime.now()
body = 	"Add body from webpage manually in SQL here."
newailment = models.Ailment(name = name, timestamp = timestamp, body = body)
db.session.add(newailment)

# table remedy
name = "Apple Cider Vinegar"
timestamp = datetime.now()
body = 	"Add body from webpage manually in SQL here."
newremedy = models.Remedy(name = name, timestamp = timestamp, body = body)
db.session.add(newremedy)

db.session.commit()
db.session.refresh(newailment)
db.session.refresh(newremedy)

# table ailmenttoremedy
newailmenttoremedy = models.AilmentToRemedy(ailment_id = newailment.id, remedy_id = newremedy.id)
db.session.add(newailmenttoremedy)

db.session.commit()

for i in range(4, 14):
	base_url = "http://www.earthclinic.com/CURES/sore_throat"
	all_urls = base_url + str(i) + ".html"
	d = pq(url = all_urls) 

	div = d("#content-inner2 > div:nth-child(1) > div")

	for i in range(0, len(div)):

		# each review is in a <p> tag
		p = pq(d("#content-inner2 > div:nth-child(1) > div:nth-child(" + str(i) + ") > p[align=left]")) 

		if p.text() is not None:
			if p.text().strip()[0] == "[":
				try:
					review   = p.text()
					vote     = review.split("]", 1)[0] # do 1x, return first value (index 0) only
					review   = review.split("]", 1)[1]
					date     = review.split(":", 1)[0]
					review   = review.split(":", 1)[1]
					username = review.split(":", 1)[0]
					review   = review.split(":", 1)[1] # comment return
				except:
					pass
				else:
					vote     = vote.replace("[", "").strip()
					date     = date.strip()
					username = username.strip()
					review   = review.strip(' "') # long way: review.strip().strip('"')
					date     = datetime.strptime(date, "%m/%d/%Y")

					newuser = models.User.query.filter_by(nickname = username).first()
					if newuser is None:
						newuser = models.User(nickname = username)
						db.session.add(newuser)
						db.session.commit()
						db.session.refresh(newuser)

					newpost = models.Post(user_id = newuser.id, nickname = username, 
						timestamp = date, body = review, vote = vote, ailmenttoremedy_id = newailmenttoremedy.id)
					db.session.add(newpost)

	db.session.commit() # move outside of for loop for speed


