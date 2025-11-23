import uuid
import httpx
from datetime import datetime
from typing import List, Dict
from app.core.config import get_settings
from app.core.models import ReportModel, IntelligenceModel


class KillManager:
    """Manages auto-reporting of intelligence to carriers and authorities."""
    
    def __init__(self):
        self.settings = get_settings()
        self.reports: List[ReportModel] = []
    
    async def generate_report(
        self, 
        intelligence: IntelligenceModel, 
        report_type: str = "both"
    ) -> ReportModel:
        """Generate a report from intelligence data."""
        report = ReportModel(
            id=str(uuid.uuid4()),
            intelligence_id=intelligence.id,
            report_type=report_type,
            submitted_at=datetime.utcnow(),
            status="pending",
            response=None
        )
        
        self.reports.append(report)
        return report
    
    async def submit_to_carriers(self, intelligence: IntelligenceModel) -> Dict:
        """Submit intelligence to telecom carriers."""
        report_data = {
            "report_type": "scam_activity",
            "phone_numbers": intelligence.phone_numbers,
            "timestamp": intelligence.extracted_at.isoformat(),
            "evidence": {
                "crypto_wallets": intelligence.crypto_wallets,
                "urls": intelligence.urls,
                "confidence": intelligence.confidence_score
            }
        }
        
        try:
            async with httpx.AsyncClient() as client:
                # In production, this would be carrier-specific endpoints
                # For now, we'll use a generic webhook
                response = await client.post(
                    f"{self.settings.report_webhook_url}/carrier-report",
                    json=report_data,
                    timeout=30.0
                )
                return {
                    "status": "submitted",
                    "carrier_response": response.json() if response.status_code == 200 else None,
                    "status_code": response.status_code
                }
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    async def submit_to_authorities(self, intelligence: IntelligenceModel) -> Dict:
        """Submit intelligence to law enforcement authorities."""
        report_data = {
            "report_type": "fraud_complaint",
            "complaint_details": {
                "phone_numbers": intelligence.phone_numbers,
                "crypto_wallets": intelligence.crypto_wallets,
                "bank_accounts": intelligence.bank_accounts,
                "urls": intelligence.urls,
                "organizations": intelligence.organization_names
            },
            "timestamp": intelligence.extracted_at.isoformat(),
            "confidence_score": intelligence.confidence_score
        }
        
        try:
            async with httpx.AsyncClient() as client:
                # In production, this would integrate with:
                # - IC3 (Internet Crime Complaint Center)
                # - FTC Complaint Assistant
                # - State Attorney General offices
                response = await client.post(
                    f"{self.settings.report_webhook_url}/authority-report",
                    json=report_data,
                    timeout=30.0
                )
                return {
                    "status": "submitted",
                    "authority_response": response.json() if response.status_code == 200 else None,
                    "status_code": response.status_code
                }
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }
    
    async def auto_report(self, intelligence: IntelligenceModel) -> ReportModel:
        """Automatically submit report to both carriers and authorities."""
        report = await self.generate_report(intelligence, report_type="both")
        
        # Submit to carriers
        carrier_result = await self.submit_to_carriers(intelligence)
        
        # Submit to authorities
        authority_result = await self.submit_to_authorities(intelligence)
        
        # Update report with results
        report.response = {
            "carrier": carrier_result,
            "authority": authority_result
        }
        
        # Update status
        carrier_success = carrier_result.get("status") == "submitted"
        authority_success = authority_result.get("status") == "submitted"
        
        if carrier_success and authority_success:
            report.status = "confirmed"
        elif carrier_success or authority_success:
            report.status = "submitted"
        else:
            report.status = "failed"
        
        return report
    
    def get_report(self, report_id: str) -> ReportModel:
        """Get a specific report."""
        for report in self.reports:
            if report.id == report_id:
                return report
        return None
    
    def get_all_reports(self) -> List[ReportModel]:
        """Get all reports."""
        return self.reports
    
    def get_reports_by_status(self, status: str) -> List[ReportModel]:
        """Get reports by status."""
        return [r for r in self.reports if r.status == status]
    
    async def bulk_report(self, intelligence_list: List[IntelligenceModel]) -> List[ReportModel]:
        """Submit multiple intelligence reports."""
        reports = []
        for intelligence in intelligence_list:
            report = await self.auto_report(intelligence)
            reports.append(report)
        return reports
