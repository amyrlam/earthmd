from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
post = Table('post', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('ailmenttoremedy_id', Integer),
    Column('user_id', Integer),
    Column('nickname', String),
    Column('timestamp', DateTime),
    Column('vote', String),
    Column('body', String),
    Column('down_votes', Integer),
    Column('score', Float),
    Column('up_votes', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post'].columns['down_votes'].drop()
    pre_meta.tables['post'].columns['up_votes'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post'].columns['down_votes'].create()
    pre_meta.tables['post'].columns['up_votes'].create()
