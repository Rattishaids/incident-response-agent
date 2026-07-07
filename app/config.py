import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    HINDSIGHT_API_KEY: str = os.getenv("HINDSIGHT_API_KEY", "")
    HINDSIGHT_URL: str = os.getenv("HINDSIGHT_URL", "https://api.hindsight.vectorize.io")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    APP_NAME: str = "Incident Response Agent"
    APP_VERSION: str = "1.0.0"
    MEMORY_BANK_ID: str = "incident-response-final-new-memory"
    
    @property
    def is_configured(self) -> bool:
        return bool(self.HINDSIGHT_API_KEY and self.GROQ_API_KEY)

settings = Settings()