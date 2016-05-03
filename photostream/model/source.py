from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer

from blueshed.micro.orm.orm_utils import Base


class Source(Base):
    id   = Column(Integer, primary_key=True)
    name = Column('service', String(50), nullable=False)

    __mapper_args__ = {'polymorphic_on': name}


class Twitter(Source):
    __tablename__   = None
    __mapper_args__ = {'polymorphic_identity': 'Twitter'}
