#!/usr/bin/env python3
"""
Demo script for ScamSinkhole ASI
This script demonstrates the system's capabilities without making real calls.
"""

import asyncio
import json
import sys
from datetime import datetime
from app.modules.swarm import SwarmManager
from app.modules.intel import IntelManager
from app.core.models import CallSessionModel


async def demo_persona_generation():
    """Demonstrate persona generation."""
    print("\n" + "="*60)
    print("DEMO: Persona Generation")
    print("="*60)
    
    swarm = SwarmManager()
    
    print("\nGenerating 5 sample personas...")
    for i in range(5):
        persona = await swarm.generate_persona()
        print(f"\n{i+1}. {persona.name} ({persona.archetype})")
        print(f"   Backstory: {persona.backstory[:100]}...")
        print(f"   Traits: {', '.join(persona.personality_traits[:3])}")
    
    return swarm


async def demo_conversation():
    """Demonstrate AI conversation generation."""
    print("\n" + "="*60)
    print("DEMO: AI Conversation")
    print("="*60)
    
    swarm = SwarmManager()
    persona = await swarm.generate_persona("confused_grandpa")
    
    print(f"\nPersona: {persona.name}")
    print(f"Archetype: {persona.archetype}")
    print(f"\nSimulated conversation:")
    
    # Simulate a conversation
    conversation_history = []
    scammer_messages = [
        "Hello, this is Microsoft support. Your computer has a virus.",
        "We need you to give us remote access to fix it.",
        "Just go to this website and download our tool."
    ]
    
    for msg in scammer_messages:
        print(f"\n[SCAMMER]: {msg}")
        response = await swarm.generate_response(persona, msg, conversation_history)
        print(f"[{persona.name.upper()}]: {response}")
        
        conversation_history.append({"role": "user", "content": msg})
        conversation_history.append({"role": "assistant", "content": response})
    
    return persona, conversation_history


async def demo_intelligence_extraction():
    """Demonstrate intelligence extraction."""
    print("\n" + "="*60)
    print("DEMO: Intelligence Extraction")
    print("="*60)
    
    # Create a mock call session with suspicious content
    mock_transcript = [
        {"speaker": "scammer", "text": "Send Bitcoin to this address: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"},
        {"speaker": "agent", "text": "What was that address again?"},
        {"speaker": "scammer", "text": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa. Or wire to account 123456789"},
        {"speaker": "agent", "text": "Let me write that down..."},
        {"speaker": "scammer", "text": "Call us at +15559998888 or visit scamsite.com"},
    ]
    
    session = CallSessionModel(
        id="demo-session-001",
        persona_id="demo-persona-001",
        target_number="+15551234567",
        start_time=datetime.utcnow(),
        status="completed",
        transcript=mock_transcript
    )
    
    print("\nAnalyzing call transcript...")
    intel_manager = IntelManager()
    intelligence = await intel_manager.analyze_transcript(session)
    
    print("\n📊 Extracted Intelligence:")
    print(f"   Crypto Wallets: {intelligence.crypto_wallets}")
    print(f"   Bank Accounts: {intelligence.bank_accounts}")
    print(f"   Phone Numbers: {intelligence.phone_numbers}")
    print(f"   URLs: {intelligence.urls}")
    print(f"   Confidence Score: {intelligence.confidence_score:.2%}")
    
    return intelligence


async def demo_reporting():
    """Demonstrate reporting capability."""
    print("\n" + "="*60)
    print("DEMO: Auto-Reporting")
    print("="*60)
    
    from app.modules.kill import KillManager
    from app.core.models import IntelligenceModel
    
    # Create mock intelligence
    intelligence = IntelligenceModel(
        id="demo-intel-001",
        call_session_id="demo-session-001",
        extracted_at=datetime.utcnow(),
        crypto_wallets=["1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"],
        bank_accounts=["123456789"],
        phone_numbers=["+15559998888"],
        urls=["http://scamsite.com"],
        organization_names=["Fake Corp"],
        confidence_score=0.85
    )
    
    kill_manager = KillManager()
    
    print("\nGenerating report from intelligence...")
    report = await kill_manager.generate_report(intelligence, "both")
    
    print("\n📋 Report Generated:")
    print(f"   Report ID: {report.id}")
    print(f"   Type: {report.report_type}")
    print(f"   Status: {report.status}")
    print(f"   Timestamp: {report.submitted_at}")
    
    print("\n✅ In production, this would be submitted to:")
    print("   - Telecom carriers (Verizon, AT&T, T-Mobile)")
    print("   - IC3 (Internet Crime Complaint Center)")
    print("   - FTC Complaint Assistant")
    print("   - State Attorney General offices")
    
    return report


async def main():
    """Run all demos."""
    print("\n" + "="*60)
    print("🛡️  SCAMSINKHOLE ASI - DEMONSTRATION MODE")
    print("="*60)
    print("\nThis demo showcases the system's capabilities without")
    print("making real phone calls or submitting real reports.")
    print()
    
    try:
        # Demo 1: Persona Generation
        await demo_persona_generation()
        
        # Demo 2: AI Conversation
        await demo_conversation()
        
        # Demo 3: Intelligence Extraction
        await demo_intelligence_extraction()
        
        # Demo 4: Reporting
        await demo_reporting()
        
        print("\n" + "="*60)
        print("✅ DEMO COMPLETE")
        print("="*60)
        print("\nTo use ScamSinkhole in production:")
        print("1. Configure API keys in .env file")
        print("2. Start the server: python main.py")
        print("3. Open browser to: http://localhost:8000")
        print("4. Use the Web UI or API endpoints")
        print()
        
    except Exception as e:
        print(f"\n❌ Demo error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
