# NEXUS AI — Agentic Business Operations Copilot

An open-source portfolio project demonstrating how an AI-powered business operations platform can qualify leads, triage customer requests, retrieve answers from a company knowledge base, and draft human-reviewable responses.

> **Portfolio positioning:** Generative AI • Agentic Workflows • LangGraph • RAG • Streamlit • Human-in-the-loop AI

## What it does

NEXUS AI combines a lightweight agent workflow with a business dashboard:

1. **Lead intelligence** — estimates lead priority from budget, urgency, intent, and company fit.
2. **Request understanding** — classifies incoming messages as sales, support, billing, or general.
3. **Knowledge retrieval** — retrieves relevant passages from the local knowledge base.
4. **Response drafting** — drafts a tailored reply using the retrieved context.
5. **Human review** — presents a recommendation and draft for a person to approve or edit. It does not send messages automatically.
6. **Analytics** — displays request volume, categories, lead priorities, and workflow outcomes.

The app works in **demo mode without an API key**. Add a Groq API key to enable LLM-generated summaries and replies.

## Architecture

```text
User / Demo Request
        |
        v
   Streamlit UI
        |
        v
  LangGraph Workflow
        |
        +--> Classify request
        |
        +--> Score lead
        |
        +--> Retrieve knowledge (TF-IDF)
        |
        +--> Draft response (Groq LLM or safe demo fallback)
        |
        v
 Human review + analytics
        |
        v
 SQLite interaction history
```

## Tech stack

- Python 3.10+
- Streamlit
- LangGraph
- LangChain-Groq (optional LLM provider)
- scikit-learn TF-IDF retrieval
- SQLite
- Pandas

No GPU is required. The retrieval layer runs locally; an LLM API is optional.

## Quick start

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/nexus-ai-agentic-operations.git
cd nexus-ai-agentic-operations
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the environment

Copy `.env.example` to `.env` and optionally add your Groq API key.

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
```

Without a key, the app uses a deterministic demo response generator.

### 5. Run the app

```bash
streamlit run app.py
```

## Example workflow

Try this sample message:

> We are a growing e-commerce company and need an AI support assistant. We have a budget of $4,000 and want to launch within one month. Can your team help us?

NEXUS AI will classify the request, estimate its priority, retrieve relevant service information, and draft a contextual response for human review.

## Project structure

```text
nexus-ai/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── data/
│   └── knowledge_base.json
├── nexus/
│   ├── __init__.py
│   ├── graph.py
│   ├── intelligence.py
│   ├── knowledge.py
│   └── storage.py
└── tests/
    └── test_intelligence.py
```

## Responsible automation design

- AI-generated replies are drafts, not automatically sent messages.
- Lead scores are recommendations, not objective judgments about people.
- The demo stores local interaction history in SQLite.
- Do not upload confidential customer data to a third-party LLM.
- Review generated content before using it with customers.

## Roadmap

- [ ] Add CRM integrations (HubSpot / Pipedrive)
- [ ] Add email inbox integration with explicit user authorization
- [ ] Add multilingual response generation
- [ ] Add evaluation dataset and quality dashboard
- [ ] Add role-based access and deployment configuration
- [ ] Add configurable approval policies

## Screenshots

Add your own screenshots after running the app:

- `screenshots/dashboard.png`
- `screenshots/request-analysis.png`

## Author

**Alisha Fida**  
Generative AI • LLM Applications • LangGraph • RAG • AI Automation

GitHub: https://github.com/Alishafd

---

This repository is a working portfolio prototype. Integrations listed in the roadmap are not implemented yet.
