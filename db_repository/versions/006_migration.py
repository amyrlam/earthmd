from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
ailment__remedy = Table('ailment__remedy', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
)

ailmenttoremedy = Table('ailmenttoremedy', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['ailment__remedy'].drop()
    post_meta.tables['ailmenttoremedy'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['ailment__remedy'].create()
    post_meta.tables['ailmenttoremedy'].drop()
