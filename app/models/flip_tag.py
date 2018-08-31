from sqlalchemy import Column, Integer, ForeignKey, String

from app.models import Base, row_to_dict, session_scope
from app.models.flip import Flip
from app.models.tag import Tag


class FlipTag(Base):
    __tablename__ = 'flip_tag'

    flip_tag_id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    flip_id = Column(
        String(length=64),
        ForeignKey(Flip.flip_id),
        nullable=False,
        index=True
    )
    tag_id = Column(
        Integer,
        ForeignKey(Tag.tag_id),
        nullable=False,
        index=True
    )

    @classmethod
    def all(cls):
        with session_scope() as session:
            rows = session.query(cls).all()

            return [row_to_dict(row) for row in rows]

    @classmethod
    def get(cls, flip_tag_id):
        with session_scope() as session:
            rows = session.query(cls).filter(
                cls.flip_tag_id == flip_tag_id
            ).first()

            if not rows:
                return None

            return row_to_dict(rows)

    @classmethod
    def get_by_flip_id(cls, flip_id):
        with session_scope() as session:
            rows = session.query(Tag).join(cls).filter(
                cls.flip_id == flip_id
            )

            if not rows:
                return None

            result = [row_to_dict(row) for row in rows]

            return result

    @classmethod
    def get_by_flips_by_tag_id(cls, tag_id):
        with session_scope() as session:
            rows = session.query(Flip).join(cls).filter(
                cls.tag_id == tag_id
            )

            if not rows:
                return None

            result = [row_to_dict(row) for row in rows]

            return result

    @classmethod
    def post(cls, params):
        with session_scope() as session:
            data = cls(
                **params
            )
            session.add(data)
            session.commit()
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
    def delete(cls, flip_tag_id):
        with session_scope() as session:
            rows = session.query(cls).filter(
                cls.flip_tag_id == flip_tag_id
            )
            session.delete(rows)

