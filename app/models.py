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

# "user" is a reserved word in postgres so changed table name to "users"

class User(db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key = True)
	nickname = db.Column(db.String(64), unique = True)
	email = db.Column(db.String(120), index = True, unique = True)
	role = db.Column(db.SmallInteger, default = ROLE_USER)
	posts = db.relationship('Post', backref = 'author', lazy = 'dynamic') # should this not show up in psql users?
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
	nickname = db.Column(db.String) # delete this column later
	timestamp = db.Column(db.DateTime)
	vote = db.Column(db.String) # choose from preassigned list of options e.g. yea, nay, better but not cured, etc. 
	up_votes = db.Column(db.Integer)
	down_votes = db.Column(db.Integer)
	score = db.Column(db.Float)
	body = db.Column(db.String)

class Ailment(db.Model):
	__tablename__ = "ailment"
	__searchable__ = ['body'] # keep this here?

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(140))
	body = db.Column(db.String)
	timestamp = db.Column(db.DateTime)

class Remedy(db.Model):
	__tablename__ = "remedy"
	__searchable__ = ['body'] # keep this here?

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(140))
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime)

	def __repr__(self):
		return self.name

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
	vote = db.Column(db.Boolean)

whooshalchemy.whoosh_index(app, Post)