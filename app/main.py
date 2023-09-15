from fastapi import FastAPI
from app.core.config import settings


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
