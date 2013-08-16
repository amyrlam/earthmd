#!flask/bin/python

from app import db, models
import random

allposts = models.Post.query.all() # .filter_by(col_name > x)
allusers = models.User.query.all()

for i in range(0, len(allposts) * 3):
	post = random.choice(allposts) 
	user = random.choice(allusers)
	vote_int = random.randint(0,4)

	# if post, user combo already exists in sql, continue
	# try, database INSERT IGNORE if error

	if models.Vote.query.filter_by(post_id=post.id, user_id=user.id).count() > 0:
		print "duplicate"
		continue
	else:
		if vote_int == 0:
			vote = -1 # downvote
		else:
			vote = 1 # upvote
		newvote = models.Vote(post_id = post.id, user_id = user.id, vote = vote)
		db.session.add(newvote)
		db.session.commit()

	print "%d/%d" % (i, len(allposts) * 3)
