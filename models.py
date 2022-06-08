from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType
from databases import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(Text)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    orders = relationship("Order", back_populates='user')

    def __repr__(self):
        return f'{self.username}'

class Order(Base):
    __tablename__ = 'orders'

    ORDER_STATUS = (
        ("PENDING", "pending"),
        ("IN-TRANSIT", "in-transit"),
        ("DELIVERED", "delivered")
    )

    FLAVOURS_CHOICES = (
        ("PEPPERONI", "pepperoni"),
        ("CHEESE", "cheese"),
        ("BACON", "bacon")
    )

    SIZES_CHOICES = (
        ("SMALL", "small"),
        ("MEDIUM", "medium"),
        ("LARGE", "large")
    )

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    order_status = Column(ChoiceType(choices=ORDER_STATUS), default='pending')
    flavour = Column(ChoiceType(choices=FLAVOURS_CHOICES))
    size = Column(ChoiceType(choices=SIZES_CHOICES))

    user = relationship("User", back_populates='orders')
    
    def __repr__(self):
        return f'{self.quantity} of {self.flavour["value"] - {self.user}}'