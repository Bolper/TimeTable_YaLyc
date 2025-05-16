import datetime
import sqlalchemy as sa

from .__db_session import SqlAlchemyBase


class Note(SqlAlchemyBase):
    __tablename__ = 'notes'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=None)
    description = sa.Column(sa.String, nullable=True)
    position = sa.Column(sa.String, nullable=True)
    starts = sa.Column(sa.DateTime, nullable=None, default=datetime.datetime.now())
    ends = sa.Column(sa.DateTime, nullable=None, default=(datetime.datetime.now() + datetime.timedelta(hours=1)))
    is_finished = sa.Column(sa.Boolean, nullable=True, default=False)
    modified_date = sa.Column(sa.DateTime, default=datetime.datetime.now())
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
