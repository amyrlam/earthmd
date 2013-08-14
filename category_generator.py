#!flask/bin/python

from app import db, models

# turns yea, nay string (Post.vote) into corresponding list index integer (Post.category)

allposts = models.Post.query.all()

for post in allposts:
	if post.category_str != None:
		continue
	if post.category_int in models.post_categories:
		post.category_str = models.post_categories.index(post.category_int)
	else:
		print "bad category %r" % post.category_int

db.session.commit()
