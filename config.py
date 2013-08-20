import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Flast-WTF extension config
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
	{ 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' }]
	#{ 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]

SQLALCHEMY_DATABASE_URI = 'postgresql://amyrlam@localhost/earthmd_db'

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
WHOOSH_BASE = os.path.join(basedir, 'search.db')

#? update below with own info how
# email server
MAIL_SERVER = 'localhost' # 'smtp.googlemail.com'
MAIL_PORT = 25 # 465
MAIL_USE_TSL = False
MAIL_USE_SSL = False # True
MAIL_USERNAME = None # 'your-gmail-username'
MAIL_PASSWORD = None # 'your-gmail-password'

# administrator list
ADMINS = ['hello@amyrlam.com']

# pagination
POSTS_PER_PAGE = 3
MAX_SEARCH_RESULTS = 50