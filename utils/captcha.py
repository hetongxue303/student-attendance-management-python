import base64
import random
from datetime import timedelta
from io import BytesIO

from aioredis import Redis
from captcha.image import ImageCaptcha

from core import Security
from database.redis import get_redis

# SEED: str = '1234567890abcdefghijkmnpqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ'
SEED: str = '1234567890'
LENGTH: int = 4
IMG_FORMAT: str = 'PNG'
PREFIX: str = 'data:image/png;base64,'
WIDTH: int = 160
HEIGHT: int = 60


async def generate_captcha(
        length: int = LENGTH,
        range_str: str = SEED,
        img_format: str = IMG_FORMAT
):
    captcha_code = ''.join(random.choice(range_str) for _ in range(length))
    image = ImageCaptcha(width=WIDTH, height=HEIGHT).generate_image(captcha_code)
    buffer = BytesIO()
    image.save(buffer, format=img_format)
    data = buffer.getvalue()
    redis: Redis = await get_redis()
    await redis.setex(name=Security.CAPTCHA, value=captcha_code, time=timedelta(minutes=1))
    return PREFIX + base64.b64encode(data).decode()
