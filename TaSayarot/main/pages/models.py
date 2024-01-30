from sqlalchemy import Column, DATE, INT, VARCHAR, TEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Create your models here.
class PendingUsers(Base):
    __tablename__ = "Pending_Users"

    mail = Column(VARCHAR(50))
    name = Column(VARCHAR(30))
    password_hash = Column(VARCHAR(255))
    personID = Column(INT, primary_key=True)
    release_date = Column(DATE)
    role = Column(VARCHAR(30))


class Users(Base):
    __tablename__ = "users"

    user_id = Column(INT, primary_key=True)
    name = Column(VARCHAR(30))
    role = Column(VARCHAR(30))
    email = Column(VARCHAR(50))
    release_date = Column(DATE)
    profile_image = Column(VARCHAR(255))
    password_hash = Column(VARCHAR(255))
    posts_num = Column(INT)
    likes_num = Column(INT)
    status = Column(INT)


class Comments(Base):
    __tablename__ = "comments"

    comment_id = Column(INT, primary_key=True)
    user_id = Column(INT)
    post_id = Column(INT)
    text = Column(TEXT)


class Likes(Base):
    __tablename__ = "likes"

    like_id = Column(INT, primary_key=True)
    post_id = Column(INT)
    user_id = Column(INT)


class Forums(Base):
    __tablename__ = "forums"

    message_id = Column(INT, primary_key=True)
    name = Column(VARCHAR(30))
    role = Column(VARCHAR(30))
    forum_name = Column(VARCHAR(30))
    post_date = Column(DATE)
    text = Column(TEXT)


class Posts(Base):
    __tablename__ = "posts"

    post_id = Column(INT, primary_key=True)
    user_id = Column(INT)
    post_date = Column(DATE)
    post_text = Column(TEXT)
    likes = Column(INT)
    post_file = Column(VARCHAR(255))
