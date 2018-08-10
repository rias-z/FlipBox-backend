from sqlalchemy import Column, Integer, ForeignKey, String

from app.models import Base, row_to_dict, session_scope
from app.models.flip import Flip
from app.models.item import Item


class FlipItem(Base):
    __tablename__ = 'flip_item'

    flip_item_id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    flip_id = Column(
        String(length=64),
        ForeignKey(Flip.flip_id),
        nullable=False
    )
    item_id = Column(
        Integer,
        ForeignKey(Item.item_id),
        nullable=False
    )

    @classmethod
    def all(cls):
        with session_scope() as session:
            rows = session.query(cls).all()

            return [row_to_dict(row) for row in rows]

