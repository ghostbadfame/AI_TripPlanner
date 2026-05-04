import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from exceptions.exceptionHandling import ConfigurationError
from logger.logging import get_logger

load_dotenv()

logger = get_logger(__name__)


class ConfigLoader:
    def __init__(self):
        self.config = load_config()
    
    def __getitem__(self, key):
        try:
            return self.config[key]
        except KeyError as exc:
            raise ConfigurationError(
                "Required configuration section is missing.",
                details={"missing_key": key},
            ) from exc

class ModelLoader(BaseModel):
    model_provider: Literal["groq", "openai"] = "groq"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()
    
    class Config:
        arbitrary_types_allowed = True
    
    def load_llm(self):
        """
        Load and return the LLM model.
        """
        logger.info("Loading LLM provider: %s", self.model_provider)
        if self.model_provider == "groq":
            groq_api_key = os.getenv("GROQ_API_KEY")
            if not groq_api_key:
                raise ConfigurationError("Missing GROQ_API_KEY for Groq model provider.")

            model_name = self._get_model_name("groq")
            llm = ChatGroq(model=model_name, api_key=groq_api_key)
        elif self.model_provider == "openai":
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if not openai_api_key:
                raise ConfigurationError("Missing OPENAI_API_KEY for OpenAI model provider.")

            model_name = self._get_model_name("openai")
            llm = ChatOpenAI(model=model_name, api_key=openai_api_key)
        else:
            raise ConfigurationError(
                "Unsupported model provider requested.",
                details={"model_provider": self.model_provider},
            )

        return llm

    def _get_model_name(self, provider: str) -> str:
        try:
            model_name = self.config["llm"][provider]["model_name"]
        except KeyError as exc:
            raise ConfigurationError(
                "Model configuration is incomplete.",
                details={"provider": provider},
            ) from exc

        if not model_name:
            raise ConfigurationError(
                "Model name is missing from configuration.",
                details={"provider": provider},
            )

        return model_name
    
