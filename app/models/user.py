from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class UserRole(str, enum.Enum):
    #dois tipos de usuário no sistema
    admin = "admin"    #mestre da campanha
    player = "player"  #jogador


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)

    #nunca salvamos a senha pura, sempre o hash
    hashed_password = Column(String(255), nullable=False)

    #todo usuário começa como player
    role = Column(Enum(UserRole), default=UserRole.player, nullable=False)
    is_active = Column(Boolean, default=True)

    #preenchido automaticamente pelo banco
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    #relação com as outras tabelas
    characters = relationship("Character", back_populates="owner")
    campaigns = relationship("Campaign", back_populates="creator")
