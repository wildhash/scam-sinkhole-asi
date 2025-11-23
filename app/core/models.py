from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel


class PersonaModel(BaseModel):
    """Model for AI persona."""
    id: str
    name: str
    archetype: str
    backstory: str
    personality_traits: List[str]
    speech_patterns: List[str]
    created_at: datetime


class CallSessionModel(BaseModel):
    """Model for call session."""
    id: str
    persona_id: str
    target_number: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    status: str  # "active", "completed", "failed"
    transcript: List[Dict[str, str]] = []
    call_id: Optional[str] = None  # Telnyx call control ID


class IntelligenceModel(BaseModel):
    """Model for extracted intelligence."""
    id: str
    call_session_id: str
    extracted_at: datetime
    crypto_wallets: List[str] = []
    bank_accounts: List[str] = []
    phone_numbers: List[str] = []
    urls: List[str] = []
    organization_names: List[str] = []
    confidence_score: float


class ReportModel(BaseModel):
    """Model for generated report."""
    id: str
    intelligence_id: str
    report_type: str  # "carrier", "authority", "both"
    submitted_at: datetime
    status: str  # "pending", "submitted", "confirmed"
    response: Optional[Dict] = None
