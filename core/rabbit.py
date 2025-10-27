import aio_pika
from core.config import Settings

settings = Settings()

async def connect_to_rabbit():
    connection = await aio_pika.connect_robust(
        settings.RABBIT_MQ_URL
    )
    return await connection.channel()
