from sqlalchemy import Column, String

from app.models import Base, row_to_dict, session_scope


class Item(Base):
    __tablename__ = 'item'

    item_id = Column(String(length=64), primary_key=True, nullable=False, index=True)
    url = Column(String(length=2024), nullable=False, unique=True)
    name = Column(String(length=64), nullable=True)
    description = Column(String(length=512), nullable=True)

    @classmethod
    def get(cls):
        with session_scope() as session:
            rows = session.query(cls).all()

            result = [row_to_dict(row) for row in rows]

            return result
