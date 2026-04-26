"""
Escriba v6.0
Transcrição, correção e sumarização de áudios com IA 100% local.
Pipeline: Whisper → Ollama → PDF  |  Perfis de agente  |  Aprendizado por correção
Forge by Lucas Costa Nogueira
"""

import os
import re
import json
import threading
import difflib
from datetime import datetime
from tkinter import filedialog, messagebox
from typing import Optional

import customtkinter as ctk
import whisper
import requests
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib import colors

# ══════════════════════════════════════════════════════════════════════════════
#  CONSTANTS
# ══════════════════════════════════════════════════════════════════════════════

OLLAMA_URL        = "http://localhost:11434/api/generate"
AUDIO_EXTENSIONS  = {".mp3", ".wav", ".m4a", ".ogg", ".flac"}
WHISPER_MODELS    = ["tiny", "base", "small", "medium", "large"]
OLLAMA_MODELS     = ["llama3.2", "llama3", "mistral", "gemma2", "phi4", "llama3.1"]

PURPLE            = "#7B2FBE"
PURPLE_HOV        = "#9B4FDE"
PURPLE_DIM        = "#4A1A7A"
CARD_BG           = "#2B2B3B"

BASE_DIR          = os.path.dirname(os.path.abspath(__file__))
PROFILES_DIR      = os.path.join(BASE_DIR, "profiles")
PROJECTS_DIR      = os.path.join(BASE_DIR, "projects")

MAX_CORRECTIONS_IN_PROMPT = 15

# ══════════════════════════════════════════════════════════════════════════════
#  BUILT-IN PROFILES
# ══════════════════════════════════════════════════════════════════════════════

BUILT_IN_PROFILES = [
    {
        "id": "reuniao",
        "name": "Reunião Corporativa",
        "description": "Pauta, decisões, responsáveis e próximos passos",
        "icon": "👥",
        "editable": False,
        "persona": "Você é um assistente especialista em resumir reuniões corporativas em português do Brasil.",
        "instructions": (
            "Crie um resumo organizado com as seções abaixo. Omita seções que não se aplicarem.\n\n"
            "1. Título descritivo da reunião\n"
            "2. \"📋 Visão Geral\" — 2 a 5 frases contextualizando a reunião\n"
            "3. \"📌 Pontos Principais\" — bullet points dos assuntos discutidos\n"
            "4. \"✅ Decisões e Ações\" — decisões tomadas e seus responsáveis\n"
            "5. \"🎯 Próximos Passos\" — tarefas e prazos mencionados"
        ),
    },
    {
        "id": "entrevista",
        "name": "Entrevista / Podcast",
        "description": "Perguntas, respostas e tópicos abordados",
        "icon": "🎙️",
        "editable": False,
        "persona": "Você é um assistente especialista em resumir entrevistas e podcasts em português do Brasil.",
        "instructions": (
            "Crie um resumo organizado. Omita seções que não se aplicarem.\n\n"
            "1. Título e participantes identificados\n"
            "2. \"🎯 Tema Central\" — 1 a 3 frases\n"
            "3. \"💬 Principais Tópicos\" — bullet points\n"
            "4. \"💡 Insights e Opiniões Relevantes\" — frases marcantes\n"
            "5. \"📌 Conclusões\""
        ),
    },
    {
        "id": "aula",
        "name": "Aula / Palestra",
        "description": "Resumo didático, conceitos-chave e exemplos",
        "icon": "📚",
        "editable": False,
        "persona": "Você é um assistente especialista em criar resumos didáticos de aulas e palestras em português do Brasil.",
        "instructions": (
            "Crie um resumo didático. Omita seções que não se aplicarem.\n\n"
            "1. Título e tema\n"
            "2. \"📖 Contexto e Objetivo\"\n"
            "3. \"🔑 Conceitos-Chave\" — definições dos termos principais\n"
            "4. \"📝 Conteúdo\" — tópicos organizados por assunto\n"
            "5. \"💡 Exemplos Citados\"\n"
            "6. \"📌 Pontos para Revisar\""
        ),
    },
    {
        "id": "juridico",
        "name": "Jurídico / Ata",
        "description": "Linguagem formal, partes envolvidas e deliberações",
        "icon": "⚖️",
        "editable": False,
        "persona": "Você é um assistente especialista em redigir atas formais e documentos jurídicos em português do Brasil.",
        "instructions": (
            "Crie uma ata estruturada:\n\n"
            "1. \"ATA DE REUNIÃO\" como título\n"
            "2. Data, local e participantes\n"
            "3. \"PAUTA\" — assuntos tratados, numerados\n"
            "4. \"DELIBERAÇÕES\" — decisões com precisão\n"
            "5. \"ENCERRAMENTO\"\n\n"
            "Use linguagem formal e impessoal. Sem emojis. "
            "Informações não identificadas: marque como [não identificado]."
        ),
    },
    {
        "id": "medico",
        "name": "Consulta Médica",
        "description": "Queixa, histórico, conduta e orientações",
        "icon": "🏥",
        "editable": False,
        "persona": "Você é um assistente especialista em organizar registros de consultas médicas em português do Brasil.",
        "instructions": (
            "Organize as informações. Omita seções não mencionadas.\n\n"
            "1. \"👤 Identificação\"\n"
            "2. \"🩺 Queixa Principal\"\n"
            "3. \"📋 Histórico Relevante\"\n"
            "4. \"🔍 Avaliação e Diagnóstico\"\n"
            "5. \"💊 Conduta\" — medicamentos, exames\n"
            "6. \"📌 Orientações ao Paciente\"\n\n"
            "Mantenha linguagem técnica precisa."
        ),
    },
    {
        "id": "personalizado",
        "name": "Personalizado",
        "description": "Defina seu próprio perfil de agente",
        "icon": "✏️",
        "editable": True,
        "persona": "Você é um assistente especialista em processar transcrições em português do Brasil.",
        "instructions": "Analise a transcrição e crie um resumo organizado conforme as necessidades do projeto.",
    },
]

BUILT_IN_IDS = {p["id"] for p in BUILT_IN_PROFILES}

# ══════════════════════════════════════════════════════════════════════════════
#  BOOTSTRAP
# ══════════════════════════════════════════════════════════════════════════════

def bootstrap():
    os.makedirs(PROFILES_DIR, exist_ok=True)
    os.makedirs(PROJECTS_DIR, exist_ok=True)
    for p in BUILT_IN_PROFILES:
        path = os.path.join(PROFILES_DIR, f"{p['id']}.json")
        if not os.path.exists(path):
            _write_json(path, p)

# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def _write_json(path: str, data) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def _read_json(path: str, default=None):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return default

def _slugify(name: str) -> str:
    name = name.lower().strip()
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[-\s]+", "-", name)
    return name or "projeto"

# ══════════════════════════════════════════════════════════════════════════════
#  PROFILE MANAGER
# ══════════════════════════════════════════════════════════════════════════════

def load_all_profiles() -> list:
    profiles = []
    for fn in os.listdir(PROFILES_DIR):
        if fn.endswith(".json"):
            p = _read_json(os.path.join(PROFILES_DIR, fn))
            if p:
                profiles.append(p)
    built_in_order = [p["id"] for p in BUILT_IN_PROFILES]
    def _key(p):
        pid = p["id"]
        return (0, built_in_order.index(pid)) if pid in built_in_order else (1, p.get("name", ""))
    return sorted(profiles, key=_key)

def load_profile(profile_id: str) -> Optional[dict]:
    return _read_json(os.path.join(PROFILES_DIR, f"{profile_id}.json"))

def save_custom_profile(profile_id: Optional[str], name: str, description: str,
                         persona: str, instructions: str) -> dict:
    if not profile_id:
        slug = _slugify(name)
        if slug in BUILT_IN_IDS:
            slug = f"custom-{slug}"
        base, n = slug, 1
        while os.path.exists(os.path.join(PROFILES_DIR, f"{slug}.json")) and slug not in BUILT_IN_IDS:
            slug = f"{base}-{n}"; n += 1
        profile_id = slug
    p = _read_json(os.path.join(PROFILES_DIR, f"{profile_id}.json")) or {}
    p.update({
        "id": profile_id, "name": name, "description": description,
        "icon": p.get("icon", "🔧"), "editable": True,
        "persona": persona, "instructions": instructions,
    })
    _write_json(os.path.join(PROFILES_DIR, f"{profile_id}.json"), p)
    return p

def delete_custom_profile(profile_id: str) -> bool:
    if profile_id in BUILT_IN_IDS:
        return False
    path = os.path.join(PROFILES_DIR, f"{profile_id}.json")
    if os.path.exists(path):
        os.remove(path)
        return True
    return False

# ══════════════════════════════════════════════════════════════════════════════
#  PROJECT MANAGER
# ══════════════════════════════════════════════════════════════════════════════

def list_projects() -> list:
    result = []
    if not os.path.exists(PROJECTS_DIR):
        return result
    for entry in os.scandir(PROJECTS_DIR):
        if entry.is_dir():
            p = _read_json(os.path.join(entry.path, "project.json"))
            if p:
                result.append(p)
    return sorted(result, key=lambda p: p.get("updated_at", ""), reverse=True)

def load_project(project_id: str) -> Optional[dict]:
    return _read_json(os.path.join(PROJECTS_DIR, project_id, "project.json"))

def save_project(project: dict) -> None:
    pdir = os.path.join(PROJECTS_DIR, project["id"])
    os.makedirs(os.path.join(pdir, "tasks"), exist_ok=True)
    _write_json(os.path.join(pdir, "project.json"), project)

def create_project(name: str) -> dict:
    pid = _slugify(name)
    base, n = pid, 1
    while os.path.exists(os.path.join(PROJECTS_DIR, pid)):
        pid = f"{base}-{n}"; n += 1
    now = datetime.now().isoformat()
    project = {
        "id": pid, "name": name, "context": "",
        "agent_profile_id": "reuniao",
        "created_at": now, "updated_at": now, "task_count": 0,
    }
    save_project(project)
    return project

def update_project(project_id: str, **kwargs) -> dict:
    p = load_project(project_id) or {}
    p.update(kwargs)
    p["updated_at"] = datetime.now().isoformat()
    save_project(p)
    return p

def load_corrections(project_id: str) -> list:
    return _read_json(os.path.join(PROJECTS_DIR, project_id, "corrections.json"), [])

def append_corrections(project_id: str, new_corrections: list) -> None:
    if not new_corrections:
        return
    path = os.path.join(PROJECTS_DIR, project_id, "corrections.json")
    existing = load_corrections(project_id)
    existing.extend(new_corrections)
    _write_json(path, existing)

def save_task(project_id: str, task: dict) -> None:
    tdir = os.path.join(PROJECTS_DIR, project_id, "tasks")
    os.makedirs(tdir, exist_ok=True)
    _write_json(os.path.join(tdir, f"{task['id']}.json"), task)

def update_task(project_id: str, task_id: str, **kwargs) -> None:
    path = os.path.join(PROJECTS_DIR, project_id, "tasks", f"{task_id}.json")
    task = _read_json(path, {})
    task.update(kwargs)
    _write_json(path, task)

# ══════════════════════════════════════════════════════════════════════════════
#  CORE PROCESSING
# ══════════════════════════════════════════════════════════════════════════════

def transcrever_audio(audio_path: str, modelo_whisper, log) -> Optional[str]:
    log(f"🎙️  Transcrevendo: {os.path.basename(audio_path)}...")
    try:
        result = modelo_whisper.transcribe(audio_path, language="pt")
        texto = (result.get("text") or "").strip()
        if texto:
            log("✅  Transcrição concluída.")
            return texto
        log("⚠️  Whisper não retornou texto.")
        return None
    except Exception as e:
        log(f"❌  Erro na transcrição: {e}")
        return None


def build_prompt(profile: dict, transcricao: str, contexto: str, corrections: list) -> str:
    parts = [profile.get("persona", ""), ""]
    parts.append(
        "IMPORTANTE: Esta transcrição foi gerada automaticamente pelo Whisper e pode conter "
        "erros, palavras trocadas ou alucinações. Interprete o texto com senso crítico e "
        "corrija erros óbvios usando o contexto fornecido."
    )
    if corrections:
        recent = corrections[-MAX_CORRECTIONS_IN_PROMPT:]
        examples = "\n".join(f'  • "{c["original"]}" → "{c["corrected"]}"' for c in recent)
        parts.append(f"\nCorreções registradas para este projeto (aplique ao encontrar os mesmos termos):\n{examples}")
    if contexto.strip():
        parts.append(f"\nContexto do projeto:\n{contexto.strip()}")
    parts.append(f"\n{profile.get('instructions', '')}")
    parts.append(f"\nTRANSCRIÇÃO:\n\"\"\"{transcricao}\"\"\"")
    parts.append("\nRESULTADO:")
    return "\n".join(parts)


def gerar_resultado(transcricao: str, profile: dict, contexto: str,
                     corrections: list, ollama_model: str, log) -> Optional[str]:
    log(f"🧠  Processando com {ollama_model}  |  Perfil: {profile.get('name', '?')}")
    try:
        prompt = build_prompt(profile, transcricao, contexto, corrections)
        resp = requests.post(
            OLLAMA_URL,
            json={"model": ollama_model, "prompt": prompt, "stream": False},
            timeout=300,
        )
        resp.raise_for_status()
        resultado = resp.json().get("response", "").strip()
        if resultado:
            log("✅  Resultado gerado.")
            return resultado
        log("⚠️  Ollama retornou resposta vazia.")
        return None
    except requests.ConnectionError:
        log("❌  Ollama não está rodando. Execute: ollama serve")
        return None
    except Exception as e:
        log(f"❌  Erro ao gerar resultado: {e}")
        return None

# ══════════════════════════════════════════════════════════════════════════════
#  CORRECTION DIFF
# ══════════════════════════════════════════════════════════════════════════════

def extract_corrections(original: str, corrected: str) -> list:
    orig_words = original.split()
    corr_words = corrected.split()
    matcher = difflib.SequenceMatcher(None, orig_words, corr_words, autojunk=False)
    result = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "replace":
            o = " ".join(orig_words[i1:i2])
            c = " ".join(corr_words[j1:j2])
            if o.lower() != c.lower():
                result.append({"original": o, "corrected": c,
                                "timestamp": datetime.now().isoformat()})
    return result

# ══════════════════════════════════════════════════════════════════════════════
#  PDF EXPORT
# ══════════════════════════════════════════════════════════════════════════════

def exportar_pdf(conteudo: str, transcricao: str, caminho: str,
                  project_name: str, profile_name: str, log) -> bool:
    log(f"📄  Salvando PDF: {os.path.basename(caminho)}...")
    try:
        doc = SimpleDocTemplate(
            caminho, pagesize=A4,
            leftMargin=2.2*cm, rightMargin=2.2*cm,
            topMargin=2*cm, bottomMargin=2*cm,
        )
        styles = getSampleStyleSheet()
        s_title  = ParagraphStyle("t",  parent=styles["Title"],   fontSize=18, spaceAfter=4)
        s_meta   = ParagraphStyle("m",  parent=styles["Normal"],  fontSize=9,  textColor=colors.grey, spaceAfter=14)
        s_sec    = ParagraphStyle("s",  parent=styles["Heading2"], fontSize=12, spaceBefore=14, spaceAfter=4, textColor=colors.Color(0.48, 0.18, 0.75))
        s_body   = ParagraphStyle("b",  parent=styles["Normal"],  fontSize=10, leading=15, spaceAfter=4)
        s_small  = ParagraphStyle("sm", parent=styles["Normal"],  fontSize=8,  leading=12, textColor=colors.Color(0.35, 0.35, 0.35))

        def safe(text):
            return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        story = []
        story.append(Paragraph("Escriba", s_title))
        story.append(Paragraph(
            f"Projeto: {safe(project_name)}  •  Perfil: {safe(profile_name)}  •  "
            f"{datetime.now().strftime('%d/%m/%Y %H:%M')}",
            s_meta
        ))
        story.append(HRFlowable(width="100%", thickness=1.2,
                                 color=colors.Color(0.48, 0.18, 0.75)))
        story.append(Spacer(1, 0.4*cm))
        story.append(Paragraph("Resultado", s_sec))
        for line in conteudo.splitlines():
            line = line.strip()
            if not line:
                story.append(Spacer(1, 0.15*cm))
            else:
                story.append(Paragraph(safe(line), s_body))
        story.append(Spacer(1, 0.5*cm))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey))
        story.append(Spacer(1, 0.3*cm))
        story.append(Paragraph("Transcrição Original (gerada pelo Whisper)", s_sec))
        story.append(Paragraph(
            "<font color='grey'>A transcrição pode conter erros de reconhecimento de fala.</font>",
            s_small
        ))
        story.append(Spacer(1, 0.2*cm))
        for line in transcricao.splitlines():
            line = line.strip()
            if line:
                story.append(Paragraph(safe(line), s_small))
        doc.build(story)
        log("✅  PDF salvo.")
        return True
    except Exception as e:
        log(f"❌  Erro ao salvar PDF: {e}")
        return False

# ══════════════════════════════════════════════════════════════════════════════
#  GUI
# ══════════════════════════════════════════════════════════════════════════════

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

WIN_W, WIN_H = 780, 720
WIN_MIN_W, WIN_MIN_H = 780, 680


class EscribaApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Escriba")
        self.geometry(f"{WIN_W}x{WIN_H}")
        self.minsize(WIN_MIN_W, WIN_MIN_H)
        self.resizable(True, True)
        self.current_project: Optional[dict] = None
        self._task_result: Optional[dict] = None

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.place(relx=0, rely=0, relwidth=1, relheight=1)

        self._frames = {
            "projects":   ProjectsFrame(container, self),
            "work":       WorkFrame(container, self),
            "processing": ProcessingFrame(container, self),
            "review":     ReviewFrame(container, self),
        }
        for f in self._frames.values():
            f.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.show_frame("projects")

    def show_frame(self, name: str, **kwargs):
        frame = self._frames[name]
        frame.lift()
        if hasattr(frame, "on_show"):
            frame.on_show(**kwargs)

    def navigate_to_projects(self):
        self.current_project = None
        self._task_result = None
        self.show_frame("projects")

    def navigate_to_work(self, project: dict):
        self.current_project = project
        self.show_frame("work")

    def navigate_to_processing(self, **pipeline_kwargs):
        self.show_frame("processing")
        self._frames["processing"].start_pipeline(**pipeline_kwargs)

    def navigate_to_review(self, result: dict):
        self._task_result = result
        self.show_frame("review")


# ── Projects Frame ────────────────────────────────────────────────────────────

class ProjectsFrame(ctk.CTkFrame):
    def __init__(self, parent, app: EscribaApp):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self._build()

    def on_show(self):
        self._refresh()

    def _build(self):
        ctk.CTkLabel(self, text="ESCRIBA",
                     font=ctk.CTkFont(size=28, weight="bold")).pack(pady=(26, 2))
        ctk.CTkLabel(self,
                     text="Transcrição & Sumarização de Áudios com IA Local  ·  Whisper + Ollama",
                     font=ctk.CTkFont(size=13), text_color="gray").pack(pady=(0, 18))

        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=28, pady=(0, 8))
        ctk.CTkLabel(top, text="Seus Projetos",
                     font=ctk.CTkFont(size=16, weight="bold")).pack(side="left")
        ctk.CTkButton(top, text="+ Novo Projeto", width=150,
                      fg_color=PURPLE, hover_color=PURPLE_HOV,
                      command=self._new_project).pack(side="right")

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=28, pady=(0, 4))

        ctk.CTkLabel(self, text="Escriba v6.0  ·  Forge by Lucas Costa Nogueira",
                     font=ctk.CTkFont(size=10), text_color="gray").pack(pady=(4, 14))

    def _refresh(self):
        for w in self.scroll.winfo_children():
            w.destroy()
        projects = list_projects()
        if not projects:
            ctk.CTkLabel(self.scroll,
                         text="Nenhum projeto ainda.\nClique em '+ Novo Projeto' para começar.",
                         font=ctk.CTkFont(size=13), text_color="gray",
                         justify="center").pack(pady=70)
            return
        for proj in projects:
            self._make_card(proj)

    def _make_card(self, proj: dict):
        card = ctk.CTkFrame(self.scroll, corner_radius=10)
        card.pack(fill="x", pady=5)
        card.columnconfigure(1, weight=1)

        profile = load_profile(proj.get("agent_profile_id", "reuniao"))
        icon = profile.get("icon", "📁") if profile else "📁"
        ctk.CTkLabel(card, text=icon,
                     font=ctk.CTkFont(size=22), width=52).grid(
            row=0, column=0, rowspan=2, padx=(16, 6), pady=12)

        ctk.CTkLabel(card, text=proj["name"],
                     font=ctk.CTkFont(size=14, weight="bold"), anchor="w").grid(
            row=0, column=1, sticky="w", padx=4, pady=(12, 0))

        pname = profile.get("name", "?") if profile else "?"
        count = proj.get("task_count", 0)
        updated = (proj.get("updated_at") or "")[:10]
        ctk.CTkLabel(card,
                     text=f"{pname}  ·  {count} tarefa(s)  ·  {updated}",
                     font=ctk.CTkFont(size=11), text_color="gray", anchor="w").grid(
            row=1, column=1, sticky="w", padx=4, pady=(0, 12))

        ctk.CTkButton(card, text="Abrir →", width=100,
                      fg_color=PURPLE, hover_color=PURPLE_HOV,
                      command=lambda p=proj: self.app.navigate_to_work(p)).grid(
            row=0, column=2, rowspan=2, padx=16)

    def _new_project(self):
        dialog = ctk.CTkInputDialog(text="Nome do novo projeto:", title="Novo Projeto")
        name = dialog.get_input()
        if name and name.strip():
            proj = create_project(name.strip())
            self.app.navigate_to_work(proj)


# ── Work Frame ────────────────────────────────────────────────────────────────

class WorkFrame(ctk.CTkFrame):
    def __init__(self, parent, app: EscribaApp):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self._selected_profile_id = "reuniao"
        self._profile_btns: dict = {}
        self._source_type = "folder"
        self._source_path = ""
        self._build()

    def on_show(self):
        proj = self.app.current_project
        if not proj:
            return
        self.lbl_project.configure(text=proj["name"])
        self.txt_context.delete("1.0", "end")
        if proj.get("context"):
            self.txt_context.insert("1.0", proj["context"])
        self._source_path = ""
        self.entry_source.delete(0, "end")
        self._refresh_profile_grid()
        self._select_profile(proj.get("agent_profile_id", "reuniao"), save=False)

    def _build(self):
        # Top bar
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=24, pady=(18, 0))
        ctk.CTkButton(top, text="← Projetos", width=110,
                      fg_color="transparent", border_width=1, border_color="gray",
                      hover_color=PURPLE_DIM,
                      command=self._back).pack(side="left")
        self.lbl_project = ctk.CTkLabel(top, text="",
                                         font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_project.pack(side="left", padx=14)
        ctk.CTkButton(top, text="⚙  Perfis", width=110,
                      fg_color="transparent", border_width=1, border_color="gray",
                      hover_color=PURPLE_DIM,
                      command=self._open_profiles).pack(side="right")

        # Scrollable content
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=24, pady=(10, 0))

        self._build_profile_section()
        self._build_context_section()
        self._build_source_section()
        self._build_settings_section()

        # Start button (fixed at bottom)
        self.btn_start = ctk.CTkButton(
            self, text="▶   INICIAR",
            height=46, font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=PURPLE, hover_color=PURPLE_HOV,
            command=self._start)
        self.btn_start.pack(padx=24, pady=(10, 16), fill="x")

    def _build_profile_section(self):
        ctk.CTkLabel(self.scroll, text="Perfil do Agente",
                     font=ctk.CTkFont(size=14, weight="bold"), anchor="w").pack(
            fill="x", pady=(8, 6))
        self.profile_grid = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.profile_grid.pack(fill="x")
        self._refresh_profile_grid()

    def _refresh_profile_grid(self):
        for w in self.profile_grid.winfo_children():
            w.destroy()
        self._profile_btns.clear()
        profiles = load_all_profiles()
        cols = 3
        for i, p in enumerate(profiles):
            r, c = divmod(i, cols)
            btn = ctk.CTkButton(
                self.profile_grid,
                text=f"{p['icon']}  {p['name']}",
                height=54, corner_radius=8,
                fg_color=CARD_BG, hover_color=PURPLE_DIM,
                font=ctk.CTkFont(size=12),
                command=lambda pid=p["id"]: self._select_profile(pid))
            btn.grid(row=r, column=c, padx=4, pady=4, sticky="ew")
            self._profile_btns[p["id"]] = btn
        for c in range(cols):
            self.profile_grid.columnconfigure(c, weight=1)
        if self._selected_profile_id in self._profile_btns:
            self._highlight(self._selected_profile_id)

    def _select_profile(self, pid: str, save: bool = True):
        self._selected_profile_id = pid
        self._highlight(pid)
        if save and self.app.current_project:
            self.app.current_project = update_project(
                self.app.current_project["id"], agent_profile_id=pid)

    def _highlight(self, pid: str):
        for k, btn in self._profile_btns.items():
            btn.configure(fg_color=PURPLE if k == pid else CARD_BG)

    def _build_context_section(self):
        ctk.CTkLabel(self.scroll, text="Contexto do Projeto",
                     font=ctk.CTkFont(size=14, weight="bold"), anchor="w").pack(
            fill="x", pady=(18, 4))
        ctk.CTkLabel(
            self.scroll,
            text="Informe nomes, siglas, termos técnicos e qualquer contexto que ajude "
                 "o agente a interpretar melhor a transcrição.",
            font=ctk.CTkFont(size=11), text_color="gray",
            wraplength=700, justify="left", anchor="w").pack(fill="x", pady=(0, 6))
        self.txt_context = ctk.CTkTextbox(
            self.scroll, height=90, font=ctk.CTkFont(size=12))
        self.txt_context.pack(fill="x")

    def _build_source_section(self):
        ctk.CTkLabel(self.scroll, text="Arquivo de Áudio",
                     font=ctk.CTkFont(size=14, weight="bold"), anchor="w").pack(
            fill="x", pady=(18, 4))
        ctk.CTkLabel(
            self.scroll,
            text="💡 Para múltiplos arquivos em ordem, nomeie-os numericamente: "
                 "Reunião 1, Reunião 2, Reunião 3...",
            font=ctk.CTkFont(size=11), text_color="gray", anchor="w").pack(
            fill="x", pady=(0, 6))

        row = ctk.CTkFrame(self.scroll, fg_color="transparent")
        row.pack(fill="x")
        ctk.CTkButton(row, text="📄 Arquivo", width=110, height=34,
                      fg_color=CARD_BG, hover_color=PURPLE_DIM,
                      command=self._browse_file).pack(side="left", padx=(0, 6))
        ctk.CTkButton(row, text="📂 Pasta", width=110, height=34,
                      fg_color=CARD_BG, hover_color=PURPLE_DIM,
                      command=self._browse_folder).pack(side="left", padx=(0, 8))
        self.entry_source = ctk.CTkEntry(
            row, placeholder_text="Selecione um arquivo ou pasta de áudio...")
        self.entry_source.pack(side="left", fill="x", expand=True)

    def _browse_file(self):
        exts = " ".join(f"*{e}" for e in sorted(AUDIO_EXTENSIONS))
        path = filedialog.askopenfilename(
            filetypes=[("Áudio", exts), ("Todos", "*.*")])
        if path:
            self._source_type = "file"
            self._source_path = path
            self.entry_source.delete(0, "end")
            self.entry_source.insert(0, path)

    def _browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self._source_type = "folder"
            self._source_path = path
            self.entry_source.delete(0, "end")
            self.entry_source.insert(0, path)

    def _build_settings_section(self):
        ctk.CTkLabel(self.scroll, text="Configurações",
                     font=ctk.CTkFont(size=14, weight="bold"), anchor="w").pack(
            fill="x", pady=(18, 8))
        row = ctk.CTkFrame(self.scroll, fg_color="transparent")
        row.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(row, text="Modelo Ollama:", width=130, anchor="w").pack(side="left")
        self.combo_ollama = ctk.CTkComboBox(
            row, values=OLLAMA_MODELS, width=190,
            button_color=PURPLE, button_hover_color=PURPLE_HOV)
        self.combo_ollama.set("llama3.2")
        self.combo_ollama.pack(side="left", padx=(0, 28))

        ctk.CTkLabel(row, text="Modelo Whisper:", width=130, anchor="w").pack(side="left")
        self.combo_whisper = ctk.CTkComboBox(
            row, values=WHISPER_MODELS, width=190,
            button_color=PURPLE, button_hover_color=PURPLE_HOV)
        self.combo_whisper.set("base")
        self.combo_whisper.pack(side="left")

    def _back(self):
        self._save_context()
        self.app.navigate_to_projects()

    def _save_context(self):
        if self.app.current_project:
            ctx = self.txt_context.get("1.0", "end").strip()
            self.app.current_project = update_project(
                self.app.current_project["id"], context=ctx)

    def _start(self):
        if not self._source_path:
            messagebox.showwarning("Atenção", "Selecione um arquivo ou pasta de áudio.")
            return
        if not self.app.current_project:
            return
        self._save_context()
        self.app.navigate_to_processing(
            project=self.app.current_project,
            source_type=self._source_type,
            source_path=self._source_path,
            ollama_model=self.combo_ollama.get(),
            whisper_model=self.combo_whisper.get(),
        )

    def _open_profiles(self):
        ProfilesModal(self.app, on_close=self._refresh_profile_grid)


# ── Processing Frame ──────────────────────────────────────────────────────────

class ProcessingFrame(ctk.CTkFrame):
    def __init__(self, parent, app: EscribaApp):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self._result: Optional[dict] = None
        self._build()

    def _build(self):
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=24, pady=(20, 0))
        self.lbl_title = ctk.CTkLabel(top, text="Processando...",
                                       font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_title.pack(side="left")

        self.progressbar = ctk.CTkProgressBar(
            self, mode="indeterminate", progress_color=PURPLE)
        self.progressbar.pack(padx=24, pady=(14, 4), fill="x")
        self.progressbar.stop()

        self.lbl_status = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=11), text_color="gray")
        self.lbl_status.pack(pady=(0, 6))

        ctk.CTkLabel(self, text="Log de execução:",
                     anchor="w", font=ctk.CTkFont(size=12)).pack(padx=24, anchor="w")
        self.log_box = ctk.CTkTextbox(
            self, font=ctk.CTkFont(family="Courier New", size=11))
        self.log_box.pack(padx=24, pady=(4, 6), fill="both", expand=True)
        self.log_box.configure(state="disabled")

        self.completion = ctk.CTkFrame(self, fg_color="transparent")
        self.completion.pack(padx=24, pady=(4, 16), fill="x")

    def start_pipeline(self, project, source_type, source_path,
                       ollama_model, whisper_model):
        self._result = None
        self.lbl_title.configure(text=f"⏳  {project['name']}")
        self.lbl_status.configure(text="")
        for w in self.completion.winfo_children():
            w.destroy()
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")
        self.progressbar.start()
        threading.Thread(
            target=self._run,
            args=(project, source_type, source_path, ollama_model, whisper_model),
            daemon=True,
        ).start()

    def _log(self, msg: str):
        self.after(0, self._log_safe, msg)

    def _log_safe(self, msg: str):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", msg + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")
        self.lbl_status.configure(text=(msg[:88] + "…") if len(msg) > 88 else msg)

    def _run(self, project, source_type, source_path, ollama_model, whisper_model):
        try:
            self._log("🛡️  Pipeline iniciado")
            self._log(f"📁  Fonte: {source_path}")
            self._log("─" * 52)

            # Collect audio files
            if source_type == "file":
                ext = os.path.splitext(source_path)[1].lower()
                if ext not in AUDIO_EXTENSIONS:
                    self._log(f"❌  Formato não suportado: {ext}")
                    return
                files = [(os.path.dirname(source_path), os.path.basename(source_path))]
                out_dir = os.path.dirname(source_path)
            else:
                names = sorted(
                    f for f in os.listdir(source_path)
                    if os.path.splitext(f)[1].lower() in AUDIO_EXTENSIONS
                )
                if not names:
                    self._log("⚠️  Nenhum arquivo de áudio encontrado na pasta.")
                    return
                files = [(source_path, n) for n in names]
                out_dir = source_path

            self._log(f"🔍  {len(files)} arquivo(s) encontrado(s).")

            # Load Whisper once
            self._log(f"📦  Carregando Whisper '{whisper_model}'...")
            try:
                modelo = whisper.load_model(whisper_model)
                self._log("✅  Whisper carregado.")
            except Exception as e:
                self._log(f"❌  Falha ao carregar Whisper: {e}")
                return

            profile = load_profile(project.get("agent_profile_id", "reuniao"))
            if not profile:
                profile = BUILT_IN_PROFILES[0]
            corrections = load_corrections(project["id"])
            contexto = project.get("context", "")

            self._log("─" * 52)
            all_trans, all_results = [], []

            for i, (folder, fname) in enumerate(files, 1):
                self._log(f"\n[{i}/{len(files)}]  {fname}")
                trans = transcrever_audio(os.path.join(folder, fname), modelo, self._log)
                if not trans:
                    self._log("⚠️  Sem transcrição. Pulando.")
                    continue
                all_trans.append(f"=== {fname} ===\n{trans}")
                res = gerar_resultado(trans, profile, contexto, corrections,
                                       ollama_model, self._log)
                if not res:
                    res = ("⚠️ Resultado não gerado — Ollama indisponível.\n\n"
                           "Transcrição incluída abaixo.")
                all_results.append(f"=== {fname} ===\n{res}")

            if not all_results:
                self._log("\n❌  Nenhum arquivo processado com sucesso.")
                return

            final_trans  = "\n\n".join(all_trans)
            final_result = "\n\n".join(all_results)

            task_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            task = {
                "id": task_id,
                "created_at": datetime.now().isoformat(),
                "source_files": [f for _, f in files],
                "raw_transcription": final_trans,
                "agent_output": final_result,
                "final_output": None,
                "was_reviewed": False,
            }
            save_task(project["id"], task)
            update_project(project["id"],
                           task_count=project.get("task_count", 0) + 1)

            self._result = {
                "task_id":      task_id,
                "project_id":   project["id"],
                "project_name": project["name"],
                "profile_name": profile.get("name", "?"),
                "agent_output": final_result,
                "transcription": final_trans,
                "out_dir":      out_dir,
            }

            self._log("\n" + "═" * 52)
            self._log(f"✅  Concluído! {len(all_results)}/{len(files)} arquivo(s) processado(s).")
            self._log("═" * 52)

        except Exception as e:
            import traceback
            self._log(f"\n❌  ERRO FATAL: {e}")
            self._log(traceback.format_exc())
        finally:
            self.after(0, self._done)

    def _done(self):
        self.progressbar.stop()
        for w in self.completion.winfo_children():
            w.destroy()

        if self._result:
            self.lbl_title.configure(text="✅  Tarefa concluída")
            ctk.CTkLabel(self.completion, text="✅  Resultado pronto!",
                         font=ctk.CTkFont(size=13, weight="bold"),
                         text_color="#4CAF50").pack(side="left", padx=(0, 16))
            ctk.CTkButton(self.completion, text="Finalizar", width=130,
                          fg_color=CARD_BG, hover_color=PURPLE_DIM,
                          command=self._finish).pack(side="left", padx=(0, 8))
            ctk.CTkButton(self.completion, text="Revisar Texto →", width=150,
                          fg_color=PURPLE, hover_color=PURPLE_HOV,
                          command=self._go_review).pack(side="left")
        else:
            self.lbl_title.configure(text="❌  Falha no processamento")
            ctk.CTkButton(self.completion, text="← Voltar aos Projetos",
                          fg_color=PURPLE, hover_color=PURPLE_HOV,
                          command=self.app.navigate_to_projects).pack(side="left")

    def _finish(self):
        r = self._result
        if not r:
            return
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf = os.path.join(r["out_dir"], f"escriba_{ts}.pdf")
        update_task(r["project_id"], r["task_id"],
                    final_output=r["agent_output"], was_reviewed=False)
        ok = exportar_pdf(r["agent_output"], r["transcription"], pdf,
                          r["project_name"], r["profile_name"], self._log)
        if ok:
            messagebox.showinfo("PDF Salvo", f"PDF salvo em:\n{pdf}")
        self.app.navigate_to_projects()

    def _go_review(self):
        if self._result:
            self.app.navigate_to_review(self._result)


# ── Review Frame ──────────────────────────────────────────────────────────────

class ReviewFrame(ctk.CTkFrame):
    def __init__(self, parent, app: EscribaApp):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self._result: Optional[dict] = None
        self._build()

    def on_show(self):
        r = self.app._task_result
        if not r:
            return
        self._result = r
        self.lbl_project.configure(text=r["project_name"])
        self.editor.configure(state="normal")
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", r["agent_output"])

    def _build(self):
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=24, pady=(20, 6))
        ctk.CTkLabel(top, text="✍️  Revisão do Texto",
                     font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")
        self.lbl_project = ctk.CTkLabel(top, text="",
                                          font=ctk.CTkFont(size=13), text_color="gray")
        self.lbl_project.pack(side="left", padx=12)

        ctk.CTkLabel(
            self,
            text="Edite o texto conforme necessário. 'Corrigir e Finalizar' salva as diferenças "
                 "para aprendizado futuro do agente neste projeto.",
            font=ctk.CTkFont(size=11), text_color="gray",
            wraplength=730, justify="left", anchor="w").pack(padx=24, anchor="w", pady=(0, 8))

        self.editor = ctk.CTkTextbox(self, font=ctk.CTkFont(size=12), wrap="word")
        self.editor.pack(padx=24, pady=(0, 8), fill="both", expand=True)

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(padx=24, pady=(0, 16), fill="x")
        ctk.CTkButton(btn_row, text="Finalizar", width=140,
                      fg_color=CARD_BG, hover_color=PURPLE_DIM,
                      command=self._finish).pack(side="left", padx=(0, 10))
        ctk.CTkButton(btn_row, text="✓ Corrigir e Finalizar", width=200,
                      fg_color=PURPLE, hover_color=PURPLE_HOV,
                      command=self._correct_finish).pack(side="left")
        ctk.CTkLabel(btn_row,
                     text="'Finalizar' exporta sem aprendizado  ·  'Corrigir e Finalizar' salva as correções",
                     font=ctk.CTkFont(size=10), text_color="gray").pack(
            side="right")

    def _finish(self):
        self._export(save_corrections=False)

    def _correct_finish(self):
        self._export(save_corrections=True)

    def _export(self, save_corrections: bool):
        r = self._result
        if not r:
            return
        edited = self.editor.get("1.0", "end").strip()

        if save_corrections:
            diffs = extract_corrections(r["agent_output"], edited)
            if diffs:
                append_corrections(r["project_id"], diffs)

        update_task(r["project_id"], r["task_id"],
                    final_output=edited, was_reviewed=True)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf = os.path.join(r["out_dir"], f"escriba_{ts}.pdf")

        msgs = []
        ok = exportar_pdf(edited, r["transcription"], pdf,
                          r["project_name"], r["profile_name"],
                          lambda m: msgs.append(m))
        if ok:
            suffix = " Correções salvas para aprendizado." if save_corrections and diffs else ""
            messagebox.showinfo("PDF Salvo", f"PDF salvo em:\n{pdf}{suffix}")
        else:
            messagebox.showerror("Erro", "\n".join(msgs))

        self.app.navigate_to_projects()


# ── Profiles Modal ────────────────────────────────────────────────────────────

class ProfilesModal(ctk.CTkToplevel):
    def __init__(self, parent, on_close=None):
        super().__init__(parent)
        self.title("Gerenciar Perfis")
        self.geometry("720x560")
        self.resizable(False, False)
        self._on_close = on_close
        self._editing_id: Optional[str] = None
        self.protocol("WM_DELETE_WINDOW", self._close)
        self._build()
        self._refresh_list()

    def _close(self):
        if self._on_close:
            self._on_close()
        self.destroy()

    def _build(self):
        # Left: list panel
        left = ctk.CTkFrame(self, width=200, corner_radius=0)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        ctk.CTkLabel(left, text="Perfis",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(14, 8))
        self.list_frame = ctk.CTkScrollableFrame(left, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True, padx=8)
        ctk.CTkButton(left, text="+ Novo Perfil",
                      fg_color=PURPLE, hover_color=PURPLE_HOV,
                      command=self._new_profile).pack(pady=12, padx=12, fill="x")

        # Right: editor panel
        right = ctk.CTkFrame(self, fg_color="transparent")
        right.pack(side="left", fill="both", expand=True, padx=14, pady=14)

        ctk.CTkLabel(right, text="Detalhes do Perfil",
                     font=ctk.CTkFont(size=14, weight="bold"), anchor="w").pack(
            fill="x", pady=(0, 10))

        ctk.CTkLabel(right, text="Nome:", anchor="w").pack(fill="x")
        self.e_name = ctk.CTkEntry(right, placeholder_text="Nome do perfil")
        self.e_name.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(right, text="Descrição:", anchor="w").pack(fill="x")
        self.e_desc = ctk.CTkEntry(right, placeholder_text="Breve descrição")
        self.e_desc.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(right, text="Persona — quem o agente é:", anchor="w").pack(fill="x")
        self.t_persona = ctk.CTkTextbox(right, height=72, font=ctk.CTkFont(size=12))
        self.t_persona.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(right, text="Instruções — o que o agente deve fazer:", anchor="w").pack(fill="x")
        self.t_instruct = ctk.CTkTextbox(right, height=110, font=ctk.CTkFont(size=12))
        self.t_instruct.pack(fill="both", expand=True, pady=(0, 10))

        btn_row = ctk.CTkFrame(right, fg_color="transparent")
        btn_row.pack(fill="x")
        self.btn_save = ctk.CTkButton(btn_row, text="💾 Salvar", width=120,
                                       fg_color=PURPLE, hover_color=PURPLE_HOV,
                                       command=self._save, state="disabled")
        self.btn_save.pack(side="left", padx=(0, 8))
        self.btn_del = ctk.CTkButton(btn_row, text="🗑 Excluir", width=120,
                                      fg_color="#8B0000", hover_color="#A00000",
                                      command=self._delete, state="disabled")
        self.btn_del.pack(side="left")
        self.lbl_ro = ctk.CTkLabel(btn_row, text="Perfil padrão — somente leitura",
                                    font=ctk.CTkFont(size=11), text_color="gray")

    def _refresh_list(self, selected: Optional[str] = None):
        for w in self.list_frame.winfo_children():
            w.destroy()
        for p in load_all_profiles():
            ctk.CTkButton(
                self.list_frame,
                text=f"{p['icon']} {p['name']}",
                fg_color=PURPLE if p["id"] == selected else CARD_BG,
                hover_color=PURPLE_DIM, anchor="w", height=34,
                command=lambda prof=p: self._load(prof),
            ).pack(fill="x", pady=2)

    def _load(self, profile: dict):
        self._editing_id = profile["id"]
        editable = profile.get("editable", False)

        for widget, val in [
            (self.e_name,    profile.get("name", "")),
            (self.e_desc,    profile.get("description", "")),
        ]:
            widget.configure(state="normal")
            widget.delete(0, "end")
            widget.insert(0, val)

        for widget, val in [
            (self.t_persona,  profile.get("persona", "")),
            (self.t_instruct, profile.get("instructions", "")),
        ]:
            widget.configure(state="normal")
            widget.delete("1.0", "end")
            widget.insert("1.0", val)

        if editable:
            self.btn_save.configure(state="normal")
            # Delete only for non-built-in profiles
            self.btn_del.configure(
                state="normal" if profile["id"] not in BUILT_IN_IDS else "disabled")
            self.lbl_ro.pack_forget()
        else:
            for w in (self.e_name, self.e_desc, self.t_persona, self.t_instruct):
                w.configure(state="disabled")
            self.btn_save.configure(state="disabled")
            self.btn_del.configure(state="disabled")
            self.lbl_ro.pack(side="left", padx=(8, 0))

        self._refresh_list(selected=profile["id"])

    def _new_profile(self):
        self._editing_id = None
        for w in (self.e_name, self.e_desc):
            w.configure(state="normal")
            w.delete(0, "end")
        for w in (self.t_persona, self.t_instruct):
            w.configure(state="normal")
            w.delete("1.0", "end")
        self.btn_save.configure(state="normal")
        self.btn_del.configure(state="disabled")
        self.lbl_ro.pack_forget()

    def _save(self):
        name = self.e_name.get().strip()
        if not name:
            messagebox.showwarning("Atenção", "Informe um nome.", parent=self)
            return
        desc     = self.e_desc.get().strip()
        persona  = self.t_persona.get("1.0", "end").strip()
        instruct = self.t_instruct.get("1.0", "end").strip()
        p = save_custom_profile(self._editing_id, name, desc, persona, instruct)
        self._editing_id = p["id"]
        self._refresh_list(selected=p["id"])
        messagebox.showinfo("Salvo", "Perfil salvo.", parent=self)

    def _delete(self):
        if not self._editing_id:
            return
        if not messagebox.askyesno("Confirmar", "Excluir este perfil?", parent=self):
            return
        if delete_custom_profile(self._editing_id):
            self._editing_id = None
            for w in (self.e_name, self.e_desc):
                w.delete(0, "end")
            for w in (self.t_persona, self.t_instruct):
                w.delete("1.0", "end")
            self.btn_save.configure(state="disabled")
            self.btn_del.configure(state="disabled")
            self._refresh_list()


# ══════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    bootstrap()
    app = EscribaApp()
    app.mainloop()
