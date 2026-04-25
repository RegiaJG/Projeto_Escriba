<div align="center">

# Escriba

### Transcrição e Resumo Inteligente de Áudios com IA 100% Local

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black?style=for-the-badge&logoColor=white)](https://ollama.com)
[![Whisper](https://img.shields.io/badge/OpenAI-Whisper-412991?style=for-the-badge&logo=openai&logoColor=white)](https://github.com/openai/whisper)
[![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-7B2FBE?style=for-the-badge&logo=python&logoColor=white)](https://customtkinter.tomschimansky.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br/>

> **Converta reuniões, aulas, podcasts e gravações em PDFs organizados com resumo inteligente — tudo processado localmente, sem custos de API e sem enviar seus dados para a nuvem.**

<br/>

![Pipeline](https://img.shields.io/badge/Audio%20--%3E%20Whisper%20%2B%20Ollama%20--%3E%20PDF-7B2FBE?style=flat-square)

</div>

---

## 📌 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Demonstração](#-demonstração)
- [Funcionalidades](#-funcionalidades)
- [Pipeline Técnico](#-pipeline-técnico)
- [Tecnologias Utilizadas](#️-tecnologias-utilizadas)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Como Usar](#️-como-usar)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Roadmap](#️-roadmap)
- [Autor](#️-autor)

---

## 🧠 Sobre o Projeto

O **Escriba** nasceu de uma necessidade real dentro da startup **Projeto Portal** — um grupo de desenvolvimento de RPG de mesa que realizava reuniões semanais de 2 a 4 horas. Muitos membros não conseguiam participar integralmente ou assistir às gravações por falta de tempo, gerando desalinhamento e perda de informação.

A ferramenta combina dois modelos de IA rodando **100% na sua máquina**:

- **OpenAI Whisper** — reconhecimento de fala com alta precisão em português
- **LLM local via Ollama** — sumarização inteligente sem depender de APIs externas

O resultado é um **PDF profissional** contendo um resumo organizado em tópicos e a transcrição completa do áudio — pronto para compartilhar, arquivar ou consultar.

### Por que isso importa?

| Abordagem comum | Escriba |
|---|---|
| Envia áudio para servidores externos | ✅ Processamento 100% local |
| Custos por token / por minuto | ✅ Gratuito após instalação |
| Dependência de conexão com internet | ✅ Funciona completamente offline |
| Dados sensíveis expostos a terceiros | ✅ Total privacidade e controle |

---

## 🎬 Demonstração

```
ESCRIBA v5.0
Transcrição & Resumo de Áudios com IA Local  ·  Whisper + Ollama

┌─────────────────────────────────────────────────────┐
│  Pasta de entrada:  [ C:/Reuniões/Agosto    ] [📂]  │
│  Modelo Ollama:     [ llama3.2          ▼ ]         │
│  Modelo Whisper:    [ base              ▼ ]         │
└─────────────────────────────────────────────────────┘

        [ ▶   INICIAR TRANSCRIÇÃO                 ]

  ████████████████████████████░░░░  Processando...

  Log de execução:
  ┌──────────────────────────────────────────────────┐
  │ 🛡️   Pipeline iniciado                          │
  │ 📦   Carregando modelo Whisper 'base'...         │
  │ ✅   Modelo Whisper carregado.                   │
  │ [1/2]  reuniao_agosto.mp3                        │
  │ 🎙️   Transcrevendo: reuniao_agosto.mp3...        │
  │ ✅   Transcrição concluída.                      │
  │ 🧠   Gerando resumo com llama3.2 (Ollama)...     │
  │ ✅   Resumo gerado.                              │
  │ 📄   Salvando PDF: reuniao_agosto.pdf...         │
  │ ✅   PDF salvo.                                  │
  │ ══════════════════════════════════════════════   │
  │ ✅   Concluído! 2/2 arquivo(s) processado(s).    │
  └──────────────────────────────────────────────────┘
```

**Exemplo de PDF gerado:**

```
Arquivo de origem: reuniao_agosto.mp3
────────────────────────────────────────────────────────────────────────────────
RESUMO ORGANIZADO
────────────────────────────────────────────────────────────────────────────────

# Reunião de Planejamento — Sprint de Agosto

📋 Visão Geral
A reunião tratou do planejamento do sprint de agosto, com foco na entrega
do módulo de autenticação e revisão das pendências do mês anterior...

📌 Pontos Principais
• Definição das histórias de usuário para o sprint
• Revisão de bugs críticos reportados pelo time de QA
• Alinhamento sobre prazo de entrega para o cliente X

✅ Decisões e Ações
• João ficou responsável pelo módulo de login — entrega até dia 15
• Maria irá revisar a documentação da API até sexta-feira

🎯 Próximos Passos
• Daily às 09h a partir de segunda-feira
• Revisão do sprint na última sexta do mês

────────────────────────────────────────────────────────────────────────────────
TRANSCRIÇÃO COMPLETA
────────────────────────────────────────────────────────────────────────────────
[transcrição literal do áudio...]
```

---

## ✨ Funcionalidades

- 🎙️ **Transcrição automática** de áudios em português com OpenAI Whisper
- 🧠 **Sumarização inteligente** com LLM local via Ollama
- 📄 **Geração de PDF** com resumo estruturado + transcrição completa
- 🖥️ **Interface gráfica** moderna e intuitiva (CustomTkinter, dark mode)
- 📂 **Processamento em lote** — processa todos os áudios de uma pasta de uma vez
- ⏭️ **Idempotência** — pula arquivos que já possuem PDF gerado
- 🔒 **100% offline** — nenhum dado é enviado para servidores externos
- 🎚️ **Configurável** — escolha o modelo Whisper e o modelo Ollama pela interface
- 🎵 **Multi-formato** — suporte a `.mp3`, `.wav`, `.m4a`, `.ogg` e `.flac`
- ⚡ **Otimizado** — modelo Whisper carregado uma única vez por sessão

---

## 🔬 Pipeline Técnico

```
┌─────────────────────────────────────────────────────────────────┐
│                        ESCRIBA v5.0                             │
│                                                                 │
│  ┌──────────┐     ┌─────────────────┐     ┌─────────────────┐  │
│  │  Arquivo │     │  OpenAI Whisper │     │  Ollama Local   │  │
│  │  de Áudio│────▶│  (transcrição)  │────▶│  llama3.2       │  │
│  │          │     │  local / PT-BR  │     │  (sumarização)  │  │
│  └──────────┘     └─────────────────┘     └────────┬────────┘  │
│                                                     │           │
│                                           ┌─────────▼────────┐  │
│                                           │   ReportLab PDF  │  │
│                                           │   Resumo + Trans │  │
│                                           └──────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Fluxo de dados

1. O usuário seleciona a pasta via interface gráfica
2. O Escriba varre a pasta em busca de arquivos de áudio suportados
3. O modelo **Whisper** é carregado uma única vez na memória
4. Para cada arquivo: transcrição → sumarização → exportação em PDF
5. O resumo é gerado via chamada HTTP ao servidor **Ollama** em `localhost:11434`
6. O PDF final contém o resumo em seções e a transcrição literal completa

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Função | Por quê |
|---|---|---|
| **Python 3.10+** | Linguagem principal | Ecossistema de IA maduro e produtivo |
| **OpenAI Whisper** | Speech-to-Text | Melhor modelo open-source para PT-BR |
| **Ollama** | LLM local para sumarização | Privacidade total, zero custo, alta qualidade |
| **CustomTkinter** | Interface gráfica | UI moderna sem frameworks pesados |
| **ReportLab** | Geração de PDF | Controle completo sobre o layout do documento |
| **Requests** | Comunicação HTTP com Ollama | Simples e confiável |

---

## 📋 Pré-requisitos

Antes de começar, você precisa ter instalado:

- **Python 3.10+** → [python.org](https://python.org)
- **Ollama** → [ollama.com](https://ollama.com)
- **FFmpeg** (necessário para o Whisper processar áudios)

  ```bash
  # Windows (via winget)
  winget install ffmpeg

  # macOS (via Homebrew)
  brew install ffmpeg

  # Ubuntu/Debian
  sudo apt install ffmpeg
  ```

- **Modelo de linguagem** baixado no Ollama:

  ```bash
  ollama pull llama3.2
  ```

> **Requisitos de hardware recomendados:**
> CPU moderna (4+ cores). Mínimo 8 GB de RAM (16 GB recomendado para modelos Whisper maiores).

---

## 🚀 Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/RegiaJG/escriba.git
cd escriba

# 2. Crie e ative um ambiente virtual (recomendado)
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

# 3. Instale as dependências
pip install openai-whisper customtkinter reportlab requests

# 4. Confirme que o Ollama está rodando
ollama serve
```

---

## 🖥️ Como Usar

```bash
# Com o Ollama rodando em segundo plano:
python escriba.py
```

**Passo a passo na interface:**

1. Clique em **📂** e selecione a pasta com seus arquivos de áudio
2. Escolha o **modelo Ollama** disponível na sua máquina (padrão: `llama3.2`)
3. Escolha o **modelo Whisper** de acordo com a precisão desejada:

   | Modelo | Velocidade | Precisão | Uso de memória |
   |--------|-----------|----------|----------------|
   | `tiny`   | ⚡⚡⚡⚡⚡ | ⭐⭐      | ~1 GB          |
   | `base`   | ⚡⚡⚡⚡  | ⭐⭐⭐    | ~1 GB          |
   | `small`  | ⚡⚡⚡    | ⭐⭐⭐⭐  | ~2 GB          |
   | `medium` | ⚡⚡      | ⭐⭐⭐⭐⭐ | ~5 GB          |
   | `large`  | ⚡        | ⭐⭐⭐⭐⭐ | ~10 GB         |

4. Clique em **▶ INICIAR TRANSCRIÇÃO**
5. Acompanhe o progresso no log em tempo real
6. Os PDFs são salvos na mesma pasta dos áudios

---

## 📁 Estrutura do Projeto

```
escriba/
│
├── escriba.py    # Aplicação principal (GUI + pipeline completo)
└── README.md     # Este arquivo
```

> O projeto foi intencionalmente mantido em **um único arquivo** para facilitar a distribuição e o uso sem dependência de estrutura de pacotes complexa.

---

## 🗺️ Roadmap

- [x] Transcrição local com Whisper
- [x] Sumarização com LLM local via Ollama
- [x] Interface gráfica com CustomTkinter
- [x] Processamento em lote
- [x] Suporte a múltiplos formatos de áudio
- [ ] Detecção automática dos modelos Ollama instalados
- [ ] Seleção de idioma de transcrição pela interface
- [ ] Exportação para `.docx` além de `.pdf`
- [ ] Visualização do PDF gerado direto na interface
- [ ] Histórico de arquivos processados
- [ ] Suporte a vídeos (`.mp4`, `.mkv`) via extração de áudio com FFmpeg
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
