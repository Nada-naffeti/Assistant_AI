Assistant IA — Déclaration Intelligente de Sinistre


📋 Table des matières

Présentation du projet
Problématique
Fonctionnalités
Architecture multi-agents
Stack technique
Structure du projet
Installation & lancement
Variables d'environnement
Auteure


🎯 Présentation du projet
Ce projet est un assistant IA conversationnel conçu pour automatiser et simplifier la déclaration de sinistres dans le secteur de l'assurance.
L'objectif est de transformer une procédure traditionnellement lente, coûteuse et sujette aux erreurs humaines en une expérience fluide, guidée et intelligente — de la description du sinistre jusqu'à la génération automatique d'un rapport PDF final.

🔍 Problématique
Le traitement des sinistres dans le secteur de l'assurance est souvent :

⏳ Lent — délais administratifs importants
💸 Coûteux — processus très manuel
❌ Sujet aux erreurs — saisies humaines, incohérences documentaires

Comment utiliser l'IA Générative pour rendre ce processus plus rapide, plus fiable et moins coûteux ?

✨ Fonctionnalités

💬 Chatbot intelligent accompagnant l'assuré étape par étape
📄 Analyse automatique des documents et images de sinistre
✅ Validation de cohérence entre preuves et déclarations
💰 Estimation automatisée des coûts de réparation
📑 Génération d'un rapport PDF structuré via LaTeX
☁️ Hébergement cloud des rapports via Vercel Blob


🏗 Architecture multi-agents
Le système repose sur un pipeline d'agents IA orchestrés, chacun ayant un rôle précis :
[Utilisateur / Chatbot]
        │
        ▼
┌─────────────────────────────────────────────────┐
│              Agent Orchestrateur                │
│  Initialise et séquence tous les autres agents  │
│  Gestion des erreurs & communication finale     │
└────────┬────────────┬──────────────┬────────────┘
         │            │              │
         ▼            ▼              ▼
  ┌─────────────┐ ┌──────────┐ ┌──────────────┐
  │  Guardrail  │ │Analyste  │ │  Estimateur  │
  │  (Validation│ │(Analyse  │ │  des coûts   │
  │  cohérence) │ │docs+img) │ │              │
  └─────────────┘ └──────────┘ └──────────────┘
                                      │
                                      ▼
                         ┌──────────────────────┐
                         │  Générateur LaTeX    │
                         │  (Template rapport)  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  FastAPI → xelatex   │
                         │  → Rapport PDF final │
                         └──────────────────────┘
AgentRôleGuardrailVérifie la cohérence entre documents fournis et description du sinistreAnalysteExtrait la nature des dommages, localisation et informations clésEstimateurPropose une première estimation chiffrée des coûts de réparationGénérateur LaTeXSynthétise toutes les données et prépare le code source du rapportOrchestrateurGère le pipeline complet : Validation → Analyse → Estimation → Rapport

🛠 Stack technique
Backend
TechnologieUsagePythonLangage principalFastAPIAPI REST asynchroneUvicornServeur ASGIPydanticValidation & sérialisation des donnéesPillow (PIL)Traitement des images avant analyse IA
Frontend
TechnologieUsageNext.js (React)Framework web moderneTypeScriptTypage statique, code robusteTailwind CSS / Shadcn/uiDesign professionnel & responsiveLucide ReactBibliothèque d'icônesClerkAuthentification & gestion des utilisateurs
Intelligence Artificielle
TechnologieUsageLangChainOrchestration du pipeline des agents IAGroq API (Llama)LLM ultra-rapide pour la réactivité du chatbotHugging Face Transformers (BLIP)Modèle de vision pour l'analyse d'images
Outils & Infrastructure
TechnologieUsageLaTeX / xelatexGénération de rapports PDF structurésVercel BlobStockage cloud et partage des rapports PDFDoclingExtraction de texte depuis PDF et DOCX

📁 Structure du projet
Assistant_AI/
├── backend/          # API FastAPI + agents IA
├── frontend/         # Application Next.js
├── .gitignore
└── README.md

🚀 Installation et lancement
Prérequis

Python 3.12+
Node.js 18+
LaTeX (xelatex) installé sur la machine

Backend
bashcd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
Frontend
bashcd frontend
npm install
npm run dev

🔐 Variables d'environnement
Créez un fichier .env à la racine de chaque dossier (backend/ et frontend/) en vous basant sur les exemples ci-dessous. Ne commitez jamais ce fichier.
backend/.env
envGROQ_API_KEY=your_groq_api_key
HUGGINGFACE_TOKEN=your_hf_token
VERCEL_BLOB_READ_WRITE_TOKEN=your_vercel_blob_token
frontend/.env
envNEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
CLERK_SECRET_KEY=your_clerk_secret_key
NEXT_PUBLIC_API_URL=http://localhost:8000
