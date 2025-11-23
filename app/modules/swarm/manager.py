import uuid
from datetime import datetime
from typing import List, Dict
from openai import OpenAI
from app.core.config import get_settings
from app.core.models import PersonaModel


class SwarmManager:
    """Manages the swarm of AI personas using AGI API."""
    
    def __init__(self):
        self.settings = get_settings()
        self.client = OpenAI(
            api_key=self.settings.agi_api_key,
            base_url=self.settings.agi_api_base_url
        )
        self.personas: List[PersonaModel] = []
        
        # Predefined archetypes for variety
        self.archetypes = [
            "confused_grandpa",
            "slow_banker",
            "tech_illiterate_retiree",
            "paranoid_conspiracy_theorist",
            "chatty_lonely_widow",
            "hard_of_hearing_senior",
            "overly_trusting_immigrant",
            "penny_pinching_accountant",
            "forgetful_alzheimers_patient",
            "religious_church_lady"
        ]
    
    async def generate_persona(self, archetype: str = None) -> PersonaModel:
        """Generate a unique persona with backstory using AGI."""
        if not archetype:
            import random
            archetype = random.choice(self.archetypes)
        
        prompt = f"""Create a detailed persona for a {archetype.replace('_', ' ')} character.
Include:
1. A realistic name
2. A detailed backstory (2-3 sentences)
3. 5 personality traits
4. 5 speech patterns or mannerisms

Format as JSON with keys: name, backstory, personality_traits, speech_patterns"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a character generator creating realistic personas."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
                response_format={"type": "json_object"}
            )
            
            import json
            persona_data = json.loads(response.choices[0].message.content)
            
            persona = PersonaModel(
                id=str(uuid.uuid4()),
                name=persona_data.get("name", "Unknown"),
                archetype=archetype,
                backstory=persona_data.get("backstory", ""),
                personality_traits=persona_data.get("personality_traits", []),
                speech_patterns=persona_data.get("speech_patterns", []),
                created_at=datetime.utcnow()
            )
            
            self.personas.append(persona)
            return persona
            
        except Exception as e:
            # Fallback to simple persona if API fails
            persona = PersonaModel(
                id=str(uuid.uuid4()),
                name=f"Agent {len(self.personas) + 1}",
                archetype=archetype,
                backstory=f"A {archetype.replace('_', ' ')} who is easily confused.",
                personality_traits=["confused", "talkative", "trusting", "slow", "forgetful"],
                speech_patterns=["repeats questions", "goes off topic", "asks for clarification"],
                created_at=datetime.utcnow()
            )
            self.personas.append(persona)
            return persona
    
    async def spawn_swarm(self, count: int = 100) -> List[PersonaModel]:
        """Spawn multiple personas for the swarm."""
        personas = []
        for i in range(count):
            # Cycle through archetypes
            archetype = self.archetypes[i % len(self.archetypes)]
            persona = await self.generate_persona(archetype)
            personas.append(persona)
        return personas
    
    def get_persona(self, persona_id: str) -> PersonaModel:
        """Retrieve a specific persona by ID."""
        for persona in self.personas:
            if persona.id == persona_id:
                return persona
        return None
    
    def get_all_personas(self) -> List[PersonaModel]:
        """Get all generated personas."""
        return self.personas
    
    async def generate_response(self, persona: PersonaModel, scammer_message: str, conversation_history: List[Dict]) -> str:
        """Generate a response from a persona based on the conversation."""
        system_prompt = f"""You are {persona.name}, a {persona.archetype.replace('_', ' ')}.
Backstory: {persona.backstory}
Personality traits: {', '.join(persona.personality_traits)}
Speech patterns: {', '.join(persona.speech_patterns)}

Your goal is to keep the scammer on the line as long as possible by:
1. Being confused and asking for repeated explanations
2. Going off on tangents about your life
3. Expressing interest but having technical difficulties
4. Asking many questions
5. Being slow to understand
6. Never agreeing too quickly

Stay in character at all times."""
        
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(conversation_history)
        messages.append({"role": "user", "content": scammer_message})
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.8,
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            # Fallback response
            return "I'm sorry, could you repeat that? I didn't quite catch what you said."
