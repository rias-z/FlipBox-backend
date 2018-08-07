from sqlalchemy import Column, Integer, String

from app.models import Base, row_to_dict, session_scope


class Sort(Base):
    __tablename__ = 'sort'

    sort_id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    name = Column(String(length=256), nullable=False)

    @classmethod
    def get_all(cls):
        with session_scope() as session:
            rows = session.query(cls).all()

            result = [row_to_dict(row) for row in rows]

            return result
