#!flask/bin/python

from app import db, models
from pyquery import PyQuery as pq 
from datetime import datetime

for i in range(4, 14):
	base_url = "http://www.earthclinic.com/CURES/sore_throat"
	all_urls = base_url + str(i) + ".html"
	d = pq(url = all_urls) 

# TO CHANGE:
# adjust URLs for each remedy
# manually delete comments not for remedy 
# adjust ailmenttoremedy_id for each



# START: 
# http://www.earthclinic.com/CURES/sore_throat4.html#ACV # does not start scraping at acv, starts at top of url
# #content-inner2 > div:nth-child(1) > div:nth-child(16) > p:nth-child(6)

# END:
# http://www.earthclinic.com/CURES/sore_throat13.html
# #content-inner2 > div:nth-child(1) > div:nth-child(15) > p:nth-child(2)

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

					# ADJUST AILMENTTOREMEDY_ID for each one
					newpost = models.Post(user_id = newuser.id, ailmenttoremedy_id = 2, nickname = username, 
						timestamp = date, body = review, vote = vote)
					db.session.add(newpost)

	db.session.commit() # move outside of for loop for speed

# table ailment
name = "Sore Throat"
timestamp = datetime.datetime.now()
body = 	"Sore Throat Cures"
		"A sore throat is an infection that can be either viral or bacterial. It is most commonly caused by a " 
		"contagious viral infection (such as the flu, cold or mononucleosis), although more serious throat " 
		"infections can be caused by a bacterial infection (such as strep, mycoplasma or hemophilus). "
		"Home Remedies for Sore Throat" 
		"Bacterial sore throats respond well to antibiotics while viral infections "
		"do not. For viral infections, there are many natural remedies that you can take to cure a sore throat. "
		"Cayenne pepper and apple cider vinegar are easily the two most popular home remedy sore throat cures. "
		"Some of these folk remedies work within an hour or two, others take effect overnight. If you do not "
		"see some improvement overnight, please visit your doctor, especially if you suspect strep throat."
newailment = models.Ailment(name = name, timestamp = timestamp, body = body)

# table remedy
name = "Apple Cider Vinegar"
timestamp = datetime.datetime.now()
body = 	"Apple Cider Vinegar for Health!"
		"Apple Cider Vinegar, that wonderful old-timers home remedy, cures more ailments than any other folk "
		"remedy -- we're convinced! From the extensive feedback we've received over the past 8 years, the "
		"reported cures from drinking Apple Cider Vinegar are numerous. They include cures for allergies "
		"(including pet, food and environmental), sinus infections, acne, high cholesterol, flu, chronic "
		"fatigue, candida, acid reflux, sore throats, contact dermatitis, arthritis, and gout. Apple Cider "
		"Vinegar also breaks down fat and is widely used to lose weight. It has also been reported that a "
		"daily dose of apple cider vinegar in water has high blood pressure under control in two weeks! "
		"Apple Cider Vinegar is also wonderful for pets, including dogs, cats, and horses. It helps them "
		"with arthritic conditions, controls fleas & barn flies, and gives a beautiful shine to their coats! "
		"Earth Clinic's #1 Remedy: Apple Cider Vinegar! "
		"If you can get over the taste of apple cider vinegar, you will find it one of the most important "
		"natural remedies in healing the body. As a wonderful side effect of drinking apple cider vinegar "
		"every day, we've discovered that it brings a healthy, rosy glow to one's complexion! This is great "
		"news if you suffer from a pale countenance."
newremedy = models.Remedy(name = name, timestamp = timestamp, body = body)

# table ailmenttoremedy
newailmenttoremedy = models.AilmentToRemedy(ailment_id = newailment.id, remedy_id = newremedy.id)
