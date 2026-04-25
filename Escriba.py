import os
import textwrap
import threading
from tkinter import filedialog

import customtkinter as ctk
import whisper
import requests
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# ==============================================================================
#              💜  ESCRIBA v5.0 – TRANSCRIÇÃO & RESUMO LOCAL  💜
#                Pipeline: Whisper (local)  ➜  Ollama (local)  ➜  PDF
#                Forge by: Regia LCN  &  Charlotte
# ==============================================================================

OLLAMA_URL       = "http://localhost:11434/api/generate"
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".ogg", ".flac"}
WHISPER_MODELS   = ["tiny", "base", "small", "medium", "large"]
OLLAMA_MODELS    = ["llama3.2", "llama3", "mistral", "gemma2", "phi4"]

PURPLE     = "#7B2FBE"
PURPLE_HOV = "#9B4FDE"

PROMPT_TEMPLATE = """\
Você é um assistente especialista em resumir reuniões, aulas, talks e podcasts \
em português do Brasil.

Analise a transcrição abaixo e crie um resumo organizado com:
1. Um título geral descritivo.
2. Seção "📋 Visão Geral" (2–5 frases resumindo o contexto).
3. Seção "📌 Pontos Principais" em tópicos com bullet points.
4. Seção "✅ Decisões e Ações" (somente se houver decisões explícitas).
5. Seção "🎯 Próximos Passos" (somente se houver tarefas futuras mencionadas).

Regras:
- Escreva sempre em português do Brasil.
- Seja direto, organizado e profissional, com tom leve.
- Use emojis discretos apenas para organizar seções.
- NUNCA invente informações que não estão na transcrição.
- Se uma seção não se aplicar, omita-a completamente.

TRANSCRIÇÃO:
\"\"\"{transcricao}\"\"\"

RESUMO:"""


# ── Core processing ────────────────────────────────────────────────────────────

def transcrever_audio(audio_path: str, modelo_whisper, log) -> str | None:
    log(f"🎙️   Transcrevendo: {os.path.basename(audio_path)}...")
    try:
        result = modelo_whisper.transcribe(audio_path, language="pt")
        texto = (result.get("text") or "").strip()
        if texto:
            log("✅   Transcrição concluída.")
            return texto
        log("⚠️   Whisper não retornou texto.")
        return None
    except Exception as e:
        log(f"❌   Erro na transcrição: {e}")
        return None


def gerar_resumo(transcricao: str, ollama_model: str, log) -> str | None:
    log(f"🧠   Gerando resumo com {ollama_model} (Ollama local)...")
    try:
        resp = requests.post(
            OLLAMA_URL,
            json={
                "model": ollama_model,
                "prompt": PROMPT_TEMPLATE.format(transcricao=transcricao),
                "stream": False,
            },
            timeout=300,
        )
        resp.raise_for_status()
        resumo = resp.json().get("response", "").strip()
        if resumo:
            log("✅   Resumo gerado.")
            return resumo
        log("⚠️   Ollama retornou resposta vazia.")
        return None
    except requests.ConnectionError:
        log("❌   Ollama não está rodando. Execute: ollama serve")
        return None
    except Exception as e:
        log(f"❌   Erro ao gerar resumo: {e}")
        return None


def exportar_pdf(conteudo: str, caminho: str, log) -> None:
    log(f"📄   Salvando PDF: {os.path.basename(caminho)}...")
    try:
        c = canvas.Canvas(caminho, pagesize=A4)
        _, height = A4
        y = height - 50
        wrapper = textwrap.TextWrapper(width=95)
        for linha in conteudo.splitlines():
            for sub in wrapper.wrap(linha) or [""]:
                if y <= 50:
                    c.showPage()
                    y = height - 50
                c.drawString(50, y, sub)
                y -= 14
        c.save()
        log("✅   PDF salvo.")
    except Exception as e:
        log(f"❌   Erro ao salvar PDF: {e}")


# ── GUI ────────────────────────────────────────────────────────────────────────

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class EscribaApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Escriba v5.0")
        self.geometry("720x640")
        self.resizable(False, False)
        self._running = False
        self._build_ui()

    # ── Layout ─────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # Header
        ctk.CTkLabel(
            self, text="💜  ESCRIBA  v5.0",
            font=ctk.CTkFont(size=24, weight="bold"),
        ).pack(pady=(22, 2))
        ctk.CTkLabel(
            self,
            text="Transcrição & Resumo de Áudios com IA Local  ·  Whisper + Ollama",
            font=ctk.CTkFont(size=13),
            text_color="gray",
        ).pack(pady=(0, 18))

        # Config frame
        cfg = ctk.CTkFrame(self)
        cfg.pack(padx=24, fill="x")
        cfg.columnconfigure(1, weight=1)

        ctk.CTkLabel(cfg, text="Pasta de entrada:", anchor="w").grid(
            row=0, column=0, padx=14, pady=10, sticky="w"
        )
        self.entry_folder = ctk.CTkEntry(
            cfg, placeholder_text="Selecione a pasta com os arquivos de áudio..."
        )
        self.entry_folder.grid(row=0, column=1, padx=8, pady=10, sticky="ew")
        ctk.CTkButton(
            cfg, text="📂", width=42,
            fg_color=PURPLE, hover_color=PURPLE_HOV,
            command=self._browse_folder,
        ).grid(row=0, column=2, padx=(0, 14), pady=10)

        ctk.CTkLabel(cfg, text="Modelo Ollama:", anchor="w").grid(
            row=1, column=0, padx=14, pady=10, sticky="w"
        )
        self.combo_ollama = ctk.CTkComboBox(
            cfg, values=OLLAMA_MODELS, width=220,
            button_color=PURPLE, button_hover_color=PURPLE_HOV,
        )
        self.combo_ollama.set("llama3.2")
        self.combo_ollama.grid(row=1, column=1, padx=8, pady=10, sticky="w")

        ctk.CTkLabel(cfg, text="Modelo Whisper:", anchor="w").grid(
            row=2, column=0, padx=14, pady=10, sticky="w"
        )
        self.combo_whisper = ctk.CTkComboBox(
            cfg, values=WHISPER_MODELS, width=220,
            button_color=PURPLE, button_hover_color=PURPLE_HOV,
        )
        self.combo_whisper.set("base")
        self.combo_whisper.grid(row=2, column=1, padx=8, pady=10, sticky="w")

        # Botão principal
        self.btn_start = ctk.CTkButton(
            self, text="▶   INICIAR TRANSCRIÇÃO",
            height=44, font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=PURPLE, hover_color=PURPLE_HOV,
            command=self._start,
        )
        self.btn_start.pack(padx=24, pady=(16, 10), fill="x")

        # Barra de progresso
        self.progressbar = ctk.CTkProgressBar(
            self, mode="indeterminate", progress_color=PURPLE
        )
        self.progressbar.pack(padx=24, fill="x")
        self.progressbar.stop()

        # Status
        self.lbl_status = ctk.CTkLabel(
            self, text="Aguardando...",
            font=ctk.CTkFont(size=12), text_color="gray",
        )
        self.lbl_status.pack(pady=(6, 2))

        # Log
        ctk.CTkLabel(
            self, text="Log de execução:",
            anchor="w", font=ctk.CTkFont(size=12),
        ).pack(padx=24, anchor="w")
        self.log_box = ctk.CTkTextbox(
            self, height=200,
            font=ctk.CTkFont(family="Courier New", size=12),
        )
        self.log_box.pack(padx=24, pady=(4, 6), fill="both", expand=True)
        self.log_box.configure(state="disabled")

        # Footer
        ctk.CTkLabel(
            self,
            text="Forge by Regia LCN & Charlotte",
            font=ctk.CTkFont(size=10), text_color="gray",
        ).pack(pady=(2, 12))

    # ── Helpers ────────────────────────────────────────────────────────────────

    def _browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.entry_folder.delete(0, "end")
            self.entry_folder.insert(0, path)

    def _log(self, msg: str):
        # Pode ser chamado de qualquer thread
        self.after(0, self._log_safe, msg)

    def _log_safe(self, msg: str):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", msg + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")
        curto = msg[:82] + ("…" if len(msg) > 82 else "")
        self.lbl_status.configure(text=curto)

    def _start(self):
        if self._running:
            return

        folder = self.entry_folder.get().strip()
        if not folder or not os.path.isdir(folder):
            self._log_safe("❌   Selecione uma pasta válida antes de iniciar.")
            return

        self._running = True
        self.btn_start.configure(state="disabled", text="⏳  Processando…")
        self.progressbar.start()

        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")

        threading.Thread(
            target=self._pipeline,
            args=(folder, self.combo_ollama.get(), self.combo_whisper.get()),
            daemon=True,
        ).start()

    def _done(self):
        self._running = False
        self.progressbar.stop()
        self.btn_start.configure(state="normal", text="▶   INICIAR TRANSCRIÇÃO")

    # ── Pipeline (thread de fundo) ─────────────────────────────────────────────

    def _pipeline(self, folder: str, ollama_model: str, whisper_model: str):
        try:
            self._log("🛡️   Pipeline iniciado")
            self._log(f"📂   Pasta: {folder}")
            self._log(f"🤖   Ollama → {ollama_model}   |   Whisper → {whisper_model}")
            self._log("─" * 54)

            files = sorted([
                f for f in os.listdir(folder)
                if os.path.splitext(f)[1].lower() in AUDIO_EXTENSIONS
            ])

            if not files:
                self._log("⚠️   Nenhum arquivo de áudio encontrado na pasta.")
                return

            self._log(f"🔍   {len(files)} arquivo(s) encontrado(s).")

            # Carrega Whisper uma única vez para todos os arquivos
            self._log(f"📦   Carregando modelo Whisper '{whisper_model}'...")
            try:
                modelo_whisper = whisper.load_model(whisper_model)
                self._log("✅   Modelo Whisper carregado.")
            except Exception as e:
                self._log(f"❌   Falha ao carregar Whisper: {e}")
                return

            self._log("─" * 54)
            processados = 0

            for i, filename in enumerate(files, 1):
                name, _ = os.path.splitext(filename)
                audio_path = os.path.join(folder, filename)
                pdf_path   = os.path.join(folder, f"{name}.pdf")

                self._log(f"\n[{i}/{len(files)}]  {filename}")

                if os.path.exists(pdf_path):
                    self._log("⏭️   PDF já existe, pulando.")
                    continue

                transcricao = transcrever_audio(audio_path, modelo_whisper, self._log)
                if not transcricao:
                    self._log("⚠️   Sem transcrição. Pulando este arquivo.")
                    continue

                resumo = gerar_resumo(transcricao, ollama_model, self._log)
                if not resumo:
                    resumo = (
                        "⚠️ Resumo não gerado (Ollama indisponível ou sem resposta).\n\n"
                        "Abaixo segue apenas a transcrição completa do áudio."
                    )

                conteudo = (
                    f"Arquivo de origem: {filename}\n"
                    f"{'─' * 80}\n"
                    f"RESUMO ORGANIZADO\n"
                    f"{'─' * 80}\n\n"
                    f"{resumo}\n\n"
                    f"{'─' * 80}\n"
                    f"TRANSCRIÇÃO COMPLETA\n"
                    f"{'─' * 80}\n\n"
                    f"{transcricao}\n"
                )

                exportar_pdf(conteudo, pdf_path, self._log)
                processados += 1

            self._log("\n" + "═" * 54)
            self._log(f"✅   Concluído! {processados}/{len(files)} arquivo(s) processado(s).")
            self._log("💜  O pacto foi concluído. Retornando ao sono eterno.")
            self._log("═" * 54)

        except Exception as e:
            self._log(f"\n❌   ERRO FATAL: {e}")
        finally:
            self.after(0, self._done)


if __name__ == "__main__":
    app = EscribaApp()
    app.mainloop()
