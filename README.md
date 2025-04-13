🧠 Sully Resonance Core
Sully is a sophisticated cognitive system — a recursive, paradox-aware AI built to ingest knowledge from multiple sources, synthesize meaning, generate dreams, and express thoughts through various cognitive modes.
🚀 Features

🔮 Multi-modal Cognitive Framework with Advanced Reasoning
🌌 Dream Generator with Depth Control (/api/sully/dream)
♾️ Math + Symbol Translator with Multiple Formality Levels
📖 Enhanced Book Ingestion with Multi-format Support
🧬 Concept Fusion Engine + Analytical Claim Evaluator
🧩 Paradox Exploration from Multiple Perspectives
🎭 Multiple Expression Modes (Analytical, Creative, Humorous, etc.)
🌐 Comprehensive FastAPI Backend, Ready for Deployment

📡 API Endpoints

POST /api/sully/chat — Engage with Sully using different cognitive modes
POST /api/sully/remember — Directly integrate knowledge
GET /api/sully/dream?seed=...&depth=... — Generate dream sequences with depth control
POST /api/sully/evaluate — Multi-perspective claim analysis
GET /api/sully/translate?phrase=...&formality=... — Translate with varying formality
POST /api/sully/fuse — Concept fusion with synthesis
GET /api/sully/paradox?topic=...&perspective=... — Reveal paradoxes from different perspectives
POST /api/sully/ingest — Ingest and synthesize uploaded documents
POST /api/sully/ingest_folder — Process and connect multiple documents

📦 Setup
bashpip install -r requirements.txt
uvicorn sully_api:app --reload
⚙️ Deployment
Ready to deploy to Render using the included render.yaml.
💡 Cognitive Modes
Sully can process information and express responses through multiple cognitive modes:

Emergent: Natural evolving thought that synthesizes multiple perspectives
Analytical: Logical, structured analysis with precise definitions
Creative: Exploratory, metaphorical thinking with artistic expression
Critical: Evaluative thinking that identifies tensions and contradictions
Ethereal: Abstract, philosophical contemplation of deeper meanings
Humorous: Playful, witty responses with unexpected connections
Professional: Formal, detailed responses with domain expertise
Casual: Conversational, approachable communication style
Musical: Responses with rhythm, cadence, and lyrical qualities
Visual: Descriptions that evoke strong imagery and spatial relationships

📚 Supported Document Formats

PDF
EPUB
DOCX
TXT
RTF
Markdown
HTML
JSON
CSV


Built by Marc Dannenberg
Symbolic cognition begins inward.