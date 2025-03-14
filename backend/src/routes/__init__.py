from .openai import openai_router
from .tts_routes import tts_router
from .emotion import emotion_router
from .sst import sst_router
from .final import final_router
from .image import image_router
from .ehr import ehr_router

__all__ = [
    "openai_router",
    "emotion_router",
    "sst_router",
    "tts_router",
    "final_router",
    "image_router",
    "ehr_router",
]
