from sqlalchemy import Column, Integer, String, Float, ForeignKey
from backend.databases import Base
from sqlalchemy.orm import relationship

class product(Base):
    __tablename__='product'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(100),nullable=False)
    price=Column(Float,nullable=False)
    product_url=Column(String(250))
    QR=Column(String(250))
class User(Base):
    __tablename__='user'
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String(50),nullable=False,unique=True)
    password=Column(String(15),nullable=False)
    role=Column(String(10))
class cart(Base):
    __tablename__='cart'
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey('user.id'))
    product_id=Column(Integer,ForeignKey('product.id'))
    quantity = Column(Integer, default=1)
    user = relationship("User", backref="carts")
    product = relationship("product", backref="carts")



