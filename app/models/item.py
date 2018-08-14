from sqlalchemy import Column, String

from app.models import Base, row_to_dict, session_scope


class Item(Base):
    __tablename__ = 'item'

    item_id = Column(
        String(length=64),
        primary_key=True,
        nullable=False,
        index=True
    )
    url = Column(String(length=2083), nullable=False)
    name = Column(String(length=64), nullable=True)
    description = Column(String(length=512), nullable=True)

    @classmethod
    def all(cls):
        with session_scope() as session:
            rows = session.query(cls).all()

            return [row_to_dict(row) for row in rows]

    @classmethod
    def get(cls, item_id):
        with session_scope() as session:
            row = session.query(cls).filter(
                cls.item_id == item_id
            ).first()

            if not row:
                return None

            return row_to_dict(row)

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
    def delete(cls, item_id):
        with session_scope() as session:
            rows = session.query(cls).filter(
                cls.item_id == item_id
            )
            session.delete(rows)

