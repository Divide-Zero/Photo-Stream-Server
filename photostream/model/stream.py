from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer
from sqlalchemy.orm import relationship

from blueshed.micro.orm.orm_utils import Base


class Stream(Base):
    id      = Column(Integer, primary_key=True)
    name    = Column(String(255), unique=True, nullable=False)
    sources = relationship('Source',
                           uselist=True,
                           primaryjoin='Stream.id==Source.stream_id',
                           remote_side='Source.stream_id',
                           back_populates='stream',
                           cascade='all, delete-orphan')
