from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy import Column, Text, Integer, String, ForeignKey, Boolean
from db.db_setup import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(25)),
    email = Column(String(100), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_activate = Column(Boolean, default=False)

    blog = relationship("Blog", back_populates="user")

    def __repr__(self):
        return f"User-> {self.username}"


class Blog(Base):
    __tablename__ = "blog"

    TYPE_BLOG = (
        ("FREE-TOPIC", "free-topic"),
        ("COMEDY", "comedy"),
        ("NOVEL", "novel"),
        ("SHORT-STORY", "short-story"),
        ("NEWS", "news"),
        ("SOFTWARE", "software")
    )

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    body = Column(Text)
    type_b = Column(ChoiceType(choices=TYPE_BLOG), default="FREE-TOPIC")
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="blog")

    def __repr__(self):
        return f"Blog-> {self.title}"