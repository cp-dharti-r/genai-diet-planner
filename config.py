import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the Diet Planner application"""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    
    # Application Configuration
    APP_TITLE = os.getenv("APP_TITLE", "AI Diet Planner")
    APP_DESCRIPTION = os.getenv("APP_DESCRIPTION", "Personalized diet planning with AI dietitian")
    
    # PDF Configuration
    PDF_FONT_SIZE = 12
    PDF_MARGIN = 50
    PDF_LINE_HEIGHT = 20
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        return True
