from sqlalchemy import Column, Integer, ForeignKey, DateTime, String

from app.models import Base, row_to_dict, session_scope
from app.models.flip import Flip
from app.models.user import User


class Bookmark(Base):
    __tablename__ = 'bookmark'

    bookmark_id = Column(
        Integer,
        primary_key=True,
        nullable=False,
    )
    user_id = Column(
        Integer,
        ForeignKey(User.user_id),
        nullable=False,
        index=True
    )
    flip_id = Column(
        String(length=64),
        ForeignKey(Flip.flip_id),
        nullable=False,
        index=True
    )
    order_id = Column(Integer)
    create_at = Column(DateTime, nullable=False)

    @classmethod
    def all(cls):
        with session_scope() as session:
            rows = session.query(cls).all()

            return [row_to_dict(row) for row in rows]

    @classmethod
    def get(cls, bookmark_id):
        with session_scope() as session:
            rows = session.query(cls).filter(
                cls.bookmark_id == bookmark_id
            ).first()

            if not rows:
                return None

            return row_to_dict(rows)

    @classmethod
    def post(cls, params):
        with session_scope() as session:
            data = cls(
                **params
            )
            session.add(data)
            session.commit()
            return row_to_dict(data)

    @classmethod
    def put(cls, params):
        with session_scope() as session:
            data = cls(
                **params
            )

            # mergeして1回commit
            session.merge(data)
            session.commit()
            return row_to_dict(data)

    @classmethod
    def delete(cls, bookmark_id):
        with session_scope() as session:
            rows = session.query(cls).filter(
                cls.bookmark_id == bookmark_id
            )
            session.delete(rows)

