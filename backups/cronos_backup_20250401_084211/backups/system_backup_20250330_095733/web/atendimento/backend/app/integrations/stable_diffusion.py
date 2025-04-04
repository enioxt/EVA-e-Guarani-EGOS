#!/usr/bin/env python
"""
EVA & GUARANI EGOS - Módulo de Integração com Stable Diffusion

Este módulo fornece integração com diferentes APIs de Stable Diffusion para
geração de imagens a partir de prompts textuais.
"""

import os
import json
import logging
import asyncio
import base64
import io
import requests
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path
from datetime import datetime
from PIL import Image

# Configuração de logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class StableDiffusionAPI:
    """Interface para APIs de Stable Diffusion"""

    def __init__(self, api_key: Optional[str] = None, api_url: Optional[str] = None):
        """
        Inicializa a integração com Stable Diffusion.

        Args:
            api_key: Chave da API (opcional se usar API local)
            api_url: URL da API (opcional se usar API padrão)
        """
        self.api_key = api_key or os.getenv("IMAGE_API_KEY", "")
        self.api_url = api_url or os.getenv("IMAGE_API_URL", "")
        self.local_api_url = "http://127.0.0.1:7860"
        self.output_dir = Path("data/generated_images")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Verificar se APIs estão disponíveis
        self.has_stable_diffusion_api = bool(
            self.api_key
            and self.api_url
            and self.api_key != "sua_chave_api_aqui"
            and self.api_url != "https://api.exemplo.com/images"
        )

        # Tentar detectar API local (Automatic1111)
        self.has_local_api = self._check_local_api()

        if self.has_stable_diffusion_api:
            logger.info("API externa de Stable Diffusion configurada")
        if self.has_local_api:
            logger.info("API local de Stable Diffusion (Automatic1111) detectada")

        if not (self.has_stable_diffusion_api or self.has_local_api):
            logger.warning("Nenhuma API de Stable Diffusion disponível")

    def _check_local_api(self) -> bool:
        """Verifica se uma API local (Automatic1111) está disponível"""
        try:
            response = requests.get(f"{self.local_api_url}/sdapi/v1/sd-models", timeout=2)
            return response.status_code == 200
        except Exception:
            return False

    async def generate_image(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 512,
        height: int = 512,
        num_images: int = 1,
        guidance_scale: float = 7.5,
        steps: int = 30,
        seed: int = -1,
    ) -> Tuple[bool, Optional[str], Optional[bytes]]:
        """
        Gera uma imagem a partir de um prompt usando qualquer API disponível.

        Args:
            prompt: Descrição textual da imagem desejada
            negative_prompt: Elementos a serem evitados na imagem
            width: Largura da imagem
            height: Altura da imagem
            num_images: Número de imagens a gerar
            guidance_scale: Escala de orientação do modelo
            steps: Número de etapas de amostragem
            seed: Semente para geração (negativo para aleatório)

        Returns:
            Tupla com (sucesso, mensagem de erro, dados da imagem)
        """
        # Primeiro tenta API local se disponível
        if self.has_local_api:
            try:
                success, error_msg, image_data = await self._generate_with_local_api(
                    prompt, negative_prompt, width, height, num_images, guidance_scale, steps, seed
                )
                if success:
                    return success, error_msg, image_data
                logger.warning(f"Falha na API local: {error_msg}. Tentando API remota...")
            except Exception as e:
                logger.error(f"Erro na API local: {e}")

        # Se não há API local ou ela falhou, tenta API remota
        if self.has_stable_diffusion_api:
            try:
                return await self._generate_with_remote_api(
                    prompt, negative_prompt, width, height, num_images, guidance_scale, steps, seed
                )
            except Exception as e:
                logger.error(f"Erro na API remota: {e}")
                return False, f"Erro na geração de imagem: {str(e)}", None

        # Se chegou aqui, não há API disponível
        return False, "Nenhuma API de Stable Diffusion está disponível", None

    async def _generate_with_local_api(
        self,
        prompt: str,
        negative_prompt: str,
        width: int,
        height: int,
        num_images: int,
        guidance_scale: float,
        steps: int,
        seed: int,
    ) -> Tuple[bool, Optional[str], Optional[bytes]]:
        """Gera imagem usando API local (Automatic1111)"""
        payload = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "width": width,
            "height": height,
            "batch_size": min(num_images, 4),  # Limita para evitar sobrecarga
            "cfg_scale": guidance_scale,
            "steps": steps,
            "seed": seed,
            "sampler_name": "Euler a",
            "enable_hr": False,
            "tiling": False,
        }

        try:
            # Fazemos uma solicitação assíncrona para não bloquear
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: requests.post(
                    url=f"{self.local_api_url}/sdapi/v1/txt2img", json=payload, timeout=120
                ),
            )

            if response.status_code != 200:
                return False, f"API local retornou código {response.status_code}", None

            response_data = response.json()
            if not response_data.get("images"):
                return False, "API local não retornou imagens", None

            # Pega a primeira imagem
            image_base64 = response_data["images"][0]
            if "," in image_base64:
                image_base64 = image_base64.split(",", 1)[1]

            # Decodifica a imagem
            image_bytes = base64.b64decode(image_base64)

            # Salva a imagem localmente para referência
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = self.output_dir / f"local_sd_{timestamp}.png"

            with open(image_path, "wb") as f:
                f.write(image_bytes)

            return True, None, image_bytes

        except Exception as e:
            logger.error(f"Erro na geração com API local: {e}")
            return False, f"Erro na API local: {str(e)}", None

    async def _generate_with_remote_api(
        self,
        prompt: str,
        negative_prompt: str,
        width: int,
        height: int,
        num_images: int,
        guidance_scale: float,
        steps: int,
        seed: int,
    ) -> Tuple[bool, Optional[str], Optional[bytes]]:
        """Gera imagem usando API remota configurada"""
        payload = {
            "key": self.api_key,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "width": str(width),
            "height": str(height),
            "samples": str(min(num_images, 4)),  # Limita para evitar sobrecarga
            "num_inference_steps": str(steps),
            "safety_checker": "yes",
            "enhance_prompt": "yes",
            "guidance_scale": guidance_scale,
            "seed": seed if seed >= 0 else None,
        }

        try:
            # Fazemos uma solicitação assíncrona para não bloquear
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, lambda: requests.post(url=self.api_url, json=payload, timeout=120)
            )

            if response.status_code != 200:
                return False, f"API remota retornou código {response.status_code}", None

            response_data = response.json()

            # O formato de resposta pode variar dependendo da API
            # Aqui tentamos detectar vários formatos comuns
            image_url = None

            # Formato comum em APIs como StabilityAI ou Prodia
            if response_data.get("output") and isinstance(response_data["output"], list):
                image_url = response_data["output"][0]

            # Outro formato comum
            elif response_data.get("output") and isinstance(response_data["output"], str):
                image_url = response_data["output"]

            # Formato alternativo
            elif response_data.get("images") and isinstance(response_data["images"], list):
                image_url = response_data["images"][0]

            # Formato direto (alguns serviços retornam diretamente a URL)
            elif isinstance(response_data, str) and (
                response_data.startswith("http://") or response_data.startswith("https://")
            ):
                image_url = response_data

            # Não conseguimos encontrar a URL da imagem
            if not image_url:
                return False, "Não foi possível extrair a URL da imagem da resposta", None

            # Baixamos a imagem a partir da URL
            img_response = await loop.run_in_executor(
                None, lambda: requests.get(image_url, timeout=30)
            )

            if img_response.status_code != 200:
                return False, f"Falha ao baixar imagem: {img_response.status_code}", None

            # Obtemos os bytes da imagem
            image_bytes = img_response.content

            # Salvamos a imagem localmente para referência
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = self.output_dir / f"remote_sd_{timestamp}.png"

            with open(image_path, "wb") as f:
                f.write(image_bytes)

            return True, None, image_bytes

        except Exception as e:
            logger.error(f"Erro na geração com API remota: {e}")
            return False, f"Erro na API remota: {str(e)}", None


# Exemplo de uso
if __name__ == "__main__":

    async def test_generation():
        sd_api = StableDiffusionAPI()
        success, error, image_data = await sd_api.generate_image(
            "A beautiful forest with sunset and mountains in the background",
            negative_prompt="ugly, blurry, low quality",
            width=512,
            height=512,
        )

        if success and image_data:
            print(f"Imagem gerada com sucesso! Tamanho: {len(image_data)} bytes")
            # Podemos mostrar a imagem
            image = Image.open(io.BytesIO(image_data))
            image.show()
        else:
            print(f"Falha na geração: {error}")

    asyncio.run(test_generation())
