<div align="center">

#  Escriba

### Transcrição e Resumo Inteligente de Reuniões com IA

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Whisper](https://img.shields.io/badge/OpenAI-Whisper-412991?style=for-the-badge&logo=openai&logoColor=white)](https://github.com/openai/whisper)
[![Gemini](https://img.shields.io/badge/Google-Gemini_2.5_Pro-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![ReportLab](https://img.shields.io/badge/ReportLab-PDF-red?style=for-the-badge)](https://www.reportlab.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br/>

> **Converta reuniões de horas em PDFs organizados com resumo inteligente — de 4 horas de gravação para 10~20 minutos de leitura.**

<br/>

![Pipeline](https://img.shields.io/badge/Audio%20MP3%20--%3E%20Whisper%20%2B%20Gemini%20--%3E%20PDF-7B2FBE?style=flat-square)

</div>

---

## 🧠 Sobre o Projeto

O **Escriba** nasceu de uma necessidade real dentro da startup **Projeto Portal** — um grupo de desenvolvimento de RPG de mesa que realizava reuniões semanais de 2 a 4 horas. Muitos membros não conseguiam participar integralmente ou assistir às gravações por falta de tempo, gerando desalinhamento e perda de informação.

A solução foi um script autônomo em Python que:
1. Varre uma pasta em busca de arquivos `.mp3`
2. Transcreve o áudio localmente usando **OpenAI Whisper**
3. Envia a transcrição ao **Gemini 2.5 Pro** para gerar um resumo organizado
4. Exporta tudo em um **PDF profissional** — resumo + transcrição completa

O projeto passou por **41 ciclos de teste** (v0.1 → v4.1) em ambiente real de produção, sendo estabilizado em março de 2026.

---

## ✨ Funcionalidades

- 🎙️ **Transcrição automática** de áudios `.mp3` em português com OpenAI Whisper (local)
- 🧠 **Sumarização inteligente** com Gemini 2.5 Pro via engenharia de prompt contextual
- 📄 **Geração de PDF** com resumo estruturado + transcrição completa
- 📂 **Processamento em lote** — processa todos os `.mp3` de uma pasta automaticamente
- ⏭️ **Idempotência** — pula arquivos que já possuem PDF gerado
- 🛡️ **Blindagem de diretório** — garante execução estável independente de onde é chamado

---

## 🔬 Pipeline Técnico

```
┌──────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌──────────┐
│  .mp3    │────▶│  Whisper local  │────▶│  Gemini 2.5 Pro │────▶│   .pdf   │
│  Áudio   │     │  (transcrição)  │     │  (sumarização)  │     │  Resumo  │
└──────────┘     └─────────────────┘     └─────────────────┘     └──────────┘
```

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Função |
|---|---|
| **Python 3.10+** | Linguagem principal |
| **OpenAI Whisper** | Transcrição de fala para texto (local) |
| **Google Gemini 2.5 Pro** | Sumarização e organização do conteúdo |
| **ReportLab** | Geração do PDF final |
| **python-dotenv** | Gerenciamento seguro da API Key |

---

## 📋 Pré-requisitos

- **Python 3.10+** → [python.org](https://python.org)
- **FFmpeg** (necessário para o Whisper processar áudios)

```bash
# Windows (via winget)
winget install ffmpeg
```

- **API Key do Google Gemini** → [ai.google.dev](https://ai.google.dev)

---

## 🚀 Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/RegiaJG/escriba.git
cd escriba

# 2. Crie e ative um ambiente virtual
python -m venv .venv

# Windows
.venv\Scripts\activate

# 3. Instale as dependências
pip install openai-whisper google-generativeai reportlab python-dotenv

# 4. Configure sua API Key
# Crie um arquivo .env na raiz do projeto:
# GEMINI_API_KEY=sua_chave_aqui
```

---

## 🖥️ Como Usar

```bash
# Coloque os arquivos .mp3 na mesma pasta do script
# Execute:
python escriba.py
```

Os PDFs serão gerados automaticamente na mesma pasta dos áudios.

---

## 📁 Estrutura do Projeto

```
escriba/
├── escriba.py    # Script principal
├── .env          # Sua API Key (não versionar!)
├── .gitignore    # Ignora .env e arquivos gerados
└── README.md     # Este arquivo
```

---

## 🗺️ Roadmap

- [x] Transcrição local com Whisper
- [x] Sumarização com Gemini 2.5 Pro
- [x] Geração de PDF com ReportLab
- [x] Processamento em lote
- [x] 41 ciclos de teste — v0.1 → v4.1
- [ ] Interface gráfica com CustomTkinter
- [ ] Substituição do Gemini por LLM local via Ollama
- [ ] Suporte a múltiplos formatos de áudio
- [ ] Empacotamento como executável (.exe) com PyInstaller

---

## 👨‍💻 Autor

<div align="center">

### Lucas Costa Nogueira

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Lucas%20Costa%20Nogueira-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/lucas-nogueira-017b12191)
[![GitHub](https://img.shields.io/badge/GitHub-RegiaJG-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/RegiaJG)
[![Email](https://img.shields.io/badge/Email-D--Gothsublime%40hotmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:D-Gothsublime@hotmail.com)

</div>

---

<div align="center">

*Projeto de Extensão Universitária — Descomplica UniAmérica · 2026*

</div>
