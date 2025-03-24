# from sqlalchemy import Column, Integer, Boolean, Numeric, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
#
# Base = declarative_base()
#
# class StateNode(Base):
#     __tablename__ = 'state_node'
#
#     id = Column(Integer, primary_key=True, nullable=False)
#     father_id = Column(Integer, ForeignKey('state_node.id'), nullable=True)
#     state = Column(Numeric, nullable=False)
#     value = Column(Integer, nullable=False)
#     height = Column(Integer, nullable=False)


from sqlalchemy import func, Index, Column, String, Numeric
from sqlmodel import SQLModel, Field, Relationship, Text, CHAR
from typing import Optional, List



class StateNode(SQLModel):
    __tablename__ = 'state_node'

    id: Optional[int] = Field(default=None, primary_key=True)
    father_id: int = Field(foreign_key="state_node.id", nullable=True)
    state: str = Field(min_length=64, max_length=64, nullable=False)
    score: int = Field(nullable=False)
    height: int = Field(nullable=False)
    depth: int = Field(nullable=False)
