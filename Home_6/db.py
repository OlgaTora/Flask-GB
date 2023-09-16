import databases
import sqlalchemy
from settings import settings
from sqlalchemy import create_engine, ForeignKey

DATABASE_URL = settings.DATABASE_URL
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    'users',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.String(32)),
    sqlalchemy.Column('surname', sqlalchemy.String(32)),
    sqlalchemy.Column('email', sqlalchemy.String(128), nullable=False, unique=True),
    sqlalchemy.Column('password', sqlalchemy.String(128), nullable=False),
)

products = sqlalchemy.Table(
    'products',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('product_name', sqlalchemy.String(32)),
    sqlalchemy.Column('description', sqlalchemy.Text(256)),
    sqlalchemy.Column('price', sqlalchemy.Float, nullable=False),
)

orders = sqlalchemy.Table(
    'orders',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('user_id', sqlalchemy.Integer, ForeignKey('users.id'), nullable=False),
    sqlalchemy.Column('product_id', sqlalchemy.Integer, ForeignKey('products.id'), nullable=False),
    sqlalchemy.Column('order_date', sqlalchemy.Date),
    sqlalchemy.Column('status', sqlalchemy.String(32)),
)

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)
