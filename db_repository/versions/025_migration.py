from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
ailment = Table('ailment', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=140)),
    Column('body', String),
    Column('timestamp', DateTime),
)

ailmenttoremedy = Table('ailmenttoremedy', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('ailment_id', Integer),
    Column('remedy_id', Integer),
)

followers = Table('followers', post_meta,
    Column('follower_id', Integer),
    Column('followed_id', Integer),
)

post = Table('post', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('ailmenttoremedy_id', Integer),
    Column('user_id', Integer),
    Column('nickname', String),
    Column('timestamp', DateTime),
    Column('category_int', String),
    Column('category_str', Integer),
    Column('score', Integer),
    Column('body', String),
)

remedy = Table('remedy', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=140)),
    Column('body', String),
    Column('timestamp', DateTime),
)

users = Table('users', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('nickname', String(length=64)),
    Column('email', String(length=120)),
    Column('role', SmallInteger, default=ColumnDefault(0)),
    Column('about_me', String(length=140)),
    Column('last_seen', DateTime),
)

vote = Table('vote', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('post_id', Integer),
    Column('user_id', Integer),
    Column('vote', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['ailment'].create()
    post_meta.tables['ailmenttoremedy'].create()
    post_meta.tables['followers'].create()
    post_meta.tables['post'].create()
    post_meta.tables['remedy'].create()
    post_meta.tables['users'].create()
    post_meta.tables['vote'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['ailment'].drop()
    post_meta.tables['ailmenttoremedy'].drop()
    post_meta.tables['followers'].drop()
    post_meta.tables['post'].drop()
    post_meta.tables['remedy'].drop()
    post_meta.tables['users'].drop()
    post_meta.tables['vote'].drop()
