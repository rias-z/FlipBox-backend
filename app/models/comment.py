from sqlalchemy import Column, Integer, ForeignKey, String, DateTime

from app.models import Base, row_to_dict, session_scope
from app.models.flip import Flip
from app.models.user import User


class Comment(Base):
    __tablename__ = 'comment'

    comment_id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
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
        index=True,
    )
    create_at = Column(DateTime, nullable=False)
    content = Column(String(length=512), nullable=False)

    @classmethod
    def all(cls):
        with session_scope() as session:
            rows = session.query(cls).all()

            return [row_to_dict(row) for row in rows]

