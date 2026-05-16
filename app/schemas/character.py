from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


class CharacterCreate(BaseModel):
    name: str
    race: str
    char_class: str
    level: int = 1
    backstory: Optional[str] = None
    campaign_id: Optional[int] = None

    @field_validator("level")
    @classmethod
    def level_valido(cls, v):
        #nível deve ser entre 1 e 20
        if not 1 <= v <= 20:
            raise ValueError("Nível deve ser entre 1 e 20.")
        return v

    @field_validator("name", "race", "char_class")
    @classmethod
    def campos_nao_vazios(cls, v):
        #nenhum campo de texto pode ser enviado vazio
        if not v.strip():
            raise ValueError("Este campo não pode ser vazio.")
        return v.strip()


class CharacterUpdate(BaseModel):
    name: Optional[str] = None
    race: Optional[str] = None
    char_class: Optional[str] = None
    level: Optional[int] = None
    backstory: Optional[str] = None
    campaign_id: Optional[int] = None

    @field_validator("level")
    @classmethod
    def level_valido(cls, v):
        if v is not None and not 1 <= v <= 20:
            raise ValueError("Nível deve ser entre 1 e 20.")
        return v


class CharacterResponse(BaseModel):
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

