from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from app.models.user import UserRole


class UserCreate(BaseModel):
    #dados necessários para criar um usuário
    name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.player


class UserUpdate(BaseModel):
    #todos opcionais pois o usuário pode atualizar só o que quiser
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    #o que a API retorna ao consultar um usuário (sem a senha!)
    id: int
    name: str
    email: str
    role: UserRole
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    #dados para fazer login
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    #resposta do login com o token gerado
    access_token: str
    token_type: str = "bearer"
