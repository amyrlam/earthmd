#!flask/bin/python

from app import db, models


print models.post_categories.index('NAY')
# turns yea, nay string (Post.category_str) into corresponding list index integer (Post.category_int)

allposts = models.Post.query.all()

for post in allposts:
	if post.category_str == None:
		print "exists"
		continue
	if post.category_str in models.post_categories: 
		print "change"
		post.category_int = models.post_categories.index(post.category_str)
		db.session.add(post)
	else:
		print "bad category %r" % post.category_str

db.session.commit()
