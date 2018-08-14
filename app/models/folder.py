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

    @classmethod
    def get(cls, folder_id):
        with session_scope() as session:
            rows = session.query(cls).filter(
                cls.folder_id == folder_id
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

    @classmethod
    def put(cls, params):
        with session_scope() as session:
            data = cls(
                **params
            )

            # mergeして1回commit
            session.merge(data)
            session.commit()

    @classmethod
    def delete(cls, folder_id):
        with session_scope() as session:
            rows = session.query(cls).filter(
                cls.folder_id == folder_id
            )
            session.delete(rows)

