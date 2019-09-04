from sqlalchemy import Column, ForeignKey, Integer, String, Float
from ..database import Base


class ModelIngredient(Base):
    __tablename__ = "ingredient"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    amount = Column('amount', Float)
    measured_in_id = Column(Integer, ForeignKey("measured_in.id"))

    def __init__(self, name, amount, measured_in_id):
        self.name = name
        self.amount = amount
        self.measured_in_id = measured_in_id
