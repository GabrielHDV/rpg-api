from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logger = logging.getLogger(__name__)

#configuração da conexão com o servidor de email
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_HOST"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)


async def enviar_email_boas_vindas(nome: str, email: str):
    #envia email de boas vindas ao novo usuário
    try:
        mensagem = MessageSchema(
            subject="Bem-vindo à API de RPG de Mesa!",
            recipients=[email],
            body=f"""
            <h2>Olá, {nome}!</h2>
            <p>Sua conta foi criada com sucesso na API de RPG de Mesa.</p>
            <p>Agora você pode:</p>
            <ul>
                <li>Criar seus personagens</li>
                <li>Entrar em campanhas</li>
                <li>Viver aventuras épicas!</li>
            </ul>
            <p>Boas aventuras!</p>
            """,
            subtype="html"
        )
        fm = FastMail(conf)
        await fm.send_message(mensagem)
        logger.info(f"Email enviado para {email}")
    except Exception as e:
        #loga o erro mas não interrompe o fluxo da aplicação
        logger.error(f"Erro ao enviar email para {email}: {str(e)}")
