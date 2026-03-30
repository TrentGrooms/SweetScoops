from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

engine = create_engine("sqlite:///orders.db")
Session = sessionmaker(bind=engine)
db_session = Session()

def get_session():
    return db_session

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    customer_name = Column(String, nullable=False)
    flavor = Column(String, nullable=False)
    size = Column(String, nullable=False)
    toppings = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    total = Column(Float, nullable=False)
    card_last_four = Column(String, nullable=False)




