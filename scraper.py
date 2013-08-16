#!flask/bin/python

from app import db, models
from pyquery import PyQuery as pq 
from datetime import datetime

pages = [
	{ 'ailment': 'Acid Reflux', 'remedy': 'Apple Cider Vinegar', 'x': 3, 'y': 25, 
	  'base_url': 'http://www.earthclinic.com/CURES/acid_reflux' }, 
	{ 'ailment': 'Bacterial Vaginosis', 'remedy': 'Hydrogen Peroxide', 'x': 31, 'y': 40, 
	  'base_url': 'http://www.earthclinic.com/CURES/bacterial_vaginosis' }, 
	{ 'ailment': 'Gallbladder Attack', 'remedy': 'Apple Cider Vinegar in Apple Juice', 'x': 1, 'y': 4, 
	  'base_url': 'http://www.earthclinic.com/CURES/gallbladder-attack-treatment' }, 
	{ 'ailment': 'Kidney Stones', 'remedy': 'Lemon Juice and Olive Oil', 'x': 7, 'y': 28, 
	  'base_url': 'http://www.earthclinic.com/CURES/kidney_stones' }, 
	{ 'ailment': 'Nail Fungus', 'remedy': 'Apple Cider Vinegar', 'x': 1, 'y': 4, 
	  'base_url': 'http://www.earthclinic.com/CURES/fungus' }, 
	{ 'ailment': 'Sinus Congestion', 'remedy': 'Apple Cider Vinegar', 'x': 1, 'y': 6, 
	  'base_url': 'http://www.earthclinic.com/CURES/sinus_congestion' }, 

	{ 'ailment': 'Sinus Infection', 'remedy': 'Apple Cider Vinegar', 'x': 1, 'y': 18, 
	  'base_url': 'http://www.earthclinic.com/CURES/sinus_infection' }, 
	{ 'ailment': 'Sinus Infection', 'remedy': 'Saline Rinse', 'x': 33, 'y': 37, 
	  'base_url': 'http://www.earthclinic.com/CURES/sinus_infection' }, 
	{ 'ailment': 'Sinus Infection', 'remedy': 'Cayenne Snorting', 'x': 18, 'y': 21, 
	  'base_url': 'http://www.earthclinic.com/CURES/sinus_infection' }, 
	{ 'ailment': 'Sinus Infection', 'remedy': 'Hydrogen Peroxide and Sea Salt', 'x': 27, 'y': 28, 
	  'base_url': 'http://www.earthclinic.com/CURES/sinus_infection' }, 
	{ 'ailment': 'Sinus Infection', 'remedy': 'Hydrogen Peroxide', 'x': 25, 'y': 27, 
	  'base_url': 'http://www.earthclinic.com/CURES/sinus_infection' }, 
	{ 'ailment': 'Sinus Infection', 'remedy': 'Grapefruit Seed Extract', 'x': 23, 'y': 25, 
	  'base_url': 'http://www.earthclinic.com/CURES/sinus_infection' }, 
	{ 'ailment': 'Sinus Infection', 'remedy': 'Neti Pot', 'x': 29, 'y': 31, 
	  'base_url': 'http://www.earthclinic.com/CURES/sinus_infection' }, 
	{ 'ailment': 'Sinus Infection', 'remedy': 'Steaming with Apple Cider Vinegar', 'x': 36, 'y': 38, 
	  'base_url': 'http://www.earthclinic.com/CURES/sinus_infection' }, 
	{ 'ailment': 'Sinus Infection', 'remedy': 'Oregano Oil', 'x': 31, 'y': 33, 
	  'base_url': 'http://www.earthclinic.com/CURES/sinus_infection' }, 
	{ 'ailment': 'Sinus Infection', 'remedy': 'Oil Pulling', 'x': 30, 'y': 32, 
	  'base_url': 'http://www.earthclinic.com/CURES/sinus_infection' }, 
	{ 'ailment': 'Sinus Infection', 'remedy': 'Garlic', 'x': 22, 'y': 24, 
	  'base_url': 'http://www.earthclinic.com/CURES/sinus_infection' }, 
	{ 'ailment': 'Sinus Infection', 'remedy': 'Colloidal Silver', 'x': 21, 'y': 22, 
	  'base_url': 'http://www.earthclinic.com/CURES/sinus_infection' }, 
	{ 'ailment': 'Sinus Infection', 'remedy': 'Mutliple Remedies', 'x': 28, 'y': 30, 
	  'base_url': 'http://www.earthclinic.com/CURES/sinus_infection' }, 
	{ 'ailment': 'Sinus Infection', 'remedy': 'Dietary Changes', 'x': 22, 'y': 23, 
	  'base_url': 'http://www.earthclinic.com/CURES/sinus_infection' }, 

	{ 'ailment': 'Sore Throat', 'remedy': 'Cayenne', 'x': 15, 'y': 41, 
	  'base_url': 'http://www.earthclinic.com/CURES/sore_throat' }, 
	{ 'ailment': 'Sore Throat', 'remedy': 'Apple Cider Vinegar', 'x': 4, 'y': 14, 
	  'base_url': 'http://www.earthclinic.com/CURES/sore_throat' }, 
	{ 'ailment': 'Sore Throat', 'remedy': 'ACV and Cayenne', 'x': 1, 'y': 5, 
	  'base_url': 'http://www.earthclinic.com/CURES/sore_throat' }, 
	{ 'ailment': 'Sore Throat', 'remedy': 'Pickle Juice Brine', 'x': 54, 'y': 57, 
	  'base_url': 'http://www.earthclinic.com/CURES/sore_throat' }, 
	{ 'ailment': 'Sore Throat', 'remedy': 'Salt Water Gargle', 'x': 57, 'y': 60, 
	  'base_url': 'http://www.earthclinic.com/CURES/sore_throat' }, 
	{ 'ailment': 'Sore Throat', 'remedy': 'Hydrogen Peroxide', 'x': 48, 'y': 50, 
	  'base_url': 'http://www.earthclinic.com/CURES/sore_throat' }, 
	{ 'ailment': 'Sore Throat', 'remedy': 'Tabasco Sauce', 'x': 59, 'y': 62, 
	  'base_url': 'http://www.earthclinic.com/CURES/sore_throat' }, 
	{ 'ailment': 'Sore Throat', 'remedy': 'Cayenne Pepper Recipes', 'x': 41, 'y': 43, 
	  'base_url': 'http://www.earthclinic.com/CURES/sore_throat' }, 
	{ 'ailment': 'Sore Throat', 'remedy': 'Iodine Painting', 'x': 50, 'y': 51, 
	  'base_url': 'http://www.earthclinic.com/CURES/sore_throat' }, 
	{ 'ailment': 'Sore Throat', 'remedy': 'Ginger', 'x': 44, 'y': 46, 
	  'base_url': 'http://www.earthclinic.com/CURES/sore_throat' }, 
	{ 'ailment': 'Sore Throat', 'remedy': 'Garlic', 'x': 44, 'y': 45, 
	  'base_url': 'http://www.earthclinic.com/CURES/sore_throat' }, 
	{ 'ailment': 'Sore Throat', 'remedy': 'Hot Sauce', 'x': 46, 'y': 48, 
	  'base_url': 'http://www.earthclinic.com/CURES/sore_throat' }, 
	{ 'ailment': 'Sore Throat', 'remedy': 'Lemon', 'x': 51, 'y': 53, 
	  'base_url': 'http://www.earthclinic.com/CURES/sore_throat' }, 
	{ 'ailment': 'Sore Throat', 'remedy': 'Mouthwash', 'x': 52, 'y': 53, 
	  'base_url': 'http://www.earthclinic.com/CURES/sore_throat' }, 
	{ 'ailment': 'Sore Throat', 'remedy': 'Vinegar', 'x': 62, 'y': 64, 
	  'base_url': 'http://www.earthclinic.com/CURES/sore_throat' }, 
	{ 'ailment': 'Sore Throat', 'remedy': 'Hot Tea', 'x': 47, 'y': 49, 
	  'base_url': 'http://www.earthclinic.com/CURES/sore_throat' }, 
	{ 'ailment': 'Sore Throat', 'remedy': 'Cloves', 'x': 42, 'y': 44, 
	  'base_url': 'http://www.earthclinic.com/CURES/sore_throat' }, 
	{ 'ailment': 'Sore Throat', 'remedy': 'Vicks Vapor Rub', 'x': 62, 'y': 63, 
	  'base_url': 'http://www.earthclinic.com/CURES/sore_throat' }, 
	{ 'ailment': 'Sore Throat', 'remedy': 'Hand Therapy', 'x': 45, 'y': 47, 
	  'base_url': 'http://www.earthclinic.com/CURES/sore_throat' }, 
	{ 'ailment': 'Sore Throat', 'remedy': 'Oregano Oil', 'x': 53, 'y': 54, 
	  'base_url': 'http://www.earthclinic.com/CURES/sore_throat' }, 

	{ 'ailment': 'White Tongue', 'remedy': 'Salt', 'x': 3, 'y': 6, 
	  'base_url': 'http://www.earthclinic.com/CURES/tongue' } 
]

# manually delete reviews not for remedy in SQL that are scraped as full page is scraped

def scrape_page(diction):
	name = diction['ailment']

	newailment = models.Ailment.query.filter_by(name = name).first()
	if newailment is None:
		timestamp = datetime.now()
		body = 	'Add body from webpage manually in SQL here.'
		newailment = models.Ailment(name = name, timestamp = timestamp, body = body)
		db.session.add(newailment)
		db.session.commit()
		db.session.refresh(newailment)

	name = diction['remedy']

	newremedy = models.Remedy.query.filter_by(name = name).first()
	if newremedy is None:
		timestamp = datetime.now()
		body = 	'Add body from webpage manually in SQL here.'
		newremedy = models.Remedy(name = name, timestamp = timestamp, body = body)
		db.session.add(newremedy)
		db.session.commit()
		db.session.refresh(newremedy)

	newailmenttoremedy = models.AilmentToRemedy(ailment_id = newailment.id, remedy_id = newremedy.id)
	#if newailmenttoremedy is None:
	db.session.add(newailmenttoremedy)
	db.session.commit()

	for i in range(diction['x'], diction['y']): 
		base_url = diction['base_url']
		all_urls = base_url + str(i) + '.html'
		d = pq(url = all_urls) 

		div = d('#content-inner2 > div:nth-child(1) > div')

		for i in range(0, len(div)+1):

			p = pq(d('#content-inner2 > div:nth-child(1) > div:nth-child(' + str(i) + ') > p[align=left]')) 

			if p.text() is not None:
				if p.text().strip()[0] == '[':
					try:
						review   = p.text()
						vote     = review.split(']', 1)[0] 
						review   = review.split(']', 1)[1]
						date     = review.split(':', 1)[0]
						date     = date.strip()
						date     = datetime.strptime(date, '%m/%d/%Y')
						review   = review.split(':', 1)[1]
						username = review.split(':', 1)[0]
						review   = review.split(':', 1)[1] 
					except:
						pass
					else:
						vote     = vote.replace('[', '').strip()
						username = username.strip()
						review   = review.strip(' "') 

						newuser = models.User.query.filter_by(nickname = username).first()
						if newuser is None:
							newuser = models.User(nickname = username)
							db.session.add(newuser)
							db.session.commit()
							db.session.refresh(newuser)

						newpost = models.Post(user_id = newuser.id, nickname = username, 
							timestamp = date, body = review, category_str = vote, ailmenttoremedy_id = newailmenttoremedy.id)
						db.session.add(newpost)

		db.session.commit() 

for i in pages:
	print 'Processing ' + i['ailment'],
	scrape_page(i)
	print 'OK'