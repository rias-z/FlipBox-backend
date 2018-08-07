from sqlalchemy import Column, Integer, String

from app.models import Base, row_to_dict, session_scope


class University(Base):
    __tablename__ = 'university'

    university_id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    name = Column(String(length=256), nullable=False)
    domain = Column(String(length=256), nullable=False)

    @classmethod
    def all(cls):
        with session_scope() as session:
            rows = session.query(cls).all()

            return [row_to_dict(row) for row in rows]

    @classmethod
    def get(cls, university_id):
        with session_scope() as session:
            rows = session.query(cls).filter(
                cls.university_id == university_id
            ).first()

            if not rows:
                return None

            return row_to_dict(rows)
