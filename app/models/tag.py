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
    name = Column(String(length=64), nullable=False, unique=True)
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
    def get_by_tag_name(cls, tag_name):
        with session_scope() as session:
            rows = session.query(cls).filter(
                cls.name == tag_name
            ).first()

            if not rows:
                return None

            return row_to_dict(rows)


    @classmethod
    def post(cls, params):
        with session_scope() as session:
            tag = cls.is_exist_by_name(params.get('name'))
            if tag is not None:
                return tag
            else:
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
    def delete(cls, tag_id):
        with session_scope() as session:
            rows = session.query(cls).filter(
                cls.tag_id == tag_id
            )
            session.delete(rows)

    @classmethod
    def is_exist_by_name(cls, name):
        '''同じメールのユーザが存在するかどうかをboolで返却
        Args:
            name:  名前
        Returns:
            bool:
        '''
        with session_scope() as session:
            tags = session.query(
                cls
            ).filter(
                cls.name == name
            )

            if tags.count() > 0:
                return row_to_dict(tags.first())
            else:
                return None

