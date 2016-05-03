from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer
from sqlalchemy.orm import relationship

from blueshed.micro.orm.orm_utils import Base


class User(Base):
    id      = Column(Integer, primary_key=True)
    email   = Column(String(255), unique=True, nullable=False)
    streams = relationship('Stream',
                           uselist=True,
                           primaryjoin='User.id==Stream.user_id',
                           remote_side='Stream.user_id',
                           back_populates='user',
                           cascade='all, delete-orphan')
