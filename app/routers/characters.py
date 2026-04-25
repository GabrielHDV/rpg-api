from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.character import Character
from app.models.campaign import Campaign, CampaignStatus
from app.models.user import User, UserRole
from app.schemas.character import CharacterCreate, CharacterUpdate, CharacterResponse
from app.auth.dependencies import get_current_user, get_current_admin

router = APIRouter(prefix="/characters", tags=["Personagens"])


@router.post("/", response_model=CharacterResponse, status_code=201)
def create_character(
    char_data: CharacterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if char_data.campaign_id:
        campaign = db.query(Campaign).filter(Campaign.id == char_data.campaign_id).first()
        if not campaign:
            raise HTTPException(status_code=404, detail="Campanha não encontrada.")
        if campaign.status != CampaignStatus.recruiting:
            raise HTTPException(status_code=400, detail="Essa campanha não está aceitando jogadores.")
        if len(campaign.characters) >= campaign.max_players:
            raise HTTPException(status_code=400, detail=f"Campanha cheia! Máximo de {campaign.max_players} jogadores.")

    new_character = Character(
        name=char_data.name,
        race=char_data.race,
        char_class=char_data.char_class,
        level=char_data.level,
        backstory=char_data.backstory,
        campaign_id=char_data.campaign_id,
        user_id=current_user.id
    )
    db.add(new_character)
    db.commit()
    db.refresh(new_character)
    return new_character


@router.get("/all", response_model=List[CharacterResponse])
def list_all_characters(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    #admins podem ver todos os personagens do sistema
    return db.query(Character).all()


@router.get("/", response_model=List[CharacterResponse])
def list_my_characters(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    #cada jogador só vê seus próprios personagens
    return db.query(Character).filter(Character.user_id == current_user.id).all()


@router.get("/{character_id}", response_model=CharacterResponse)
def get_character(
    character_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Personagem não encontrado.")
    if current_user.role != UserRole.admin and character.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Acesso negado.")
    return character


@router.put("/{character_id}", response_model=CharacterResponse)
def update_character(
    character_id: int,
    update_data: CharacterUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Personagem não encontrado.")
    if character.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Você não pode editar o personagem de outro jogador.")
    if update_data.campaign_id is not None:
        campaign = db.query(Campaign).filter(Campaign.id == update_data.campaign_id).first()
        if not campaign:
            raise HTTPException(status_code=404, detail="Campanha não encontrada.")
        if campaign.status != CampaignStatus.recruiting:
            raise HTTPException(status_code=400, detail="Essa campanha não está aceitando jogadores.")
    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(character, field, value)
    db.commit()
    db.refresh(character)
    return character


@router.delete("/{character_id}", status_code=204)
def delete_character(
    character_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    character = db.query(Character).filter(Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Personagem não encontrado.")
    if current_user.role != UserRole.admin and character.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Acesso negado.")
    db.delete(character)
    db.commit()
    return None
