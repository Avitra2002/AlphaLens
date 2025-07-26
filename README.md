# 🔍 AlphaLens – Smart Investment Research Assistant

**AlphaLens** is an AI-powered research assistant designed to supercharge institutional-grade investment analysis. It combines real-time macroeconomic insights, intelligent document analysis, and powerful knowledge graph visualizations—driven by local and cloud-based LLMs.

---

## 🚀 What It Does

### 📈 1. Macro Analysis Module (**Trends AI**)
- Scrapes macroeconomic indicators from trusted sources (World Bank, IMF, FRED).
- Summarizes country/region-level economic trends using a large language model.
- Provides actionable insights:

  > *"High inflation in Argentina → Fixed income likely to outperform equities."*

---

### 🧠 2. Entity Intelligence Module (**InsightVault**)
- Ingests structured and unstructured data (e.g., 10-Ks, news, press releases).
- Extracts relationships between companies, executives, investors.
- Visualizes connections in an interactive knowledge graph:

  > *"BlackRock → invested in → Company XYZ."*

---

### 💬 3. LLM Chatbot Interface
Ask investment-grade queries like:
- *“What’s the outlook for emerging markets this year?”*
- *“Which firms are most connected to Temasek in 2023?”*
- *“What sectors are most exposed to China’s slowdown?”*

---

## 🧱 Tech Stack

### 📊 Data Sources
- World Bank API, IMF API, FRED  
- EDGAR (10-Ks), Yahoo Finance, News APIs

### 🧠 LLM
- Local models via [Ollama](https://ollama.com/) (e.g., LLaMA 3, Mistral, etc.)
- *(Future)* OpenAI GPT-4 API

### 🧠 NLP / Information Extraction
- [`spaCy`](https://spacy.io/), [`transformers`](https://huggingface.co/transformers/)
- *(Optional)* OpenAI function calling or LangChain tools

### 📚 Context Management (RAG)
- [`LangChain`](https://www.langchain.com/)
- [`FAISS`](https://github.com/facebookresearch/faiss)

### 🧠 Agent & Tool Routing
- LangChain `AgentExecutor`

### 🌐 API Layer
- [`FastAPI`](https://fastapi.tiangolo.com/) (used in place of broken `wbdata` APIs)

### 🧮 Knowledge Graph
- [`Neo4j`](https://neo4j.com/) or optionally `ArangoDB`
- Visualization via `NetworkX`, `PyVis`,

### 💾 Storage & Auth
- [`Supabase`](https://supabase.com/) (PostgreSQL + file storage)
- Auth via Supabase Auth, Auth0, or Clerk (based on frontend needs)

### 💻 Frontend
- [`Next.js`](https://nextjs.org/) + React (deployed via Vercel)

### 🔙 Backend Orchestration
- Node.js backend for:
  - Serving LLM outputs
  - Handling frontend requests
  - Orchestrating NLP, APIs, and database logic

### 💬 Chat Interface
- React-based chatbot UI  

### 📦 Containerization
- Dockerized backend and LangChain/LLM modules

---

## 🛠️ Setup Instructions (Coming Soon)
This section will contain:
- 🧩 Installation steps
- ⚙️ `.env` configuration
- 🧪 Developer and contribution guidelines

---

## 📄 License

MIT License *(or add your preferred license)*

---

## 🤝 Contributions

Open to contributions from:
- Data scientists
- Full-stack developers
- NLP and LLM researchers

Feel free to fork, open issues, or submit pull requests!

---
