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

