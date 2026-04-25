from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.campaign import Campaign
from app.schemas.campaign import CampaignCreate, CampaignUpdate, CampaignResponse
from app.auth.dependencies import get_current_user, get_current_admin
from app.models.user import User

router = APIRouter(prefix="/campaigns", tags=["Campanhas"])


@router.post("/", response_model=CampaignResponse, status_code=201)
def create_campaign(
    campaign_data: CampaignCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    #apenas admins podem criar campanhas
    new_campaign = Campaign(
        title=campaign_data.title,
        description=campaign_data.description,
        setting=campaign_data.setting,
        max_players=campaign_data.max_players,
        created_by=admin.id
    )
    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)
    return new_campaign


@router.get("/", response_model=List[CampaignResponse])
def list_campaigns(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    #qualquer usuário logado pode ver as campanhas
    return db.query(Campaign).all()


@router.get("/{campaign_id}", response_model=CampaignResponse)
def get_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campanha não encontrada.")
    return campaign


@router.put("/{campaign_id}", response_model=CampaignResponse)
def update_campaign(
    campaign_id: int,
    update_data: CampaignUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campanha não encontrada.")

    #só o admin que criou pode editar
    if campaign.created_by != admin.id:
        raise HTTPException(status_code=403, detail="Você não pode editar a campanha de outro admin.")

    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(campaign, field, value)

    db.commit()
    db.refresh(campaign)
    return campaign


@router.delete("/{campaign_id}", status_code=204)
def delete_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campanha não encontrada.")

    #só o admin que criou pode deletar
    if campaign.created_by != admin.id:
        raise HTTPException(status_code=403, detail="Você não pode deletar a campanha de outro admin.")

    db.delete(campaign)
    db.commit()
    return None
