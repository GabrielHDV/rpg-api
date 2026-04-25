from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CharacterCreate(BaseModel):
    #dados necessários para criar um personagem
    name: str
    race: str
    char_class: str
    level: int = 1
    backstory: Optional[str] = None
    campaign_id: Optional[int] = None


class CharacterUpdate(BaseModel):
    #todos opcionais pois o jogador pode atualizar só o que quiser
    name: Optional[str] = None
    race: Optional[str] = None
    char_class: Optional[str] = None
    level: Optional[int] = None
    backstory: Optional[str] = None
    campaign_id: Optional[int] = None


class CharacterResponse(BaseModel):
    #o que a API retorna ao consultar um personagem
    id: int
    name: str
    race: str
    char_class: str
    level: int
    backstory: Optional[str]
    user_id: int
    campaign_id: Optional[int]
    created_at: datetime

    model_config = {"from_attributes": True}
