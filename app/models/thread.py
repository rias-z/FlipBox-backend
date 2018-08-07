from datetime import datetime, timedelta, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from app.config import current_config
from app.models import Base, row_to_dict, session_scope
from app.models.category import Category


JST = timezone(timedelta(hours=+9), 'JST')


class Thread(Base):
    __tablename__ = 'thread'

    thread_id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    title = Column(String(length=256), nullable=False)
    create_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S.%f')
    )
    update_at = Column(
        DateTime,
        nullable=False,
        default=datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S.%f')
    )
    speed = Column(Integer, nullable=True, default=0)
    comment_count = Column(Integer, nullable=True, default=0)
    category_id = Column(
        Integer,
        ForeignKey(Category.category_id),
        nullable=False,
    )

    @classmethod
    def get(cls, thread_id):
        '''threadとthread_idに紐づくcomment取得
        '''
        from app.models.comment import Comment

        with session_scope() as session:
            # thread取得
            t_rows = session.query(cls).filter(
                cls.thread_id == thread_id
            ).first()

            if not t_rows:
                return None

            # thread_idに紐づくcommentリスト取得
            comments = Comment.get_all_by_t_id(thread_id)

            result = {
                'thread': row_to_dict(t_rows),
                'comments': comments,
            }

            return result

    @classmethod
    def get_all(cls):
        '''すべてのthread情報取得
        '''
        with session_scope() as session:
            rows = session.query(cls).all()

            result = [row_to_dict(row) for row in rows]

            return result

    @classmethod
    def get_all_by_c_id(cls, category_id, sort_id, paging):
        '''category_idに紐づくthreadリスト取得
        '''
        with session_scope() as session:
            query = session.query(
                cls
            ).join(
                Category, Thread.category_id == Category.category_id
            ).filter(
                Category.category_id == category_id
            )

            # sort
            if sort_id == current_config().get('ID_ASC'):
                # ID昇順
                pass
            elif sort_id == current_config().get('ID_DESC'):
                # ID降順
                query = query.order_by(cls.thread_id.desc())
            elif sort_id == current_config().get('SPEED_DESC'):
                # 人気高い順
                query = query.order_by(cls.speed.desc())
            elif sort_id == current_config().get('SPEED_ASC'):
                # 人気低い順
                query = query.order_by(cls.speed.asc())
            elif sort_id == current_config().get('NUM_COMMENT_DESC'):
                # コメント数多い順
                query = query.order_by(cls.thread_id.desc())
            elif sort_id == current_config().get('NUM_COMMENT_ASC'):
                # コメント数少ない順
                query = query.order_by(cls.thread_id.asc())

            # paging
            # ex)
            # 1. offset=0, limit=10
            # 2. offset=10, limit=20

            # pagingバリデーション
            if paging <= 0:
                paging = 1

            offset = (paging - 1) * 10
            limit = 10

            query_range = query.offset(offset).limit(limit)

            rows = query_range.all()

            # threadが取得できなかった場合
            # 1. threadが1つ以上取得できる場合，最後のpagingのthreadリストを返却
            # 2. threadが0の場合，[]を返却
            if not rows:
                # category_idに紐づくすべてのthread取得
                rows = query.all()

                # それでもthreadが取得できない場合
                if not rows:
                    return []

                result = []

                count = len(rows)

                # threadリストを逆順にしてpaging区切りのthreadをまとめて返却
                for row in list(reversed(rows)):
                    if count == 0 or count % 10 == 0:
                        break

                    result.append(row_to_dict(row))

                    count = count - 1

                return result

            result = [row_to_dict(row) for row in rows]

            return result

    @classmethod
    def get_by_title(cls, title):
        with session_scope() as session:
            rows = session.query(
                cls
            ).join(
                Category, cls.category_id == Category.category_id
            ).filter(
                cls.title.like(title + '%')
            )

            result = [row_to_dict(row) for row in rows]

            return result

    @classmethod
    def post(cls, title, category_id, params=None):
        # length_check
        if len(title) > 40:
            raise Exception('over title length')

        with session_scope() as session:
            if not params:
                data = cls(
                    title=title,
                    category_id=category_id,
                    create_at=datetime.now(JST).strftime(
                        '%Y-%m-%d %H:%M:%S.%f'
                    ),
                    update_at=datetime.now(JST).strftime(
                        '%Y-%m-%d %H:%M:%S.%f'
                    ),
                )
            else:
                if not params.get('create_at'):
                    params.update({
                        'create_at':
                        datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S.%f')
                        }
                    )

                if not params.get('update_at'):
                    params.update({
                        'update_at':
                            datetime.now(JST).strftime('%Y-%m-%d %H:%M:%S.%f')
                        }
                    )

                data = cls(
                    title=title,
                    category_id=category_id,
                    **params
                )
            session.add(data)
            session.flush()

            # threadのspeed計算処理
            cls._update_speed(session=session)

            return row_to_dict(data)

    @classmethod
    def delete(cls, thread_id):
        from app.models.comment import Comment

        with session_scope() as session:
            # thread_idに紐づくcomment削除
            c_rows = session.query(
                Comment
            ).filter(
                cls.thread_id == thread_id
            ).all()

            # thread_idに紐づくcommentの削除
            if c_rows:
                for row in c_rows:
                    session.delete(row)

            # threadの削除
            t_row = session.query(cls).filter_by(thread_id=thread_id).first()

            if not t_row:
                raise Exception('thread not found')

            session.delete(t_row)

    @classmethod
    def _update_speed(cls, session=None):
        '''新しいthread投稿時，全てのthreadのspeedを計算する
        '''
        rows = session.query(
            cls.thread_id,
            cls.create_at,
            cls.update_at,
            cls.comment_count
        ).all()

        for r in rows:
            # 更新時間と作成時間の差
            latest_delta = r.update_at - r.create_at

            if latest_delta != timedelta(0):
                # 現在時刻と更新時間の差
                current_delta = datetime.now(JST).strftime(
                    '%Y-%m-%d %H:%M:%S.%f'
                ) - r.update_at

                # (コメント数 / 現在時刻秒数) * 100
                speed = (
                    r.comment_count / current_delta.total_seconds()
                ) * 1000

                data = cls(
                    thread_id=r.thread_id,
                    speed=speed
                )

                session.merge(data)
