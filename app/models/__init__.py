from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import create_dburl


Base = declarative_base()


def row_to_dict(row):
    if row is None:
        return None

    d = {}
    for column in row.__table__.columns:
        d[column.name] = getattr(row, column.name)

    return d


@contextmanager
def session_scope():
    dburl = create_dburl()
    engine = create_engine(dburl)
    Session = sessionmaker(bind=engine)

    session = Session()

    try:
        yield session
        session.commit()
    except: # NOQA
        session.rollback()
        raise
    finally:
        session.close()
