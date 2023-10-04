from fastapi import FastAPI

from app.core.config import settings
from app.api.api_v1.api import api_router


description = """
This API generates personalized response templates based on WhatsApp conversations.

## Templates

You will be able to:
* **Send WhatsApp conversations**
"""

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=description,
    contact={
        "name": "Eduardo Medina",
        "url": "https://www.linkedin.com/in/eduardomedina-ai/",
        "email": "contacto@nova-tek.io",
    },
)

app.include_router(api_router, prefix=settings.API_V1_STR)
