from sqlalchemy import Column, Integer, ForeignKey

from app.models import Base, row_to_dict, session_scope
from app.models.notify import Notify
from app.models.user import User


class UserNotify(Base):
    __tablename__ = 'user_notify'

    user_notify_id = Column(
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
    notify_id = Column(
        Integer,
        ForeignKey(Notify.notify_id),
        nullable=False
    )

    @classmethod
    def all(cls):
        with session_scope() as session:
            rows = session.query(cls).all()

            return [row_to_dict(row) for row in rows]

    @classmethod
    def get(cls, user_notify_id):
        with session_scope() as session:
            rows = session.query(cls).filter(
                cls.user_notify_id == user_notify_id
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
    def delete(cls, user_notify_id):
        with session_scope() as session:
            rows = session.query(cls).filter(
                cls.user_notify_id == user_notify_id
            )
            session.delete(rows)

