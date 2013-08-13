#!flask/bin/python

from app import db, models

# turns yea, nay string (Post.vote) into corresponding list index integer (Post.category)

allposts = models.Post.query.all()

for post in allposts:
	if post.category != None:
		continue
	if post.vote in models.post_categories:
		post.category = models.post_categories.index(post.vote)
	else:
		print "bad category %r" % post.vote

db.session.commit()
