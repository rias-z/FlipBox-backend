from sqlalchemy import Column, Integer, DateTime, ForeignKey

from app.models import Base, row_to_dict, session_scope
from app.models.user import User


class Follow(Base):
    __tablename__ = 'follow'

    follow_id = Column(
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
    follow_user_id = Column(
        Integer,
        ForeignKey(User.user_id),
        nullable=False,
    )
    create_at = Column(DateTime, nullable=False)

    @classmethod
    def all(cls):
        with session_scope() as session:
            rows = session.query(cls).all()

            return [row_to_dict(row) for row in rows]

    @classmethod
    def get(cls, follow_id):
        with session_scope() as session:
            rows = session.query(cls).filter(
                cls.follow_id == follow_id
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
    def delete(cls, follow_id):
        with session_scope() as session:
            rows = session.query(cls).filter(
                cls.follow_id == follow_id
            )
            session.delete(rows)

