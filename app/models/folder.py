from sqlalchemy import Column, Integer, ForeignKey, String

from app.models import Base, row_to_dict, session_scope
from app.models.bookmark import Bookmark
from app.models.user import User


class Folder(Base):
    __tablename__ = 'folder'

    folder_id = Column(
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
    bookmark_id = Column(
        Integer,
        ForeignKey(Bookmark.bookmark_id),
        nullable=False
    )
    order_id = Column(Integer)
    title = Column(String(length=512), nullable=False)
    
    @classmethod
    def all(cls):
        with session_scope() as session:
            rows = session.query(cls).all()

            return [row_to_dict(row) for row in rows]

