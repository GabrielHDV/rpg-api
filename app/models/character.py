from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    race = Column(String(50), nullable=False)
    char_class = Column(String(50), nullable=False)
    level = Column(Integer, default=1)
    backstory = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    #a quem pertence esse personagem
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    #em qual campanha está (pode ser nulo se ainda não entrou em nenhuma)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True)

    owner = relationship("User", back_populates="characters")
    campaign = relationship("Campaign", back_populates="characters")

