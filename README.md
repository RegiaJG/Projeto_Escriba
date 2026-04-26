<div align="center">

# Escriba

### Transcrição, Correção e Sumarização de Áudios com IA 100% Local

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black?style=for-the-badge&logoColor=white)](https://ollama.com)
[![Whisper](https://img.shields.io/badge/OpenAI-Whisper-412991?style=for-the-badge&logo=openai&logoColor=white)](https://github.com/openai/whisper)
[![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-7B2FBE?style=for-the-badge&logo=python&logoColor=white)](https://customtkinter.tomschimansky.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br/>

> **Converta reuniões, aulas, consultas, entrevistas e gravações em PDFs organizados com IA especializada — tudo processado localmente, sem custos de API e sem enviar seus dados para a nuvem.**

<br/>

![Pipeline](https://img.shields.io/badge/Áudio%20→%20Whisper%20→%20Ollama%20→%20Revisão%20→%20PDF-7B2FBE?style=flat-square)

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
- [Perfis de Agente](#-perfis-de-agente)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Roadmap](#️-roadmap)
- [Autor](#-autor)

---

## 🧠 Sobre o Projeto

O **Escriba** nasceu de uma necessidade real dentro da startup **Projeto Portal** — um grupo de desenvolvimento de RPG de mesa que realizava reuniões semanais de 2 a 4 horas. Muitos membros não conseguiam participar integralmente ou assistir às gravações por falta de tempo, gerando desalinhamento e perda de informação.

A ferramenta combina dois modelos de IA rodando **100% na sua máquina**:

- **OpenAI Whisper** — reconhecimento de fala com alta precisão em português
- **LLM local via Ollama** — sumarização inteligente sem depender de APIs externas

O resultado é um **PDF profissional** com resumo estruturado e transcrição completa — pronto para compartilhar, arquivar ou consultar. Com o sistema de **perfis de agente** e **aprendizado por correção**, o Escriba se adapta ao vocabulário e às necessidades específicas de cada projeto ao longo do tempo.

### Por que isso importa?

| Abordagem comum | Escriba |
|---|---|
| Envia áudio para servidores externos | ✅ Processamento 100% local |
| Custos por token / por minuto | ✅ Gratuito após instalação |
| Dependência de conexão com internet | ✅ Funciona completamente offline |
| Dados sensíveis expostos a terceiros | ✅ Total privacidade e controle |
| Agente genérico sem contexto do projeto | ✅ Perfis especializados + contexto customizável |
| Erros de transcrição sem correção | ✅ Aprendizado por correção manual |

---

## 🎬 Demonstração

**Tela inicial — Seus Projetos:**
```
┌─────────────────────────────────────────────────────────────────────┐
│  ESCRIBA                                              + Novo Projeto │
│  Transcrição & Sumarização de Áudios com IA Local                   │
│─────────────────────────────────────────────────────────────────────│
│  Seus Projetos                                                       │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  👥  Projeto Portal                              [Abrir →]  │    │
│  │      Reunião Corporativa  ·  12 tarefas  ·  2026-04-25      │    │
│  └─────────────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  📚  Faculdade 2026                              [Abrir →]  │    │
│  │      Aula / Palestra  ·  5 tarefas  ·  2026-04-20           │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

**Tela de trabalho — Configuração:**
```
← Projetos   Projeto Portal                              ⚙ Perfis

Perfil do Agente:
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  👥 Reunião      │ │  🎙️ Entrevista   │ │  📚 Aula         │
│  Corporativa     │ │  / Podcast       │ │  / Palestra      │
└──────────────────┘ └──────────────────┘ └──────────────────┘
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  ⚖️ Jurídico /  │ │  🏥 Consulta     │ │  ✏️ Personalizado│
│  Ata             │ │  Médica          │ │                  │
└──────────────────┘ └──────────────────┘ └──────────────────┘

Contexto do Projeto:
┌─────────────────────────────────────────────────────────────┐
│  Membros: Lucas (PO), Ana (Dev), Pedro (Design).            │
│  Projeto XPTO. Siglas: PBI = Product Backlog Item.          │
└─────────────────────────────────────────────────────────────┘

Arquivo de Áudio:
[📄 Arquivo]  [📂 Pasta]  [ reunioes/sprint_abril/ _________ ]

Modelo Ollama: [ llama3.2 ▼ ]    Modelo Whisper: [ base ▼ ]

              [ ▶   INICIAR                                   ]
```

**Exemplo de PDF gerado:**
```
Escriba
Projeto: Projeto Portal  ·  Perfil: Reunião Corporativa  ·  25/04/2026 14:32
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Resultado

# Reunião de Planejamento — Sprint de Abril

📋 Visão Geral
A reunião tratou do planejamento do sprint de abril com foco na
entrega do módulo de autenticação e revisão do PBI backlog...

📌 Pontos Principais
• Definição das histórias de usuário para o sprint
• Revisão de bugs críticos reportados pelo time de QA

✅ Decisões e Ações
• Lucas ficou responsável pela revisão do PBI — entrega até dia 30
• Ana irá implementar o módulo de login

🎯 Próximos Passos
• Daily às 09h a partir de segunda-feira

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Transcrição Original (gerada pelo Whisper)
[transcrição literal do áudio com marcação de possíveis erros...]
```

---

## ✨ Funcionalidades

- 🗂️ **Sistema de projetos** — organize seus trabalhos em projetos separados com histórico e configurações individuais
- 🤖 **Perfis de agente especializados** — 5 perfis prontos (Reunião, Entrevista, Aula, Jurídico, Médico) + perfil personalizável
- 📝 **Campo de contexto** — alimente o agente com nomes, siglas e termos do seu projeto para reduzir erros
- 🔁 **Aprendizado por correção** — o agente aprende com suas revisões manuais e melhora a cada sessão
- ✍️ **Editor de revisão integrado** — revise e corrija o resultado antes de exportar o PDF
- 🎙️ **Transcrição automática** em português com OpenAI Whisper
- 🧠 **Sumarização inteligente** com LLM local via Ollama
- 📄 **Geração de PDF** com resumo estruturado + transcrição completa
- 🖥️ **Interface gráfica** moderna (CustomTkinter, dark mode, redimensionável)
- 📄 **Arquivo único ou pasta** — processe um áudio isolado ou uma pasta inteira em sequência
- 🔒 **100% offline** — nenhum dado é enviado para servidores externos
- 🎚️ **Configurável** — escolha o modelo Whisper e Ollama pela interface
- 🎵 **Multi-formato** — `.mp3`, `.wav`, `.m4a`, `.ogg` e `.flac`
- ⚡ **Otimizado** — modelo Whisper carregado uma única vez por sessão

---

## 🔬 Pipeline Técnico

```
┌───────────────────────────────────────────────────────────────────┐
│                         ESCRIBA v6.0                              │
│                                                                   │
│  ┌──────────┐   ┌──────────────┐   ┌──────────────────────────┐  │
│  │  Arquivo │   │    Whisper   │   │       Ollama Local        │  │
│  │  de Áudio│──▶│  Transcrição │──▶│  Perfil + Contexto +     │  │
│  │          │   │  local PT-BR │   │  Correções anteriores     │  │
│  └──────────┘   └──────────────┘   └────────────┬─────────────┘  │
│                                                  │                │
│  ┌──────────────────────────────────────────┐    │                │
│  │  corrections.json  ◀────────────────────┼────┘                │
│  │  (aprendizado por correção manual)       │  ▲                  │
│  └──────────────────────────────────────────┘  │                  │
│                                                 │                  │
│                              ┌──────────────────┴──────────────┐  │
│                              │     Editor de Revisão           │  │
│                              │  [Finalizar] [Corrigir+Salvar]  │  │
│                              └──────────────────┬──────────────┘  │
│                                                 │                  │
│                                      ┌──────────▼──────────────┐  │
│                                      │    ReportLab PDF        │  │
│                                      │  Resultado + Transcrição│  │
│                                      └─────────────────────────┘  │
└───────────────────────────────────────────────────────────────────┘
```

### Fluxo de dados

1. O usuário cria ou seleciona um **projeto** com contexto e perfil de agente
2. Seleciona um **arquivo único** ou uma **pasta** de áudios
3. O **Whisper** transcreve o áudio localmente em português
4. O **prompt** é montado com: persona do perfil + aviso de alucinações + contexto do projeto + correções anteriores + instruções + transcrição
5. O **Ollama** processa e retorna o resultado estruturado
6. O usuário revisa no **editor integrado** e pode salvar correções para aprendizado
7. O **PDF** é exportado com resultado e transcrição originais

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Função | Por quê |
|---|---|---|
| **Python 3.10+** | Linguagem principal | Ecossistema de IA maduro e produtivo |
| **OpenAI Whisper** | Speech-to-Text | Melhor modelo open-source para PT-BR |
| **Ollama** | LLM local para sumarização | Privacidade total, zero custo, alta qualidade |
| **CustomTkinter** | Interface gráfica | UI moderna sem frameworks pesados |
| **ReportLab Platypus** | Geração de PDF | Controle completo sobre layout e estilos |
| **difflib** | Detecção de correções | Comparação de texto sem dependências externas |
| **Requests** | Comunicação HTTP com Ollama | Simples e sem overhead |

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
>
> Para melhor qualidade em análises especializadas (jurídico, médico), recomenda-se modelos maiores como `llama3.1:70b` ou `qwen2.5:72b` via Ollama — exigem GPU ou mais RAM.

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

# 4. Inicie o servidor Ollama
ollama serve
```

---

## 🖥️ Como Usar

```bash
# Com o Ollama rodando em segundo plano:
python escriba.py
```

**Passo a passo:**

1. **Crie ou abra um projeto** na tela inicial
2. **Escolha um perfil de agente** clicando no card desejado
3. **Adicione contexto** (opcional, mas recomendado): nomes dos participantes, siglas, termos específicos do seu projeto
4. **Selecione o áudio**: `📄 Arquivo` para um único arquivo ou `📂 Pasta` para múltiplos
5. **Configure os modelos** Ollama e Whisper conforme necessário
6. Clique em **▶ INICIAR** e acompanhe o log em tempo real
7. Ao concluir: **Finalizar** para exportar diretamente, ou **Revisar Texto** para editar antes de exportar
8. Se revisado: **Corrigir e Finalizar** salva as diferenças para que o agente aprenda nas próximas tarefas

> 💡 **Dica para múltiplos arquivos:** nomeie os arquivos em ordem numérica para garantir o processamento na sequência correta.
> Exemplo: `Reunião 1.mp3`, `Reunião 2.mp3`, `Reunião 3.mp3`

**Modelos Whisper disponíveis:**

| Modelo | Velocidade | Precisão | Memória |
|--------|-----------|----------|---------|
| `tiny`   | ⚡⚡⚡⚡⚡ | ⭐⭐      | ~1 GB   |
| `base`   | ⚡⚡⚡⚡  | ⭐⭐⭐    | ~1 GB   |
| `small`  | ⚡⚡⚡    | ⭐⭐⭐⭐  | ~2 GB   |
| `medium` | ⚡⚡      | ⭐⭐⭐⭐⭐ | ~5 GB   |
| `large`  | ⚡        | ⭐⭐⭐⭐⭐ | ~10 GB  |

---

## 🤖 Perfis de Agente

O Escriba vem com 5 perfis prontos e 1 perfil personalizável:

| Perfil | Ideal para | Saída esperada |
|---|---|---|
| 👥 **Reunião Corporativa** | Reuniões de equipe, sprints, alinhamentos | Visão geral, pontos principais, decisões, próximos passos |
| 🎙️ **Entrevista / Podcast** | Entrevistas, podcasts, conversas gravadas | Tema central, tópicos, insights, conclusões |
| 📚 **Aula / Palestra** | Aulas, apresentações, palestras | Conceitos-chave, conteúdo estruturado, exemplos |
| ⚖️ **Jurídico / Ata** | Atas formais, contratos, reuniões jurídicas | Ata formal, deliberações, linguagem técnica |
| 🏥 **Consulta Médica** | Consultas, anamneses, laudos em áudio | Queixa, histórico, conduta, orientações |
| ✏️ **Personalizado** | Qualquer uso específico | Definido pelo usuário |

Perfis customizados podem ser criados, editados e excluídos diretamente pela interface em **⚙ Perfis**.

---

## 📁 Estrutura do Projeto

```
escriba/
├── escriba.py                    # Aplicação principal (único arquivo)
├── profiles/                     # Perfis de agente (JSON)
│   ├── reuniao.json
│   ├── entrevista.json
│   ├── aula.json
│   ├── juridico.json
│   ├── medico.json
│   └── personalizado.json
├── projects/                     # Dados por projeto (criado automaticamente)
│   └── nome-do-projeto/
│       ├── project.json          # Configurações e metadados
│       ├── corrections.json      # Histórico de aprendizado
│       └── tasks/                # Resultados das tarefas
│           └── 20260425_143022.json
└── README.md
```

> Os diretórios `profiles/` e `projects/` são criados automaticamente na primeira execução.

---

## 🗺️ Roadmap

- [x] Transcrição local com Whisper
- [x] Sumarização com LLM local via Ollama
- [x] Interface gráfica com CustomTkinter (dark mode)
- [x] Suporte a múltiplos formatos de áudio
- [x] Sistema de projetos com histórico
- [x] Perfis de agente especializados (5 built-in + personalizável)
- [x] Campo de contexto por projeto
- [x] Prompt consciente de alucinações do Whisper
- [x] Editor de revisão integrado pós-processamento
- [x] Aprendizado por correção manual (few-shot local)
- [x] Janela redimensionável
- [ ] Tela inicial animada com apresentação do Escriba
- [ ] Tutorial interativo de uso integrado à interface
- [ ] Suporte a modelos maiores para análises especializadas
- [ ] Detecção automática dos modelos Ollama instalados
- [ ] Seleção de idioma de transcrição pela interface
- [ ] Exportação para `.docx` além de `.pdf`
- [ ] Suporte a vídeos (`.mp4`, `.mkv`) via extração de áudio com FFmpeg
- [ ] Empacotamento como executável (.exe) com PyInstaller

---

## 👤 Autor

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
