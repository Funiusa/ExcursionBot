# from sqlalchemy import create_engine, Column, String
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
#
# from exbot.config import POSTGRES_URI
#
# engine = create_engine(POSTGRES_URI)
# Session = sessionmaker(bind=engine)
# session = Session()
#
# Base = declarative_base()
#
#
# # Define a model representing a table in the database
# class User(Base):
#     __tablename__ = "users"
#     id = Column(String, primary_key=True)
#     name = Column(String)
#
#
# # Create a new user and add it to the session
# user = User(id="123", name="John")
# session.add(user)
#
# # Commit the changes to the database
# session.commit()
