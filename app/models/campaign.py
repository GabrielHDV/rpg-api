from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class CampaignStatus(str, enum.Enum):
    #estados possíveis de uma campanha
    recruiting = "recruiting"  # aceitando jogadores
    ongoing = "ongoing"        # em andamento
    finished = "finished"      # finalizada
    paused = "paused"          # pausada


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    setting = Column(String(100), nullable=True)

    #começa aceitando jogadores por padrão
    status = Column(Enum(CampaignStatus), default=CampaignStatus.recruiting)
    max_players = Column(Integer, default=6)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    #qual admin criou essa campanha
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    creator = relationship("User", back_populates="campaigns")
    characters = relationship("Character", back_populates="campaign")

