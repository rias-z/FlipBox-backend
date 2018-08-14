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
    def all(cls):
        with session_scope() as session:
            rows = session.query(cls).all()

            return [row_to_dict(row) for row in rows]

    @classmethod
    def get(cls, tag_id):
        with session_scope() as session:
            rows = session.query(cls).filter(
                cls.tag_id == tag_id
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
    def delete(cls, tag_id):
        with session_scope() as session:
            rows = session.query(cls).filter(
                cls.tag_id == tag_id
            )
            session.delete(rows)

