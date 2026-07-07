from typing import List, Dict
import re
import json
from hindsight_client import Hindsight
from cascadeflow import CascadeAgent, ModelConfig
from .models import IncidentMemory, IncidentResponse
from .config import settings

class IncidentAgent:
    def __init__(self):
        if not settings.is_configured:
            raise ValueError("Missing API keys! Please set HINDSIGHT_API_KEY and GROQ_API_KEY in .env")
        
        self.memory = Hindsight(
            api_key=settings.HINDSIGHT_API_KEY,
            base_url=settings.HINDSIGHT_URL
        )
        self.bank_id = settings.MEMORY_BANK_ID
        self.max_context_incidents = 3
        
        try:
            self.router = CascadeAgent(models=[
                ModelConfig(name="qwen/qwen3-32b", provider="groq", cost=0.000375),
                ModelConfig(name="llama-3.3-70b-versatile", provider="groq", cost=0.00562),
            ])
            print("✅ cascadeflow initialized successfully")
        except Exception as e:
            print(f"⚠️ cascadeflow initialization failed: {e}")
            self.router = None
        
        print("✅ Agent initialized with Hindsight Cloud")
    
    def load_incidents(self, incidents: List[IncidentMemory]):
        print(f"📥 Loading {len(incidents)} incidents into memory...")
        for incident in incidents:
            json_content = json.dumps({
                "incident_id": incident.incident_id,
                "title": incident.title,
                "symptoms": incident.symptoms,
                "root_cause": incident.root_cause,
                "resolution": incident.resolution,
                "service": incident.affected_service,
                "severity": incident.severity.value,
                "duration": incident.duration_minutes,
                "detection": incident.detection_method
            })
            self.memory.retain(
                bank_id=self.bank_id,
                content=json_content
            )
            print(f"   ✅ Stored {incident.incident_id}")
        print(f"✅ Loaded {len(incidents)} incidents")
    
    async def recall_all(self, alert: str) -> List[Dict]:
        try:
            results = await self.memory.arecall(
                bank_id=self.bank_id,
                query=alert
            )
            
            if not results:
                return []
            
            formatted_results = []
            for item in results:
                score = getattr(item, 'score', 0)
                content = getattr(item, 'text', None)
                if content is None:
                    content = getattr(item, 'content', None)
                if content is None:
                    content = str(item)
                
                try:
                    if isinstance(content, str) and content.strip().startswith('{'):
                        parsed = json.loads(content)
                        formatted_results.append({'content': parsed, 'score': score})
                    else:
                        formatted_results.append({'content': content, 'score': score})
                except (json.JSONDecodeError, TypeError):
                    formatted_results.append({'content': content, 'score': score})
            
            return formatted_results
        except Exception as e:
            print(f"⚠️ Error: {e}")
            return []
    
    def _clean_response(self, text: str) -> str:
        """Remove all thinking/reasoning from response"""
        # Remove <think> tags
        text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
        # Remove reasoning phrases
        thinking_patterns = [
            r"^.*?The user wants me to.*?\.\s*",
            r"^.*?Okay, let'?s.*?\.\s*",
            r"^.*?First, I need to.*?\.\s*",
            r"^.*?I need to.*?\.\s*",
            r"^.*?Let me.*?\.\s*",
            r"^.*?I should.*?\.\s*",
            r"^.*?I'll start.*?\.\s*",
            r"^.*?Looking at.*?\.\s*",
        ]
        for pattern in thinking_patterns:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE | re.DOTALL)
        # Clean up
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()
    
    def _extract_root_cause(self, text: str) -> str:
        """Extract root cause from diagnosis"""
        match = re.search(r"ROOT CAUSE[:\s]+(.+?)(?=[.\n]|$)", text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return "See diagnosis"
    
    def _extract_resolution_steps(self, text: str) -> List[str]:
        """Extract resolution steps from diagnosis"""
        match = re.search(r"RECOVERY STEPS.*?:([\s\S]*?)(CURRENT RECOMMENDATION|$)", text, re.IGNORECASE)
        if not match:
            return []
        
        section = match.group(1)
        steps = []
        for line in section.splitlines():
            line = line.strip()
            if line.startswith("-") or line.startswith("•"):
                steps.append(line.lstrip("-• ").strip())
        return steps
    
    async def analyze(self, alert: str) -> IncidentResponse:
        """Analyze an alert using memory + intelligent routing"""
        print(f"\n📢 Alert: {alert}")
        print("🔍 Searching memory...")
        
        all_similar = await self.recall_all(alert)
        similar_count = len(all_similar)
        print(f"📋 Found {similar_count} similar incidents")
        
        if similar_count == 0:
            return IncidentResponse(
                diagnosis="No similar incidents found in memory. This appears to be a new incident.",
                model_used="none",
                cost=0.0,
                similar_incidents_found=0,
                confidence="Low",
                root_cause="Unknown",
                resolution_steps=["No similar incidents found"]
            )
        
        best_item = max(all_similar, key=lambda x: x.get('score', 0))
        best_content = best_item.get('content', {})
        print(f"📊 Best match score: {best_item.get('score', 0)}")
        
        context_text = ""
        if isinstance(best_content, dict):
            parts = []
            for key, value in best_content.items():
                if value and key != 'duration':
                    parts.append(f"{key}: {value}")
            context_text = "\n".join(parts)
        else:
            context_text = str(best_content)
        
        print(f"📄 Context preview: {context_text[:200]}...")
        
        if self.router:
            try:
                prompt = f"""
You are an Incident Response AI. Your ONLY job is to output a diagnosis.

A similar incident has already been recovered in the past.

SIMILAR INCIDENT FOUND IN MEMORY:
{context_text[:1500]}

CRITICAL INSTRUCTION - FOLLOW EXACTLY:
1. Start with: "This incident closely matches a previously resolved incident."
2. Then provide these 4 sections with EXACT headings:
   PREVIOUS INCIDENT SUMMARY:
   ROOT CAUSE:
   RECOVERY STEPS: (use bullet points with •)
   CURRENT RECOMMENDATION:

IMPORTANT RULES:
- Do NOT say "The user wants me to..."
- Do NOT say "Let me" or "I think" or "Okay"
- Do NOT include any reasoning or thinking
- Do NOT mention "similar incidents found"
- Return ONLY the diagnosis with the 4 sections
- Be specific and use the exact information from the incident

Your response must be ONLY the diagnosis, nothing else.
"""
                
                result = await self.router.run(prompt)
                print(f"✅ cascadeflow responded!")
                print(f"📊 Model: {result.model_used}")
                print(f"💰 Cost: ${result.total_cost:.6f}")
                
                diagnosis = self._clean_response(result.content)
                
                if not diagnosis or len(diagnosis) < 50:
                    diagnosis = """This incident closely matches a previously resolved incident.

PREVIOUS INCIDENT SUMMARY:
A similar incident was previously recorded in the incident memory.

ROOT CAUSE:
Based on the retrieved incident, the root cause appears to be related to the service issue.

RECOVERY STEPS:
• Review the incident details
• Apply standard recovery procedures
• Verify service health after recovery

CURRENT RECOMMENDATION:
Apply the same recovery steps and monitor the service closely."""
                
                root_cause = self._extract_root_cause(diagnosis)
                resolution_steps = self._extract_resolution_steps(diagnosis)
                
                if similar_count >= 5:
                    confidence = "High"
                elif similar_count >= 1:
                    confidence = "Medium"
                else:
                    confidence = "Low"
                
                return IncidentResponse(
                    diagnosis=diagnosis,
                    model_used=result.model_used,
                    cost=result.total_cost,
                    similar_incidents_found=similar_count,
                    confidence=confidence,
                    root_cause=root_cause,
                    resolution_steps=resolution_steps[:5] if resolution_steps else ["See diagnosis"]
                )
                
            except Exception as e:
                print(f"⚠️ cascadeflow error: {e}")
        
        fallback_diagnosis = """This incident closely matches a previously resolved incident.

PREVIOUS INCIDENT SUMMARY:
A similar incident was previously recorded in the incident memory.

ROOT CAUSE:
Based on the retrieved incident, the root cause appears to be related to the service issue.

RECOVERY STEPS:
• Review the incident details
• Apply standard recovery procedures
• Verify service health after recovery

CURRENT RECOMMENDATION:
Apply the same recovery steps and monitor the service closely."""
        
        return IncidentResponse(
            diagnosis=fallback_diagnosis,
            model_used="fallback",
            cost=0.0,
            similar_incidents_found=similar_count,
            confidence="Medium",
            root_cause="See diagnosis",
            resolution_steps=["See diagnosis"]
        )