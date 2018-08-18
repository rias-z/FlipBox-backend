from datetime import datetime, timedelta, timezone
from sqlalchemy import Column, DateTime, Integer, String

from app.models import Base, row_to_dict, session_scope


JST = timezone(timedelta(hours=+9), 'JST')


class ProvisionalUser(Base):
    __tablename__ = 'provisional_user'

    provisional_user_id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    email = Column(String(length=256), nullable=False)
    login_token = Column(String(length=256), nullable=False)
    create_at = Column(DateTime, nullable=False)

    @classmethod
    def all(cls):
        with session_scope() as session:
            rows = session.query(cls).all()

            return [row_to_dict(row) for row in rows]

    @classmethod
    def get(cls, provisional_user_id):
        with session_scope() as session:
            rows = session.query(cls).filter(
                cls.provisional_user_id == provisional_user_id
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
    def delete(cls, provisional_user_id):
        with session_scope() as session:
            rows = session.query(cls).filter(
                cls.provisional_user_id == provisional_user_id
            )
            session.delete(rows)

