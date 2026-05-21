import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import tempfile
import os
import logging

load_dotenv()

logger = logging.getLogger(__name__)

#configura as credenciais do Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)


async def upload_imagem_personagem(arquivo: bytes, character_id: int) -> str:
    #salva o arquivo temporariamente e faz upload pelo caminho
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(arquivo)
            tmp_path = tmp.name

        resultado = cloudinary.uploader.upload(
            tmp_path,
            folder="rpg-api/characters",
            public_id=f"character_{character_id}",
            overwrite=True,
            resource_type="image"
        )

        os.unlink(tmp_path)

        url = resultado.get("secure_url")
        logger.info(f"Imagem do personagem {character_id} enviada: {url}")
        return url
    except Exception as e:
        logger.error(f"Erro ao fazer upload da imagem: {str(e)}")
        raise
