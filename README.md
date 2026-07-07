
# 🚨 Incident Response Agent

> An AI-powered incident response system with persistent memory that remembers past incidents and provides intelligent diagnoses.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.110.0-green.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/LangGraph-0.0.20-orange.svg" alt="LangGraph">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</p>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Team](#team)
- [Architecture](#architecture)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Demo](#demo)
- [Links](#links)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The **Incident Response Agent** is an AI-powered system designed to help DevOps and SRE teams quickly diagnose and resolve production incidents. It leverages **Hindsight** for persistent memory storage and **cascadeflow** for intelligent model routing, enabling it to learn from past incidents and provide accurate, context-aware diagnoses.

### How It Works

When an engineer reports an incident, the agent:

1. **Searches its memory** for similar past incidents using semantic search
2. **Retrieves the most relevant** incident details
3. **Generates a structured diagnosis** including root cause and resolution steps
4. **Routes the query** to the optimal LLM model based on complexity
5. **Learns from the interaction** by storing new incident data

---

## Features

### 🧠 Persistent Memory
- Stores every incident with full context (symptoms, root cause, resolution)
- Uses **Hindsight's** semantic search to find similar incidents
- Automatically extracts entities, relationships, and facts from incidents
- Memory persists across sessions, enabling continuous learning

### 💰 Intelligent Model Routing
- Uses **cascadeflow** to route queries to the optimal LLM
- Simple queries → cheap, fast models
- Complex queries → powerful, reasoning models
- **Cost savings of 40-85%** on LLM API costs

### 🚀 Fast & Responsive
- Sub-5ms overhead for routing decisions
- Real-time streaming responses
- API-first design for easy integration

### 🎯 Structured Diagnoses
- **Previous Incident Summary** - What happened in the past
- **Root Cause** - What caused the incident
- **Recovery Steps** - How it was solved previously
- **Current Recommendation** - What to do now

### 📊 Beautiful UI
- Clean, modern dashboard
- Real-time analysis with loading states
- Color-coded confidence indicators
- One-click quick test alerts

---

## 👥 Team TwinSparks 🔥

| Role | Name | GitHub |
|------|------|--------|
| **Team Lead / Developer** | Revathi | [@revathi](https://github.com/revathi) |
| **Developer** | Rattishkumar SS | [@rattishkumar](https://github.com/rattishkumar) |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                              │
│                     (HTML/CSS/JavaScript)                           │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         FASTAPI BACKEND                             │
│                          (app/api.py)                               │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      INCIDENT AGENT (LangGraph)                     │
│                         (app/agent.py)                              │
│                                                                      │
│   ┌─────────────┐    ┌─────────────┐    ┌───────────────────────┐  │
│   │   Intake    │───▶│   Memory    │───▶│      Investigate      │  │
│   │   Node      │    │    Node     │    │        Node           │  │
│   └─────────────┘    └─────────────┘    └───────────────────────┘  │
│          │                   │                       │              │
│          ▼                   ▼                       ▼              │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │                     Response Generation                     │  │
│   └─────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
          │                   │                       │
          ▼                   ▼                       ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐
│   HINDSIGHT     │  │  cascadeflow    │  │   GROQ / LLM        │
│   MEMORY        │  │  ROUTING        │  │   PROVIDER          │
└─────────────────┘  └─────────────────┘  └─────────────────────┘
```

---

## Technologies Used

| Technology | Purpose |
|------------|---------|
| **FastAPI** | Backend API framework |
| **LangGraph** | Agent orchestration and workflow management |
| **Hindsight Cloud** | Persistent memory storage and semantic search |
| **cascadeflow** | Intelligent model routing and cost optimization |
| **Groq** | Fast LLM inference with generous free tier |
| **HTML/CSS/JS** | Frontend UI |

### LLM Models Used

| Model | Provider | Cost | Use Case |
|-------|----------|------|----------|
| qwen/qwen3-32b | Groq | $0.000375/token | Simple queries, first attempt |
| llama-3.3-70b-versatile | Groq | $0.00562/token | Complex reasoning, fallback |

---

## Prerequisites

- **Python 3.10+**
- **Groq API Key** (free) - [Get from Groq Console](https://console.groq.com)
- **Hindsight Cloud API Key** - [Sign up](https://ui.hindsight.vectorize.io) (use code `MEMHACK625` for $50 free credits)
- **Git** (for cloning)
- **VS Code** (recommended) or any text editor

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Revathi2006/incident-response-agent.git
cd incident-response-agent
```

### 2. Create and Activate Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# .env
HINDSIGHT_API_KEY=your-hindsight-api-key-here
GROQ_API_KEY=your-groq-api-key-here
```

---

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `HINDSIGHT_API_KEY` | Your Hindsight Cloud API key | ✅ Yes |
| `GROQ_API_KEY` | Your Groq API key | ✅ Yes |
| `HINDSIGHT_URL` | Hindsight API endpoint (default: api.hindsight.vectorize.io) | ❌ No |

### Incident Data

Incidents are stored in `data/incidents.json`. Each incident should have:

```json
{
  "incident_id": "INC-001",
  "title": "Payment API complete outage",
  "symptoms": "All payment requests failing with HTTP 503",
  "root_cause": "Database connection pool exhausted",
  "resolution": "Restarted PostgreSQL, increased pool size",
  "affected_service": "Payment Gateway",
  "severity": "Critical",
  "duration_minutes": 45,
  "detection_method": "AlertManager"
}
```

---

## Running the Application

### Command to Load Incident Data

```bash
python data/load_data.py
```

**Expected Output:**
```
📥 Loading 10 incidents from data/incidents.json
🗑️ Deleted old bank
📥 Storing incidents as JSON...
   ✅ Stored INC-001
   ✅ Stored INC-002
   ✅ Stored INC-003
   ...
✅ Loaded 10 incidents as JSON!
```

### Command to Run the Server

```bash
python run.py
```

**Expected Output:**
```
🚀 Starting Incident Response Agent...
==================================================
✅ API keys found
📡 Starting FastAPI server at http://localhost:8000
📚 API Docs at http://localhost:8000/docs
==================================================
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Command to Test the API

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Analyze an Incident (PowerShell)
```powershell
$body = @{alert="Payment service is returning 503 errors"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/incident" -Method POST -Body $body -ContentType "application/json"
```

#### Analyze an Incident (curl)
```bash
curl -X POST "http://localhost:8000/incident" \
  -H "Content-Type: application/json" \
  -d '{"alert": "Payment service is returning 503 errors"}'
```

### Open the UI

1. Open `index.html` in your browser
   - Double-click the file, or
   - Use VS Code Live Server extension, or
   - Run `python -m http.server 8080` and go to `http://localhost:8080`

---

## API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Root endpoint with status |
| `GET` | `/health` | Detailed health check |
| `POST` | `/incident` | Analyze an incident alert |

### POST `/incident`

**Request Body:**
```json
{
  "alert": "Payment service is returning 503 errors"
}
```

**Response:**
```json
{
  "diagnosis": "This incident closely matches a previously resolved incident...",
  "model_used": "llama-3.3-70b-versatile",
  "cost": 0.00024,
  "confidence": "High",
  "root_cause": "Database connection pool exhausted...",
  "resolution_steps": [
    "Restarted PostgreSQL",
    "Increased connection pool size",
    "Added connection timeout"
  ]
}
```

### Swagger Documentation

Access the interactive API docs at: `http://localhost:8000/docs`

---

## Project Structure

```
incident-response-agent/
│
├── app/
│   ├── __init__.py
│   ├── agent.py           # Core agent logic
│   ├── api.py             # FastAPI endpoints
│   ├── config.py          # Configuration settings
│   └── models.py          # Pydantic models
│
├── data/
│   ├── incidents.json     # Incident dataset
│   └── load_data.py       # Data loading script
│
├── docs/
│   └── README.md          # Project documentation
│
├── .env                   # Environment variables (don't commit!)
├── .env.example           # Example environment file
├── .gitignore             # Git ignore file
├── index.html             # Beautiful UI
├── LICENSE                # MIT License
├── requirements.txt       # Python dependencies
├── run.py                 # Application entry point
└── test_cascade.py        # Test script
```

---

## Demo

### Quick Demo Steps

1. **Load the data:**
   ```bash
   python data/load_data.py
   ```

2. **Start the server:**
   ```bash
   python run.py
   ```

3. **Open the UI:**
   - Open `index.html` in your browser

4. **Enter an incident:**
   - Type: "Payment service is returning 503 errors"
   - Or click a quick test button

5. **View the diagnosis:**
   - The agent analyzes the incident
   - Shows similar past incidents
   - Provides root cause and resolution steps
   - Displays confidence and cost

### Demo Video

[![Demo Video](https://img.youtube.com/vi/your-video-id/0.jpg)](https://youtu.be/your-demo-video-link)

**Link:** [https://youtu.be/your-demo-video-link](https://youtu.be/your-demo-video-link)

---

## Links

### Project Links
- **GitHub Repository**: [https://github.com/Revathi2006/incident-response-agent](https://github.com/Revathi2006/incident-response-agent)
- **Demo Video**: [https://youtu.be/your-demo-video-link](https://youtu.be/your-demo-video-link)
- **Article**: [https://medium.com/@Revathi2006/incident-response-agent](https://medium.com/@Revathi2006/incident-response-agent)
- **LinkedIn Post**: [https://linkedin.com/posts/Revathi2006/incident-response-agent](https://linkedin.com/posts/Revathi2006/incident-response-agent)
- **Reddit Post**: [https://reddit.com/r/your-subreddit/comments/incident-response-agent](https://reddit.com/r/your-subreddit/comments/incident-response-agent)

### Technology Links
- **Hindsight**: [https://github.com/vectorize-io/hindsight](https://github.com/vectorize-io/hindsight)
- **cascadeflow**: [https://github.com/lemony-ai/cascadeflow](https://github.com/lemony-ai/cascadeflow)
- **Groq**: [https://console.groq.com](https://console.groq.com)

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `Hindsight API key invalid` | Check `.env` file, ensure key is correct |
| `Port 8000 in use` | Change port in `run.py` to 8001 |
| `No incidents found` | Run `python data/load_data.py` |
| `<think>` tags in output | Updated `agent.py` has cleaning logic |

### Getting Help

- [Hindsight Documentation](https://hindsight.vectorize.io/)
- [cascadeflow Documentation](https://docs.cascadeflow.ai/)
- [Groq Console](https://console.groq.com)

---

## License

MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Built with [Hindsight](https://github.com/vectorize-io/hindsight) for memory
- Powered by [cascadeflow](https://github.com/lemony-ai/cascadeflow) for routing
- LLM inference via [Groq](https://groq.com/)

---

## 👥 Team TwinSparks 🔥

| Role | Name | GitHub |
|------|------|--------|
| **Team Lead / Developer** | Revathi | [@Revathi2006](https://github.com/revathi) |
| **Developer** | Rattishkumar SS | [@Rattishaids](https://github.com/rattishkumar) |

---

<p align="center">
  <strong>Made with ❤️ by Team TwinSparks 🔥</strong><br>
  <strong>for the Hindsight x cascadeflow Hackathon</strong>
</p>

---
