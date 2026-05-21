from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, LoginRequest, TokenResponse
from app.auth.security import hash_password, verify_password, create_access_token
from app.services.email import enviar_email_boas_vindas

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    user_data: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    #verifica se o email já está em uso
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este email já está cadastrado."
        )

    #cria o usuário com a senha hasheada
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        role=user_data.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    #envia email de boas vindas em background (não trava a resposta)
    background_tasks.add_task(
        enviar_email_boas_vindas,
        new_user.name,
        new_user.email
    )

    return new_user


@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()

    #verifica se o usuário existe e a senha está correta
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário desativado. Entre em contato com o administrador."
        )

    #gera o token com o email e o papel do usuário
    token = create_access_token(data={
        "sub": user.email,
        "role": user.role
    })

    return {"access_token": token, "token_type": "bearer"}
