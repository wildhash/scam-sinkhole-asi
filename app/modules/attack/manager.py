import uuid
import telnyx
from datetime import datetime
from typing import List, Optional, Dict
from app.core.config import get_settings
from app.core.models import CallSessionModel, PersonaModel


class AttackManager:
    """Manages outbound calls to scammers using Telnyx Voice API."""
    
    def __init__(self):
        self.settings = get_settings()
        telnyx.api_key = self.settings.telnyx_api_key
        self.active_sessions: Dict[str, CallSessionModel] = {}
    
    async def initiate_call(self, target_number: str, persona: PersonaModel) -> CallSessionModel:
        """Initiate a call to a scammer using a specific persona."""
        session = CallSessionModel(
            id=str(uuid.uuid4()),
            persona_id=persona.id,
            target_number=target_number,
            start_time=datetime.utcnow(),
            status="active",
            transcript=[]
        )
        
        try:
            # Create a call using Telnyx
            call = telnyx.Call.create(
                connection_id=self.settings.telnyx_phone_number,
                to=target_number,
                from_=self.settings.telnyx_phone_number,
                # Webhook URL for call events
                webhook_url=f"{self.settings.report_webhook_url}/call-events",
                webhook_event_url=f"{self.settings.report_webhook_url}/call-events",
            )
            
            # Store the call ID for tracking
            session.call_id = call.call_control_id
            self.active_sessions[session.id] = session
            return session
            
        except Exception as e:
            session.status = "failed"
            session.end_time = datetime.utcnow()
            return session
    
    async def dial_scam_list(self, phone_numbers: List[str], personas: List[PersonaModel]) -> List[CallSessionModel]:
        """Dial multiple scam numbers with different personas."""
        sessions = []
        
        for i, number in enumerate(phone_numbers):
            # Assign persona (cycle through available personas)
            persona = personas[i % len(personas)]
            session = await self.initiate_call(number, persona)
            sessions.append(session)
        
        return sessions
    
    async def handle_call_event(self, event_data: Dict) -> None:
        """Handle incoming call events from Telnyx webhook."""
        call_id = event_data.get("call_control_id")
        event_type = event_data.get("event_type")
        
        # Find the session for this call
        session_id = None
        for sid, session in self.active_sessions.items():
            if hasattr(session, 'call_id') and session.call_id == call_id:
                session_id = sid
                break
        
        if not session_id:
            return
        
        session = self.active_sessions[session_id]
        
        if event_type == "call.answered":
            # Call was answered, start conversation
            session.status = "active"
        elif event_type == "call.hangup":
            # Call ended
            session.end_time = datetime.utcnow()
            session.duration_seconds = int((session.end_time - session.start_time).total_seconds())
            session.status = "completed"
        elif event_type == "call.speak.ended":
            # Speech completed, wait for response
            pass
    
    async def send_audio_response(self, session_id: str, text: str) -> bool:
        """Send audio response using text-to-speech."""
        if session_id not in self.active_sessions:
            return False
        
        session = self.active_sessions[session_id]
        
        try:
            # Use Telnyx TTS to speak the response
            # This would use the call control API
            session.transcript.append({
                "speaker": "agent",
                "text": text,
                "timestamp": datetime.utcnow().isoformat()
            })
            return True
        except Exception as e:
            return False
    
    def get_session(self, session_id: str) -> Optional[CallSessionModel]:
        """Get a specific call session."""
        return self.active_sessions.get(session_id)
    
    def get_active_sessions(self) -> List[CallSessionModel]:
        """Get all active call sessions."""
        return [s for s in self.active_sessions.values() if s.status == "active"]
    
    def get_all_sessions(self) -> List[CallSessionModel]:
        """Get all call sessions."""
        return list(self.active_sessions.values())
    
    async def end_call(self, session_id: str) -> bool:
        """Manually end a call session."""
        if session_id not in self.active_sessions:
            return False
        
        session = self.active_sessions[session_id]
        session.end_time = datetime.utcnow()
        session.duration_seconds = int((session.end_time - session.start_time).total_seconds())
        session.status = "completed"
        return True
