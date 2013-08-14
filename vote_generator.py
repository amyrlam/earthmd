#!flask/bin/python

from app import db, models
import random

allposts = models.Post.query.all() # .filter_by(col_name > x)

allusers = models.User.query.all()

for i in range(0, len(allposts) * 3):
	post = random.choice(allposts) 
	user = random.choice(allusers)
	vote_int = random.randint(0,4)

	if vote_int == 0:
		vote = -1 # downvote
	else:
		vote = 1 # upvote

	newvote = models.Vote(post_id = post.id, user_id = user.id, vote = vote)
	db.session.add(newvote)
	print "%d/%d" % (i, len(allposts) * 3)

db.session.commit()

# print repr(allposts)