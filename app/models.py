from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class Severity(str, Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class AlertRequest(BaseModel):
    alert: str
    severity: Optional[Severity] = Severity.MEDIUM
    service: Optional[str] = None

class IncidentResponse(BaseModel):
    diagnosis: str
    model_used: str
    cost: float
    similar_incidents_found: int
    confidence: str
    root_cause: Optional[str] = None
    resolution_steps: List[str] = []

class IncidentMemory(BaseModel):
    incident_id: str
    title: str
    symptoms: str
    root_cause: str
    resolution: str
    affected_service: str
    severity: Severity
    duration_minutes: int
    detection_method: str
    
    def to_memory_content(self) -> str:
        return f"""
ID: {self.incident_id}
Title: {self.title}
Symptoms: {self.symptoms}
Root Cause: {self.root_cause}
Resolution: {self.resolution}
Service: {self.affected_service}
Severity: {self.severity.value}
Duration: {self.duration_minutes} min
Detection: {self.detection_method}
"""