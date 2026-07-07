#!/usr/bin/env python
import os
import subprocess
import sys

def main():
    print("🚀 Starting Incident Response Agent...")
    print("="*50)
    
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("Please create .env file with:")
        print("  HINDSIGHT_API_KEY=your-key")
        print("  GROQ_API_KEY=your-key")
        sys.exit(1)
    
    with open('.env', 'r') as f:
        env_content = f.read()
        if 'your-hindsight' in env_content or 'your-groq' in env_content:
            print("⚠️  Please update .env with your actual API keys!")
            sys.exit(1)
    
    print("✅ API keys found")
    print("📡 Starting FastAPI server at http://localhost:8000")
    print("📚 API Docs at http://localhost:8000/docs")
    print("="*50)
    
    subprocess.run([
        sys.executable, "-m", "uvicorn", "app.api:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ])

if __name__ == "__main__":
    main()