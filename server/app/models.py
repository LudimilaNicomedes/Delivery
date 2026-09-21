from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "banco.db"

# Usa sempre o mesmo arquivo de banco
db = create_engine(
    f"sqlite:///{DATABASE_PATH.as_posix()}",
    connect_args={"check_same_thread": False}
)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String, nullable=False)
    email = Column('email', String, nullable=False)
    phone = Column('phone', String)
    password = Column('password', String, nullable= False)
    asset = Column('asset', Boolean)
    admin = Column('admin', Boolean, default=False)

    def __init__(self, name, email, phone, password, asset=True, admin=False):
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password
        self.asset = asset
        self.admin = admin

class Order(Base):
    __tablename__ = "orders"
    #STATUS_ORDRS = (
        #('PENDING', 'PENDING'),
        #('CANCELED', 'CANCELED'),
        #('COMPLETED', 'COMPLETED'),)

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    status = Column('status', String)
    user = Column('user', ForeignKey('users.id'))
    price = Column('price', Float)
    items = relationship('OrderItem', cascade='all, delete')

    def __init__(self, user , items=None, status='PENDING',price=0):
        self.status = status
        self.user = user
        self.price = price 
        self.items = items

    def calculate_price(self):
        self.price = sum(item.unit_price * item.quantity for item in self.items)

class OrderItem(Base):
    __tablename__ = 'orders_items'

    id =  Column('id', Integer, primary_key=True, autoincrement=True)
    quantity = Column('quantity', Integer )
    flavor = Column('flavor', String)
    size = Column('size', String)
    unit_price = Column('unit_price', Float)
    order = Column('order', ForeignKey('orders.id'))

    def __init__(self, quantity, flavor, size, unit_price, order):
        self.quantity = quantity
        self.flavor = flavor
        self.size = size
        self.unit_price = unit_price
        self.order = order
