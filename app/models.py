from hashlib import md5
from app import db
from app import app
import flask.ext.whooshalchemy as whooshalchemy

ROLE_USER = 0
ROLE_ADMIN = 1

followers = db.Table('followers',
	db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
	db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)

post_categories = ['YEA', 'NAY', 'BETTER BUT NOT CURED', 'WORKED TEMPORARILY', 'BETTER BUT WITH SIDE EFFECTS', 
					'SIDE EFFECTS', 'WARNING!', 'QUESTION']

# "user" is a reserved word in postgres so changed table name to "users"

class User(db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key = True)
	nickname = db.Column(db.String(64), unique = True)
	email = db.Column(db.String(120), index = True, unique = True) # duplicate to Post nickname
	role = db.Column(db.SmallInteger, default = ROLE_USER)
	
	posts = db.relationship('Post', backref = 'author', lazy = 'dynamic') # should this not show up in psql users? yes it is a join
	
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime)
	followed = db.relationship('User',
		secondary = followers,
		primaryjoin = (followers.c.follower_id == id),
		secondaryjoin = (followers.c.followed_id ==id),
		backref = db.backref('followers', lazy = 'dynamic'),
		lazy = 'dynamic')

	@staticmethod
	def make_unique_nickname(nickname):
		if User.query.filter_by(nickname = nickname).first() == None:
			return nickname
		version = 2
		while True:
			new_nickname = nickname + str(version)
			if User.query.filter_by(nickname = new_nickname).first() == None:
				break
			version += 1
		return new_nickname

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def avatar(self, size):
		return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)
			return self

	def unfollow(self, user):
		if self.is_following(user):
			self.followed.remove(user)
			return self

	def is_following(self, user):
		return self.followed.filter(followers.c.followed_id == user.id).count() > 0

	def followed_posts(self):
		return Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id).order_by(Post.timestamp.desc())			

class Post(db.Model):
	__tablename__ = "post"
	__searchable__ = ['body']

	id = db.Column(db.Integer, primary_key = True)
	ailmenttoremedy_id = db.Column(db.Integer, db.ForeignKey('ailmenttoremedy.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	nickname = db.Column(db.String) # delete this column later, duplicate to User nickname
	timestamp = db.Column(db.DateTime)
	
	category_str = db.Column(db.String) 
	category_int = db.Column(db.Integer) # see post_categories above

	score = db.Column(db.Integer)
	votes = db.relationship('Vote', backref = 'post', lazy = 'dynamic') # can call vote.post in views.py

	body = db.Column(db.String)

	def vote_on_post(self, vote):
		v = Vote(post_id=self.id, user_id = current_user.id, vote = vote)
		self.score += vote
		session.add(v)
		session.commit(v)

class Ailment(db.Model):
	__tablename__ = "ailment"
	__searchable__ = ['body'] # keep this here?

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(140))
	body = db.Column(db.String) # blank for now
	timestamp = db.Column(db.DateTime)

class Remedy(db.Model):
	__tablename__ = "remedy"
	__searchable__ = ['body'] # keep this here?

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(140))
	body = db.Column(db.String) # blank for now
	timestamp = db.Column(db.DateTime)

class AilmentToRemedy(db.Model):
	__tablename__ = "ailmenttoremedy"

	id = db.Column(db.Integer, primary_key = True)
	ailment_id = db.Column(db.Integer, db.ForeignKey('ailment.id'))
	remedy_id = db.Column(db.Integer, db.ForeignKey('remedy.id'))

class Vote(db.Model):
	__tablename__ = "vote"

	id = db.Column(db.Integer, primary_key = True)
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	vote = db.Column(db.Integer)

	#__table_args__ = (db.UniqueConstraint('post_id', 'user_id', name='vote_post_user_unq'),) 
	# not working here, inserted directly into psql

whooshalchemy.whoosh_index(app, Post) # is this full text, which won't work with heroku