# ...existing code...
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "Tola Ecommerce Development"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES") 
    
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
    }
settings = Settings()
# ...existing code...