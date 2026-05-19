# AI Assistant : Automated Insurance Claim Declaration

An end-to-end AI-powered system that guides policyholders through the insurance claim process, from initial description to structured PDF report automatically.

---

## Problem Statement

Insurance claim processing is traditionally:

- **Slow** : long and repetitive administrative procedures
- **Costly** : human intervention required at every step
- **Error-prone** : document inconsistencies and manual data entry

This project explores how Generative AI can make this process faster, more reliable, and less expensive.

---

## How It Works

The system orchestrates a pipeline of AI agents that process the claim from the first message to the final report.

```
Policyholder (chatbot)
    → Orchestrator
        → Guardrail Agent     (document consistency check)
        → Analyst Agent       (damage extraction & localization)
        → Estimator Agent     (repair cost evaluation)
    → LaTeX Generator
        → FastAPI → PDF Report
```

1. **Conversation** — the chatbot collects the claim description and supporting evidence (documents, photos)
2. **Validation** — the Guardrail agent checks consistency between uploaded documents and the declaration
3. **Analysis** — the Analyst agent extracts damage type, location, and key information
4. **Estimation** — the Estimator agent produces an initial repair cost evaluation
5. **Report** — the pipeline auto-generates a structured PDF via LaTeX and stores it on Vercel Blob

---

## Features

- Step-by-step conversational chatbot for the policyholder
- AI vision analysis of damage images (BLIP)
- Text extraction from PDF and DOCX files (Docling)
- Automatic evidence consistency verification
- Automated repair cost estimation
- LaTeX-based structured PDF report generation
- Cloud report hosting via Vercel Blob
- Secure authentication with Clerk

---

## Tech Stack

**Backend**

| Technology | Role |
|---|---|
| Python 3.12 | Main language |
| FastAPI | Async REST API |
| Uvicorn | ASGI server |
| Pydantic | Data validation & serialization |
| Pillow (PIL) | Image preprocessing |

**Frontend**

| Technology | Role |
|---|---|
| Next.js 14 (React) | Web framework |
| TypeScript | Static typing |
| Tailwind CSS / Shadcn/ui | UI design |
| Lucide React | Icon library |
| Clerk | Authentication & user management |

**AI**

| Technology | Role |
|---|---|
| LangChain | AI agent pipeline orchestration |
| Groq API (Llama) | Ultra-fast LLM for chatbot reactivity |
| Hugging Face / BLIP | Vision model for image analysis |

**Infrastructure**

| Technology | Role |
|---|---|
| LaTeX / xelatex | Structured PDF report generation |
| Vercel Blob | Cloud storage & report sharing |
| Docling | Text extraction from PDF and DOCX |

---

## Project Structure

```
Assistant_AI/
├── backend/       # FastAPI + AI agents (Python)
├── frontend/      # Next.js application (TypeScript)
├── .gitignore
└── README.md
```

---

## Getting Started

**Prerequisites**

- Python 3.12+
- Node.js 18+
- LaTeX with xelatex ([TeX Live](https://www.tug.org/texlive/))

**1. Clone the repository**

```bash
git clone https://github.com/Nada-naffeti/Assistant_AI.git
cd Assistant_AI
```

**2. Backend**

```bash
cd backend
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

**3. Frontend**

```bash
cd frontend
npm install
npm run dev
```

The application runs at `http://localhost:3000`.

---

## Environment Variables

Create a `.env` file in each folder. Never commit it — it is already in `.gitignore`.

`backend/.env`
```
GROQ_API_KEY=your_groq_api_key
HUGGINGFACE_TOKEN=your_hf_token
VERCEL_BLOB_READ_WRITE_TOKEN=your_vercel_blob_token
```

`frontend/.env`
```
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
CLERK_SECRET_KEY=your_clerk_secret_key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Author

**Nada Naffeti** — Data Science & AI Engineering Student @ [ESSAI](https://www.essai.tn/)

[LinkedIn](https://linkedin.com/in/nada-naffeti) · [GitHub](https://github.com/Nada-naffeti)
