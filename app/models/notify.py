from sqlalchemy import Column, Integer, ForeignKey, String, DateTime

from app.models import Base, row_to_dict, session_scope
from app.models.flip import Flip


class Notify(Base):
    __tablename__ = 'notify'

    notify_id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    content = Column(String(length=512), nullable=False)
    receive_user_id = Column(Integer, nullable=False, index=True)
    send_user_id = Column(Integer, nullable=False)
    flip_id = Column(
        String(length=64),
        ForeignKey(Flip.flip_id),
        nullable=False
    )
    create_at = Column(DateTime, nullable=False)

    @classmethod
    def all(cls):
        with session_scope() as session:
            rows = session.query(cls).all()

            return [row_to_dict(row) for row in rows]

    @classmethod
    def get(cls, notify_id):
        with session_scope() as session:
            rows = session.query(cls).filter(
                cls.notify_id == notify_id
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
    def delete(cls, notify_id):
        with session_scope() as session:
            rows = session.query(cls).filter(
                cls.notify_id == notify_id
            )
            session.delete(rows)

