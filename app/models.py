from sqlalchemy import Column, Integer
from app.database import Base
from app.crypto_types import EncryptedString


class Entity(Base):
    __tablename__ = "entities"

    id = Column(Integer, primary_key=True, index=True)
    userDocument = Column(EncryptedString(255), nullable=False)
    creditCardToken = Column(EncryptedString(255), nullable=False)
    value = Column(Integer, nullable=False)
