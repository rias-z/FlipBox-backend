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
        String,
        ForeignKey(Flip.flip_id),
        nullable=False
    )
    create_at = Column(DateTime, nullable=False)

    @classmethod
    def all(cls):
        with session_scope() as session:
            rows = session.query(cls).all()

            return [row_to_dict(row) for row in rows]

