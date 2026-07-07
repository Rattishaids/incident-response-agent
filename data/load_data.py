import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agent import IncidentAgent
from app.models import IncidentMemory

def load_incidents(json_file: str = "data/incidents.json", limit: int = 10):
    print(f"📥 Loading {limit} incidents from {json_file}")
    
    # Initialize agent
    agent = IncidentAgent()
    
    # Delete old bank
    try:
        agent.memory.delete_bank(bank_id=agent.bank_id)
        print("🗑️ Deleted old bank")
    except Exception as e:
        print(f"📌 Could not delete: {e}")
    
    # Load JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Store as JSON (not text!)
    print("📥 Storing incidents as JSON...")
    for item in data[:limit]:
        incident = IncidentMemory(**item)
        
        # Store as JSON
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
        
        agent.memory.retain(
            bank_id=agent.bank_id,
            content=json_content
        )
        print(f"   ✅ Stored {incident.incident_id}")
    
    print(f"✅ Loaded {len(data[:limit])} incidents as JSON!")

if __name__ == "__main__":
    load_incidents("data/incidents.json", limit=50)