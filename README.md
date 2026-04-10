 ***Assistant IA — Déclaration Intelligente de Sinistre***

🔍 Problématique
Le traitement des sinistres dans le secteur de l'assurance est aujourd'hui :

Lent — procédures administratives longues et répétitives
Coûteux — intervention humaine à chaque étape
Sujet aux erreurs — incohérences documentaires, saisies manuelles


**Comment utiliser l'IA Générative pour rendre ce processus plus rapide, plus fiable et moins coûteux ?**


**🎥 Vue d'ensemble du pipeline**
Le système guide l'assuré à travers un pipeline d'agents IA orchestrés, du premier message jusqu'au rapport final.
1. Assuré (chatbot)
2. Orchestrateur
3. Guardrail → Analyste → Estimateur
4. Générateur LaTeX
5. FastAPI → PDF

**🛠️ Comment ça marche**

Conversation : le chatbot guide l'assuré et collecte la description du sinistre ainsi que les preuves (documents, photos).
Validation : l'agent Guardrail vérifie la cohérence entre les documents fournis et la déclaration.
Analyse : l'agent Analyste extrait la nature des dommages, la localisation et les informations clés.
Estimation : l'agent Estimateur propose une première évaluation chiffrée des coûts de réparation.
Rapport : le pipeline génère automatiquement un rapport PDF structuré via LaTeX et le stocke sur Vercel Blob.


**✨ Fonctionnalités**

 Chatbot conversationnel pas-à-pas pour l'assuré
 Analyse d'images de sinistre par vision IA (BLIP)
 Extraction de texte depuis PDF et DOCX (Docling)
 Vérification automatique de la cohérence des preuves
 Estimation automatisée des coûts de réparation
 Génération d'un rapport PDF en LaTeX
 Hébergement cloud du rapport via Vercel Blob
 Authentification sécurisée avec Clerk


**🧰 Stack technique**
*Backend*
TechnologieRôlePython 3.12Langage principalFastAPIAPI REST asynchroneUvicornServeur ASGIPydanticValidation & sérialisation des donnéesPillow (PIL)Traitement des images avant analyse IA
*Frontend*
TechnologieRôleNext.js 14 (React)Framework web moderneTypeScriptTypage statiqueTailwind CSS / Shadcn/uiDesign professionnel & responsiveLucide ReactBibliothèque d'icônesClerkAuthentification & gestion utilisateurs
*Intelligence Artificielle*
TechnologieRôleLangChainOrchestration du pipeline des agents IAGroq API (Llama)LLM ultra-rapide pour la réactivité du chatbotHugging Face / BLIPModèle de vision pour l'analyse d'images
*Outils & Infrastructure*
TechnologieRôleLaTeX / xelatexGénération de rapports PDF structurésVercel BlobStockage cloud et partage des rapportsDoclingExtraction de texte depuis PDF et DOCX

**📁 Structure du projet**
Assistant_AI/
├── backend/          # API FastAPI + agents IA (Python)
├── frontend/         # Application Next.js (TypeScript)
├── .gitignore
└── README.md

**🚀 Installation**
Prérequis

Python 3.12+
Node.js 18+
LaTeX avec xelatex (Installation TeX Live)

*1. Cloner le projet*
bashgit clone https://github.com/Nada-naffeti/Assistant_AI.git
cd Assistant_AI
*2. Backend*
bashcd backend
python -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
*3. Frontend*
bashcd frontend
npm install
npm run dev
L'application est disponible sur http://localhost:3000.

**🔐 Variables d'environnement**
Créez un fichier .env dans chaque dossier. Ne commitez jamais ce fichier — il est déjà dans le .gitignore.
*backend/.env*
envGROQ_API_KEY=your_groq_api_key
HUGGINGFACE_TOKEN=your_hf_token
VERCEL_BLOB_READ_WRITE_TOKEN=your_vercel_blob_token
*frontend/.env*
envNEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
CLERK_SECRET_KEY=your_clerk_secret_key
NEXT_PUBLIC_API_URL=http://localhost:8000
