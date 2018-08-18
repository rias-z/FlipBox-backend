from sqlalchemy import Column, Integer, String

from app.models import Base, row_to_dict, session_scope


class User(Base):
    __tablename__ = 'user'

    user_id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    email = Column(String(length=512), nullable=False, unique=True)
    username = Column(String(length=64), nullable=True)
    password = Column(String(length=64), nullable=False)
    description = Column(String(length=512), nullable=True)
    thumbnail = Column(String(length=64), nullable=False)

    @classmethod
    def all(cls):
        with session_scope() as session:
            rows = session.query(cls).all()

            return [row_to_dict(row) for row in rows]

    @classmethod
    def get(cls, user_id):
        with session_scope() as session:
            rows = session.query(cls).filter(
                cls.user_id == user_id
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
    def delete(cls, user_id):
        with session_scope() as session:
            rows = session.query(cls).filter(
                cls.user_id == user_id
            )
            session.delete(rows)

    @classmethod
    def is_exist_by_email(cls, email):
        '''同じメールのユーザが存在するかどうかをboolで返却
        Args:
            email:  学番メール
        Returns:
            bool:
        '''
        with session_scope() as session:
            count = session.query(
                cls
            ).filter(
                cls.email == email
            ).count()

            if count > 0:
                return True
            else:
                return False
