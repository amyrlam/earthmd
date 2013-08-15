from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid 
from forms import LoginForm, EditForm, PostForm, SearchForm
from models import User, ROLE_USER, ROLE_ADMIN, Post, Remedy, Ailment, AilmentToRemedy, post_categories, Vote
from datetime import datetime
from config import POSTS_PER_PAGE, MAX_SEARCH_RESULTS
from emails import follower_notification

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.before_request
def before_request():
	g.user = current_user 
	if g.user.is_authenticated():
		g.user.last_seen = datetime.utcnow()
		db.session.add(g.user)
		db.session.commit()
		g.search_form = SearchForm()

@app.errorhandler(404)
def internal_error(error):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
@app.route('/index/<int:page>', methods = ['GET', 'POST'])
@login_required
def index(page = 1):
	form = PostForm()
	if form.validate_on_submit():
		post = Post(body = form.post.data, timestamp = datetime.utcnow(), author = g.user)
		db.session.add(post)
		db.session.commit()
		flash('Your post is now live!')
		return redirect(url_for('index'))
	posts = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False)
	return render_template('index.html',
		title = 'Home',
		form = form,
		posts = posts)

@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		session['remember_me'] = form.remember_me.data
		return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
	return render_template('login.html',
		title = 'Sign In',
		form = form,
		providers = app.config['OPENID_PROVIDERS'])

@oid.after_login
def after_login(resp):
	if resp.email is None or resp.email == "":
		flash('Invalid login. Please try again.')
		return redirect(url_for('login'))
	user = User.query.filter_by(email=resp.email).first()
	if user is None:
		nickname = resp.nickname
		if nickname is None or nickname == "":
			nickname = resp.email.split('@')[0]
		user = User(nickname=nickname, email=resp.email, role=ROLE_USER)
		db.session.add(user)
		db.session.commit()
		# make the user follow him/herself
		db.session.add(user.follow(user))
		db.session.commit()
	remember_me = False
	if 'remember_me' in session:
		remember_me = session['remember_me']
		session.pop('remember_me', None)
	login_user(user, remember=remember_me)
	return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/user/<nickname>')
@app.route('/user/<nickname>/<int:page>')
@login_required
def user(nickname, page = 1):
	user = User.query.filter_by(nickname=nickname).first()
	if user == None:
		flash('User ' + nickname + ' not found.')
		return redirect(url_for('index'))
	posts = user.posts.paginate(page, POSTS_PER_PAGE, False) # is this pagination working?
	return render_template('user.html',
		user=user,
		posts=posts)

@app.route('/edit', methods = ['GET', 'POST'])
@login_required
def edit():
	form = EditForm(g.user.nickname)
	if form.validate_on_submit():
		g.user.nickname = form.nickname.data
		g.user.about_me = form.about_me.data
		db.session.add(g.user)
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('edit'))
	else:
		form.nickname.data = g.user.nickname
		form.about_me.data = g.user.about_me
	return render_template('edit.html', form=form)

@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
	user = User.query.filter_by(nickname=nickname).first()
	if user == None:
		flash('User ' + nickname + ' not found.')
		return redirect(url_for('index'))
	if user == g.user:
		flash('You can\'t follow yourself!')
		return redirect(url_for('user', nickname=nickname))
	u = g.user.follow(user)
	if u is None:
		flash('Cannot follow ' + nickname + '.')
		return redirect(url_for('user', nickname=nickname))
	db.session.add(u)
	db.session.commit()
	flash('Your are now following ' + nickname + '!')
	follower_notification(user, g.user)
	return redirect(url_for('user', nickname=nickname))

@app.route('/unfollow/<nickname>')
def unfollow(nickname):
	user = User.query.filter_by(nickname=nickname).first()
	if user == None:
		flash('User ' + nickname + ' not found.')
		return redirect(url_for('index'))
	if user == g.user:
		flash('You can\'t unfollow yourself!')
		return redirect(url_for('user', nickname=nickname))
	u = g.user.unfollow(user)
	if u is None:
		flash('Cannot unfollow ' + nickname + '.')
		return redirect(url_for('user', nickname=nickname))
	db.session.add(u)
	db.session.commit()
	flash('You have stopped following ' + nickname + '.')
	return redirect(url_for('user', nickname=nickname))

@app.route('/search', methods = ['POST'])
@login_required
def search():
	if not g.search_form.validate_on_submit():
		return redirect(url_for('index'))
	return redirect(url_for('search_results', query=g.search_form.search.data))

@app.route('/search_results/<query>')
@login_required
def search_results(query):
	results = Post.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
	return render_template('search_results.html',
		query = query,
		results = results)

@app.route('/ailments')
def ailments():
	ailments = Ailment.query.all() # every row and column in ailments, sqlalchemy usually returns every col
	return render_template('ailments.html', ailments=ailments)

@app.route('/ailment/<ailment_id>')
def ailment(ailment_id):
	ailment = Ailment.query.get_or_404(ailment_id) # get returns one

	ailmenttoremedies = AilmentToRemedy.query.filter_by(ailment_id=ailment.id).all()  
	
	remedies = []
	for row in ailmenttoremedies:
		remedy = Remedy.query.get(row.remedy_id)
		# print remedy.name 
		remedies.append(remedy)

	return render_template('ailment.html', ailment=ailment, remedies=remedies)

def lookup_pair(ailment_id, remedy_id):
	ailment = Ailment.query.get_or_404(ailment_id)
	remedy = Remedy.query.get_or_404(remedy_id)
	ailmenttoremedy = AilmentToRemedy.query.filter_by(ailment_id=ailment.id, remedy_id=remedy.id).first()
	return (ailment, remedy, ailmenttoremedy)

@app.route('/posts/<ailment_id>/<remedy_id>')
def posts(ailment_id, remedy_id):
	ailment, remedy, ailmenttoremedy = lookup_pair(ailment_id, remedy_id)

	# if ailmenttoremedyid == None: # correct?
	# return render_template('404.html')

	# SELECT user_id, category_str, rank() OVER (PARTITION BY category_str ORDER BY score DESC) FROM post LIMIT 5;
	# score = session.having(func.count(Vote.vote))
	# print score
	
	# how to write strings in sqlalchemy 
	# SELECT nickname, timestamp, category_str, body, rank() OVER (PARTITION BY category_str ORDER BY timestamp DESC) FROM post LIMIT 5;

	posts = Post.query.filter_by(ailmenttoremedy_id = ailmenttoremedy.id)
	
	# .order_by("category_int") #.paginate(1, POSTS_PER_PAGE, False)
	return render_template('posts.html', ailment=ailment, remedy=remedy, posts=posts, post_categories=post_categories)

@app.route('/vote', methods = ['POST'])
def vote():
	print "We're here!"
	if request.form.get("vote") == "up": # expression == returns True, if != returns False
		vote_input = 1 # upvote
	else:
		vote_input = -1 # downvote
	post_id = request.form.get("post_id")
	vote = Vote(post_id=post_id, user_id=g.user.id, vote=vote_input) # limit user from voting twice with an if statement
	
	# change upvote to green if successful?
	# if user upvotes a post, can't downvote it how?
	# see unique constraint in models.Vote

	db.session.add(vote)
	db.session.commit()
	return "Vote recorded!"

@app.route('/posts/<ailment_id>/<remedy_id>/new', methods = ['GET', 'POST'])
def newpost(ailment_id, remedy_id):
	ailment, remedy, ailmenttoremedy = lookup_pair(ailment_id, remedy_id)
	form = PostForm(request.form)
	if form.validate_on_submit():
		print "branch1"
		# why / how can i use author here? see flask mega
		post = Post(category_str=form.category.data, body=form.body.data, timestamp=datetime.utcnow(), author=g.user, 
					ailmenttoremedy_id=ailmenttoremedy.id)
		db.session.add(post)
		db.session.commit()
		flash('Your post is now live!')
		return redirect(url_for('posts', ailment_id=ailment.id, remedy_id=remedy.id))
	else:
		print "branch2: %r" % (form.errors,)
		return render_template('post_new.html', form=form)
	
@app.route('/remedies/')
def remedies():
	remedies = Remedy.query.all()
	return render_template('remedies.html', remedies=remedies)

@app.route('/remedy/<remedy_id>')
def remedy(remedy_id):
	remedy = Remedy.query.get_or_404(remedy_id)

	ailmenttoremedies = AilmentToRemedy.query.filter_by(remedy_id=remedy.id).all()

	ailments = []
	for row in ailmenttoremedies:
		ailment = Ailment.query.get(row.ailment_id)
		ailments.append(ailment)

	return render_template('remedy.html', remedy=remedy, ailments=ailments)

def lookup_pair(ailment_id, remedy_id):
	ailment = Ailment.query.get_or_404(ailment_id)
	remedy = Remedy.query.get_or_404(remedy_id)
	ailmenttoremedy = AilmentToRemedy.query.filter_by(ailment_id=ailment.id, remedy_id=remedy.id).first()
	return (ailment, remedy, ailmenttoremedy)


























