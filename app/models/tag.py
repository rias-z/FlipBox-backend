from sqlalchemy import Column, Integer, String

from app.models import Base, row_to_dict, session_scope


class Tag(Base):
    __tablename__ = 'tag'

    tag_id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    name = Column(String(length=64), nullable=False)
    tag_cnt = Column(Integer, nullable=False)

    @classmethod
    def get_all(cls):
        with session_scope() as session:
            rows = session.query(cls).all()

            result = [row_to_dict(row) for row in rows]

            return result
