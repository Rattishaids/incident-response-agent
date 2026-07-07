#!/usr/bin/env python
"""
Test cascadeflow connectivity
Run: python test_cascade.py
"""

import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("❌ GROQ_API_KEY not found in .env file!")
    print("Please add: GROQ_API_KEY=gsk_xxxxxxxxxxxx")
    exit(1)

print(f"✅ Groq API Key found: {GROQ_API_KEY[:10]}...")

try:
    from cascadeflow import CascadeAgent, ModelConfig
    
    print("🔧 Initializing cascadeflow...")
    
    agent = CascadeAgent(models=[
        ModelConfig(name="qwen/qwen3-32b", provider="groq", cost=0.000375),
        ModelConfig(name="llama-3.3-70b-versatile", provider="groq", cost=0.00562),
    ])
    
    print("✅ cascadeflow initialized successfully!")
    
    print("\n🧪 Testing with a simple query...")
    
    # Create async function to run the test
    async def test_cascade():
        result = await agent.run("What is 2+2?")
        return result
    
    # Run the async function
    result = asyncio.run(test_cascade())
    
    print(f"\n✅ Success!")
    print(f"Answer: {result.content}")
    print(f"Model used: {result.model_used}")
    print(f"Cost: ${result.total_cost:.6f}")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Try: pip install cascadeflow")
    
except Exception as e:
    print(f"❌ Error: {e}")
    
    # Show more details
    if "api_key" in str(e).lower():
        print("\n⚠️ Groq API key might be invalid or missing.")
        print("Check your .env file and make sure GROQ_API_KEY is correct.")
    elif "groq" in str(e).lower():
        print("\n⚠️ Groq provider might not be available.")
        print("Try: pip install 'cascadeflow[groq]'")