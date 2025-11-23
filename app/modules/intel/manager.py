import re
import uuid
from datetime import datetime
from typing import List
from openai import OpenAI
from app.core.config import get_settings
from app.core.models import IntelligenceModel, CallSessionModel


class IntelManager:
    """Manages intelligence extraction from call transcripts using AGI."""
    
    def __init__(self):
        self.settings = get_settings()
        self.client = OpenAI(
            api_key=self.settings.agi_api_key,
            base_url=self.settings.agi_api_base_url
        )
        self.intelligence_data: List[IntelligenceModel] = []
    
    async def analyze_transcript(self, call_session: CallSessionModel) -> IntelligenceModel:
        """Analyze call transcript to extract intelligence."""
        
        # Combine transcript into text
        transcript_text = "\n".join([
            f"{msg['speaker']}: {msg['text']}"
            for msg in call_session.transcript
        ])
        
        # Use regex for basic extraction
        crypto_wallets = self._extract_crypto_wallets(transcript_text)
        bank_accounts = self._extract_bank_accounts(transcript_text)
        phone_numbers = self._extract_phone_numbers(transcript_text)
        urls = self._extract_urls(transcript_text)
        
        # Use AGI for advanced extraction
        agi_intel = await self._agi_extract(transcript_text)
        
        # Merge results
        intelligence = IntelligenceModel(
            id=str(uuid.uuid4()),
            call_session_id=call_session.id,
            extracted_at=datetime.utcnow(),
            crypto_wallets=list(set(crypto_wallets + agi_intel.get("crypto_wallets", []))),
            bank_accounts=list(set(bank_accounts + agi_intel.get("bank_accounts", []))),
            phone_numbers=list(set(phone_numbers + agi_intel.get("phone_numbers", []))),
            urls=list(set(urls + agi_intel.get("urls", []))),
            organization_names=agi_intel.get("organization_names", []),
            confidence_score=agi_intel.get("confidence_score", 0.5)
        )
        
        self.intelligence_data.append(intelligence)
        return intelligence
    
    def _extract_crypto_wallets(self, text: str) -> List[str]:
        """Extract cryptocurrency wallet addresses using regex."""
        wallets = []
        
        # Bitcoin addresses (simplified patterns)
        btc_pattern = r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b'
        btc_matches = re.findall(btc_pattern, text)
        wallets.extend(btc_matches)
        
        # Ethereum addresses
        eth_pattern = r'\b0x[a-fA-F0-9]{40}\b'
        eth_matches = re.findall(eth_pattern, text)
        wallets.extend(eth_matches)
        
        return wallets
    
    def _extract_bank_accounts(self, text: str) -> List[str]:
        """Extract bank account numbers using regex."""
        # Look for sequences of 8-17 digits that might be account numbers
        # More restrictive pattern to avoid false positives
        accounts = []
        
        # Look for explicit mentions of account numbers
        account_contexts = [
            r'account\s+(?:number\s+)?#?(\d{8,17})',
            r'routing\s+(?:number\s+)?#?(\d{9})',
            r'bank\s+account\s+(\d{8,17})'
        ]
        
        for pattern in account_contexts:
            matches = re.findall(pattern, text, re.IGNORECASE)
            accounts.extend(matches)
        
        return accounts
    
    def _extract_phone_numbers(self, text: str) -> List[str]:
        """Extract phone numbers using regex."""
        # Various phone number formats
        phone_pattern = r'\+?1?\s*\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})'
        matches = re.findall(phone_pattern, text)
        phones = [f"+1{m[0]}{m[1]}{m[2]}" for m in matches]
        return phones
    
    def _extract_urls(self, text: str) -> List[str]:
        """Extract URLs using regex."""
        # More explicit URL pattern to avoid suspicious character ranges
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[\$\-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, text)
        return urls
    
    async def _agi_extract(self, transcript: str) -> dict:
        """Use AGI to extract intelligence from transcript."""
        prompt = f"""Analyze this scam call transcript and extract:
1. Cryptocurrency wallet addresses
2. Bank account numbers
3. Phone numbers mentioned
4. URLs or websites mentioned
5. Organization or company names mentioned
6. Overall confidence score (0-1) of extracted data

Transcript:
{transcript}

Return JSON with keys: crypto_wallets, bank_accounts, phone_numbers, urls, organization_names, confidence_score"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an intelligence analyst extracting information from scam calls."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            return {
                "crypto_wallets": [],
                "bank_accounts": [],
                "phone_numbers": [],
                "urls": [],
                "organization_names": [],
                "confidence_score": 0.0
            }
    
    def get_intelligence(self, intelligence_id: str) -> IntelligenceModel:
        """Get specific intelligence data."""
        for intel in self.intelligence_data:
            if intel.id == intelligence_id:
                return intel
        return None
    
    def get_all_intelligence(self) -> List[IntelligenceModel]:
        """Get all intelligence data."""
        return self.intelligence_data
    
    def get_high_value_intelligence(self, min_confidence: float = 0.7) -> List[IntelligenceModel]:
        """Get high-confidence intelligence data."""
        return [
            intel for intel in self.intelligence_data
            if intel.confidence_score >= min_confidence
        ]
