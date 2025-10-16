from typing import Any, Callable, Dict, List, Optional, Union
from pydantic import BaseModel, HttpUrl, Field
# from justAnotherKahootBot.config.state import args 


# ------------------------
# Submodels
# ------------------------
class LanguageInfo(BaseModel):
    language: Optional[str] = None
    lastUpdatedOn: Optional[int] = None
    readAloudSupported: Optional[bool] = None


class Choice(BaseModel):
    answer: Optional[str] = None
    correct: Optional[bool] = None
    languageInfo: Optional[LanguageInfo] = None


class Video(BaseModel):
    id: Optional[str] = None
    startTime: Optional[float] = None
    endTime: Optional[float] = None
    service: Optional[str] = None
    fullUrl: Optional[str] = None


class ImageMetadata(BaseModel):
    id: Optional[str] = None
    contentType: Optional[str] = None
    resources: Optional[str] = ""


class Question(BaseModel):
    question_type: Optional[str] = Field(None, alias="type")
    question: Optional[str] = None
    time: Optional[int] = None
    points: Optional[bool] = None
    pointsMultiplier: Optional[int] = None
    choices: Optional[List[Choice]] = []
    image: Optional[HttpUrl] = None
    imageMetadata: Optional[ImageMetadata] = None
    resources: Optional[str] = ""
    video: Optional[Video] = None
    questionFormat: Optional[int] = None
    languageInfo: Optional[LanguageInfo] = None
    media: Optional[List] = []


class ExtractedColor(BaseModel):
    swatch: Optional[str] = None
    rgbHex: Optional[str] = None


class CoverMetadata(BaseModel):
    id: Optional[str] = None
    contentType: Optional[str] = None
    resources: Optional[str] = ""
    extractedColors: Optional[List[ExtractedColor]] = []
    blurhash: Optional[str] = None


class VersionMetadata(BaseModel):
    version: Optional[int] = None
    created: Optional[int] = None
    creator: Optional[str] = None


class Metadata(BaseModel):
    access: Optional[dict] = None
    versionMetadata: Optional[VersionMetadata] = None


# ------------------------
# Top-level KahootQuiz model
# ------------------------
class KahootQuiz(BaseModel):
    uuid: Optional[str] = None
    language: Optional[str] = None
    creator: Optional[str] = None
    creator_username: Optional[str] = None
    compatibilityLevel: Optional[int] = None
    creator_primary_usage: Optional[str] = None
    visibility: Optional[int] = None
    audience: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    quizType: Optional[str] = None
    cover: Optional[HttpUrl] = None
    coverMetadata: Optional[CoverMetadata] = None
    questions: Optional[List[Question]] = []
    metadata: Optional[Metadata] = None
    resources: Optional[str] = ""
    slug: Optional[str] = None
    languageInfo: Optional[LanguageInfo] = None
    inventoryItemIds: Optional[List] = []
    isValid: Optional[bool] = None
    playAsGuest: Optional[bool] = None
    hasRestrictedContent: Optional[bool] = None
    question_type: Optional[str] = Field(None, alias="type")
    created: Optional[int] = None
    modified: Optional[int] = None

