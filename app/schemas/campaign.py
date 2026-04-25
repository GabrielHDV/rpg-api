from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.campaign import CampaignStatus


class CampaignCreate(BaseModel):
    #dados necessários para criar uma campanha
    title: str
    description: Optional[str] = None
    setting: Optional[str] = None
    max_players: int = 6


class CampaignUpdate(BaseModel):
    #todos opcionais pois o admin pode atualizar só o que quiser
    title: Optional[str] = None
    description: Optional[str] = None
    setting: Optional[str] = None
    status: Optional[CampaignStatus] = None
    max_players: Optional[int] = None


class CampaignResponse(BaseModel):
    #o que a API retorna ao consultar uma campanha
    id: int
    title: str
    description: Optional[str]
    setting: Optional[str]
    status: CampaignStatus
    max_players: int
    created_by: int
    created_at: datetime

    model_config = {"from_attributes": True}
