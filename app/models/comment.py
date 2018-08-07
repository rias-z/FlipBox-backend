from datetime import datetime, timedelta, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.models import Base, session_scope, row_to_dict
from app.models.thread import Thread
from app.models.user import User


JST = timezone(timedelta(hours=+9), 'JST')


class Comment(Base):
    __tablename__ = 'comment'

    comment_id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    thread_id = Column(
        Integer,
        ForeignKey(Thread.thread_id),
        nullable=False,
        index=True
    )
    name = Column(String(length=256), nullable=False)
    text = Column(String(length=256), nullable=False)
    create_at = Column(
        DateTime, nullable=False
    )
    user_id = Column(
        Integer,
        ForeignKey(User.user_id),
        nullable=False,
    )

    @classmethod
    def get_all(cls):
        with session_scope() as session:
            rows = session.query(cls).all()

            result = [row_to_dict(row) for row in rows]

            return result

    @classmethod
    def get_all_by_t_id(cls, thread_id):
        with session_scope() as session:
            rows = session.query(cls).filter(
                cls.thread_id == thread_id
            ).all()

            result = [row_to_dict(row) for row in rows]

            return result

    @classmethod
    def post(cls, params):
        # length_check
        text = params.get('text')
        if len(text) > 200:
            raise Exception('over text length')

        with session_scope() as session:
            if not params.get('create_at'):
                params.update({'create_at': datetime.now(JST)})

            data = cls(**params)
            session.add(data)
            session.flush()

            # thread_idに紐づくthreadのcomment_count加算
            cls.update_thread(
                session=session,
                thread_id=params.get('thread_id')
            )

    @classmethod
    def update_thread(cls, session, thread_id):
        data = Thread(
            thread_id=thread_id,
            comment_count=(Thread.comment_count + 1),
            update_at=datetime.now(JST)
        )

        session.merge(data)
