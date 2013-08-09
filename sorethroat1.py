#!flask/bin/python

from app import db, models
from pyquery import PyQuery as pq 
from datetime import datetime

# ailment sore throat, remedy cayenne

# TO CHANGE:
# adjust ailment name, remedy name as string
# adjust range and URL
# manually delete reviews not for remedy in SQL that are scraped as full page is scraped

# table ailment
name = "Sore Throat"

newailment = models.Ailment.query.filter_by(name = name).first()
if newailment is None:
	timestamp = datetime.now()
	body = 	"Add body from webpage manually in SQL here."
	newailment = models.Ailment(name = name, timestamp = timestamp, body = body)
	db.session.add(newailment)
	db.session.commit()
	db.session.refresh(newailment)

# table remedy
name = "Cayenne"

newremedy = models.Ailment.query.filter_by(name = name).first()
if newremedy is None:
	timestamp = datetime.now()
	body = 	"Add body from webpage manually in SQL here."
	newremedy = models.Remedy(name = name, timestamp = timestamp, body = body)
	db.session.add(newremedy)
	db.session.commit()
	db.session.refresh(newremedy)

# table ailmenttoremedy
newailmenttoremedy = models.AilmentToRemedy(ailment_id = newailment.id, remedy_id = newremedy.id)
db.session.add(newailmenttoremedy)
db.session.commit()

for i in range(15, 41): # range is not inclusive on RHS
	base_url = "http://www.earthclinic.com/CURES/sore_throat"
	all_urls = base_url + str(i) + ".html"
	d = pq(url = all_urls) 

	div = d("#content-inner2 > div:nth-child(1) > div")

	for i in range(0, len(div)+1):

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


