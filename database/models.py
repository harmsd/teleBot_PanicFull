from sqlalchemy import BigInteger, Integer, Text, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .db import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    full_name: Mapped[str] = mapped_column(String, nullable=True)

    panics: Mapped[list["Panic"]] = relationship("Panic", back_populates="user", cascade="all, delete-orphan")

class Panic(Base):
    __tablename__ = 'panics'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=True)
    panic_string: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    comment: Mapped[str] = mapped_column(String, nullable=True)
    
    user: Mapped["User"] = relationship("User", back_populates='panics')
