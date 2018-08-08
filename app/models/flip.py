from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from app.models import Base, row_to_dict, session_scope
from app.models.user import User


class Flip(Base):
    __tablename__ = 'flip'

    flip_id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        index=True
    )
    title = Column(String(length=64), nullable=False)
    user_id = Column(
        Integer,
        ForeignKey(User.user_id),
        nullable=False
    )
    item_cnt = Column(Integer, nullable=False)
    bookmark_cnt = Column(Integer, nullable=False)
    good_cnt = Column(Integer, nullable=False)
    create_at = Column(DateTime, nullable=False)

    @classmethod
    def all(cls):
        with session_scope() as session:
            rows = session.query(cls).all()

            return [row_to_dict(row) for row in rows]

    @classmethod
    def get(cls, flip_id):
        with session_scope() as session:
            rows = session.query(cls).filter(
                cls.flip_id == flip_id
            ).first()

            if not rows:
                return None

            return row_to_dict(rows)
