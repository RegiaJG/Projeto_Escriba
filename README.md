<div align="center">

# Escriba

### AI-Powered Audio Transcription, Correction & Summarization — 100% Local

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black?style=for-the-badge&logoColor=white)](https://ollama.com)
[![Whisper](https://img.shields.io/badge/OpenAI-Whisper-412991?style=for-the-badge&logo=openai&logoColor=white)](https://github.com/openai/whisper)
[![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-7B2FBE?style=for-the-badge&logo=python&logoColor=white)](https://customtkinter.tomschimansky.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br/>

> **Convert meetings, classes, consultations, interviews and recordings into organized PDFs with specialized AI — everything processed locally, with no API costs and no data sent to the cloud.**

<br/>

![Pipeline](https://img.shields.io/badge/Audio%20→%20Whisper%20→%20Ollama%20→%20Review%20→%20PDF-7B2FBE?style=flat-square)

</div>

---

## 📌 Table of Contents

- [About the Project](#-about-the-project)
- [Demo](#-demo)
- [Features](#-features)
- [Technical Pipeline](#-technical-pipeline)
- [Technologies Used](#️-technologies-used)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [How to Use](#️-how-to-use)
- [Agent Profiles](#-agent-profiles)
- [Project Structure](#-project-structure)
- [Roadmap](#️-roadmap)
- [Author](#-author)

---

## 🧠 About the Project

**Escriba** was born from a real need within the **Projeto Portal** startup — an independent tabletop RPG development group that held weekly meetings lasting 2 to 4 hours. Many members couldn't attend fully or watch recordings afterwards due to time constraints, causing misalignment and information loss.

The tool combines two AI models running **100% on your machine**:

- **OpenAI Whisper** — high-precision speech recognition in Portuguese
- **Local LLM via Ollama** — intelligent summarization without relying on external APIs

The result is a **professional PDF** with a structured summary and full transcription — ready to share, archive or reference. With the **agent profile system** and **correction-based learning**, Escriba adapts to the vocabulary and specific needs of each project over time.

### Why does this matter?

| Common approach | Escriba |
|---|---|
| Sends audio to external servers | ✅ 100% local processing |
| Costs per token / per minute | ✅ Free after installation |
| Requires internet connection | ✅ Works completely offline |
| Sensitive data exposed to third parties | ✅ Full privacy and control |
| Generic agent with no project context | ✅ Specialized profiles + customizable context |
| Transcription errors with no correction | ✅ Correction-based learning |

---

## 🎬 Demo

**Home Screen — Your Projects:**
```
┌─────────────────────────────────────────────────────────────────────┐
│  ESCRIBA                                              + New Project  │
│  Audio Transcription & Summarization with Local AI                  │
│─────────────────────────────────────────────────────────────────────│
│  Your Projects                                                       │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  👥  Portal Project                              [Open →]   │    │
│  │      Corporate Meeting  ·  12 tasks  ·  2026-04-25          │    │
│  └─────────────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  📚  College 2026                                [Open →]   │    │
│  │      Class / Lecture  ·  5 tasks  ·  2026-04-20             │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

**Work Screen — Configuration:**
```
← Projects   Portal Project                              ⚙ Profiles

Agent Profile:
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  👥 Corporate    │ │  🎙️ Interview    │ │  📚 Class        │
│  Meeting         │ │  / Podcast       │ │  / Lecture       │
└──────────────────┘ └──────────────────┘ └──────────────────┘
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  ⚖️ Legal /     │ │  🏥 Medical      │ │  ✏️ Custom       │
│  Minutes         │ │  Consultation    │ │                  │
└──────────────────┘ └──────────────────┘ └──────────────────┘

Project Context:
┌─────────────────────────────────────────────────────────────┐
│  Members: Lucas (PO), Ana (Dev), Pedro (Design).            │
│  Project XPTO. Acronyms: PBI = Product Backlog Item.        │
└─────────────────────────────────────────────────────────────┘

Audio File:
[📄 File]  [📂 Folder]  [ meetings/april_sprint/ __________ ]

Ollama Model: [ llama3.2 ▼ ]    Whisper Model: [ base ▼ ]

              [ ▶   START                                     ]
```

**Example of generated PDF:**
```
Escriba
Project: Portal Project  ·  Profile: Corporate Meeting  ·  04/25/2026 14:32
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Result

# Planning Meeting — April Sprint

📋 Overview
The meeting covered April sprint planning focused on delivering
the authentication module and reviewing the PBI backlog...

📌 Key Points
• Definition of user stories for the sprint
• Review of critical bugs reported by the QA team

✅ Decisions & Actions
• Lucas is responsible for PBI review — deadline April 30
• Ana will implement the login module

🎯 Next Steps
• Daily standup at 9am starting Monday

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Original Transcription (generated by Whisper)
[literal audio transcription with possible error markers...]
```

---

## ✨ Features

- 🗂️ **Project system** — organize your work into separate projects with individual history and settings
- 🤖 **Specialized agent profiles** — 5 built-in profiles (Meeting, Interview, Class, Legal, Medical) + customizable profile
- 📝 **Context field** — feed the agent with names, acronyms and terms from your project to reduce errors
- 🔁 **Correction-based learning** — the agent learns from your manual revisions and improves each session
- ✍️ **Integrated review editor** — review and correct the output before exporting the PDF
- 🎙️ **Automatic transcription** in Portuguese with OpenAI Whisper
- 🧠 **Intelligent summarization** with local LLM via Ollama
- 📄 **PDF generation** with structured summary + full transcription
- 🖥️ **Modern GUI** (CustomTkinter, dark mode, resizable window)
- 📄 **Single file or folder** — process one audio file or an entire folder in sequence
- 🔒 **100% offline** — no data is sent to external servers
- 🎚️ **Configurable** — choose Whisper and Ollama models through the interface
- 🎵 **Multi-format** — `.mp3`, `.wav`, `.m4a`, `.ogg` and `.flac`
- ⚡ **Optimized** — Whisper model loaded only once per session

---

## 🔬 Technical Pipeline

```
┌───────────────────────────────────────────────────────────────────┐
│                         ESCRIBA v6.0                              │
│                                                                   │
│  ┌──────────┐   ┌──────────────┐   ┌──────────────────────────┐  │
│  │  Audio   │   │   Whisper    │   │       Local Ollama        │  │
│  │  File    │──▶│ Transcription│──▶│  Profile + Context +     │  │
│  │          │   │  local PT-BR │   │  Previous corrections     │  │
│  └──────────┘   └──────────────┘   └────────────┬─────────────┘  │
│                                                  │                │
│  ┌──────────────────────────────────────────┐    │                │
│  │  corrections.json  ◀────────────────────┼────┘                │
│  │  (manual correction learning)            │  ▲                  │
│  └──────────────────────────────────────────┘  │                  │
│                                                 │                  │
│                              ┌──────────────────┴──────────────┐  │
│                              │       Review Editor             │  │
│                              │  [Finalize] [Correct+Save]      │  │
│                              └──────────────────┬──────────────┘  │
│                                                 │                  │
│                                      ┌──────────▼──────────────┐  │
│                                      │    ReportLab PDF        │  │
│                                      │  Result + Transcription │  │
│                                      └─────────────────────────┘  │
└───────────────────────────────────────────────────────────────────┘
```

### Data flow

1. The user creates or selects a **project** with context and agent profile
2. Selects a **single file** or **folder** of audio files
3. **Whisper** transcribes the audio locally in Portuguese
4. The **prompt** is assembled with: profile persona + hallucination warning + project context + previous corrections + instructions + transcription
5. **Ollama** processes and returns the structured result
6. The user reviews in the **integrated editor** and can save corrections for learning
7. The **PDF** is exported with the result and original transcription

---

## 🛠️ Technologies Used

| Technology | Role | Why |
|---|---|---|
| **Python 3.10+** | Main language | Mature and productive AI ecosystem |
| **OpenAI Whisper** | Speech-to-Text | Best open-source model for Portuguese |
| **Ollama** | Local LLM for summarization | Full privacy, zero cost, high quality |
| **CustomTkinter** | Graphical interface | Modern UI without heavy frameworks |
| **ReportLab Platypus** | PDF generation | Full control over layout and styles |
| **difflib** | Correction detection | Text comparison without external dependencies |
| **Requests** | HTTP communication with Ollama | Simple and low-overhead |

---

## 📋 Prerequisites

Before starting, you need to have installed:

- **Python 3.10+** → [python.org](https://python.org)
- **Ollama** → [ollama.com](https://ollama.com)
- **FFmpeg** (required for Whisper to process audio)

  ```bash
  # Windows (via winget)
  winget install ffmpeg

  # macOS (via Homebrew)
  brew install ffmpeg

  # Ubuntu/Debian
  sudo apt install ffmpeg
  ```

- **Language model** downloaded in Ollama:

  ```bash
  ollama pull llama3.2
  ```

> **Recommended hardware requirements:**
> Modern CPU (4+ cores). Minimum 8 GB RAM (16 GB recommended for larger Whisper models).
>
> For better quality on specialized analyses (legal, medical), larger models such as `llama3.1:70b` or `qwen2.5:72b` via Ollama are recommended — these require a GPU or more RAM.

---

## 🚀 Installation

```bash
# 1. Clone the repository
git clone https://github.com/RegiaJG/escriba.git
cd escriba

# 2. Create and activate a virtual environment (recommended)
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

# 3. Install dependencies
pip install openai-whisper customtkinter reportlab requests

# 4. Start the Ollama server
ollama serve
```

---

## 🖥️ How to Use

```bash
# With Ollama running in the background:
python escriba.py
```

**Step by step:**

1. **Create or open a project** on the home screen
2. **Choose an agent profile** by clicking the desired card
3. **Add context** (optional but recommended): participant names, acronyms, project-specific terms
4. **Select audio**: `📄 File` for a single file or `📂 Folder` for multiple
5. **Configure models** — Ollama and Whisper as needed
6. Click **▶ START** and follow the real-time log
7. When done: **Finalize** to export directly, or **Review Text** to edit before exporting
8. If reviewed: **Correct and Finalize** saves the differences so the agent learns in future tasks

> 💡 **Tip for multiple files:** name files numerically to ensure correct processing order.
> Example: `Meeting 1.mp3`, `Meeting 2.mp3`, `Meeting 3.mp3`

**Available Whisper models:**

| Model | Speed | Accuracy | Memory |
|--------|-------|----------|--------|
| `tiny`   | ⚡⚡⚡⚡⚡ | ⭐⭐      | ~1 GB  |
| `base`   | ⚡⚡⚡⚡  | ⭐⭐⭐    | ~1 GB  |
| `small`  | ⚡⚡⚡    | ⭐⭐⭐⭐  | ~2 GB  |
| `medium` | ⚡⚡      | ⭐⭐⭐⭐⭐ | ~5 GB  |
| `large`  | ⚡        | ⭐⭐⭐⭐⭐ | ~10 GB |

---

## 🤖 Agent Profiles

Escriba comes with 5 built-in profiles and 1 customizable profile:

| Profile | Best for | Expected output |
|---|---|---|
| 👥 **Corporate Meeting** | Team meetings, sprints, alignments | Overview, key points, decisions, next steps |
| 🎙️ **Interview / Podcast** | Interviews, podcasts, recorded conversations | Central theme, topics, insights, conclusions |
| 📚 **Class / Lecture** | Classes, presentations, talks | Key concepts, structured content, examples |
| ⚖️ **Legal / Minutes** | Formal minutes, contracts, legal meetings | Formal minutes, deliberations, technical language |
| 🏥 **Medical Consultation** | Consultations, anamneses, audio reports | Complaint, history, conduct, guidance |
| ✏️ **Custom** | Any specific use case | Defined by the user |

Custom profiles can be created, edited and deleted directly through the **⚙ Profiles** interface.

---

## 📁 Project Structure

```
escriba/
├── escriba.py                    # Main application (single file)
├── profiles/                     # Agent profiles (JSON)
│   ├── reuniao.json
│   ├── entrevista.json
│   ├── aula.json
│   ├── juridico.json
│   ├── medico.json
│   └── personalizado.json
├── projects/                     # Per-project data (auto-created)
│   └── project-name/
│       ├── project.json          # Settings and metadata
│       ├── corrections.json      # Learning history
│       └── tasks/                # Task results
│           └── 20260425_143022.json
└── README.md
```

> The `profiles/` and `projects/` directories are created automatically on first run.

---

## 🗺️ Roadmap

- [x] Local transcription with Whisper
- [x] Summarization with local LLM via Ollama
- [x] GUI with CustomTkinter (dark mode)
- [x] Support for multiple audio formats
- [x] Project system with history
- [x] Specialized agent profiles (5 built-in + customizable)
- [x] Per-project context field
- [x] Whisper hallucination-aware prompting
- [x] Integrated post-processing review editor
- [x] Manual correction learning (local few-shot)
- [x] Resizable window
- [ ] Animated splash screen / onboarding
- [ ] Interactive tutorial integrated into the interface
- [ ] Support for larger models for specialized analyses
- [ ] Automatic detection of installed Ollama models
- [ ] Language selection for transcription via interface
- [ ] Export to `.docx` in addition to `.pdf`
- [ ] Video support (`.mp4`, `.mkv`) via FFmpeg audio extraction
- [ ] Packaging as executable (.exe) with PyInstaller

---

## 👤 Author

<div align="center">

### Lucas Costa Nogueira

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Lucas%20Costa%20Nogueira-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/lucas-nogueira-017b12191)
[![GitHub](https://img.shields.io/badge/GitHub-RegiaJG-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/RegiaJG)
[![Email](https://img.shields.io/badge/Email-D--Gothsublime%40hotmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:D-Gothsublime@hotmail.com)

</div>

---

<div align="center">

*University Extension Project — Descomplica UniAmérica · 2026*

</div>
