import os
import time
import textwrap

from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import whisper
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# ==============================================================================
#                 💜  ESCRIBA v4.1 – TRANSCRIÇÃO & RESUMO ÁUDIO  💜
# ==============================================================================

# 0. Carrega variáveis do .env (se existir)
load_dotenv()

# 1. API KEY DO GEMINI  (já utilizada anteriormente)
API_KEY_GEMINI = os.getenv("GEMINI_API_KEY", "****************************************").strip()

# 3. Instrução de sistema para o GEMINI (resumo em tópicos)
SYSTEM_INSTRUCTION = """
ATUE COMO: Um assistente especialista em resumir reuniões, aulas, talks, podcasts e áudios longos em português.

OBJETIVO:
- Ler a transcrição de um arquivo de áudio.
- Entender rapidamente o contexto (reunião, aula, conversa, planejamento etc.).
- Organizar o conteúdo em um resumo claro, em tópicos, destacando:
  - Tema geral.
  - Pontos principais discutidos.
  - Decisões tomadas.
  - Tarefas/ações e, se possível, responsáveis.

ESTILO:
- Escreva sempre em português do Brasil.
- Seja direto, organizado e profissional, mas com tom leve.
- Use alguns emojis para tornar o texto mais agradável e visual (por ex.: ✅, 📝, 📌, 💡, 🎯),
  porém com moderação (não mais que 1 ou 2 por subtítulo ou bloco).

FORMATO ESPERADO:
- Um título geral para o áudio.
- Seção "Visão Geral" com 2–5 frases.
- Seção "Pontos Principais" em tópicos organizados.
- Seção "Decisões e Ações" se houver decisões explícitas.
- Seção "Próximos Passos" se forem mencionadas tarefas futuras.

NUNCA:
- Inventar conteúdo que não está implícita ou explicitamente na transcrição.
- Exagerar nos emojis.
"""

# ==============================================================================

def blindagem_de_diretorio():
    """Garante que a Escriba trabalhe na pasta onde o arquivo .py está."""
    try:
        caminho_real = os.path.dirname(os.path.abspath(__file__))
        os.chdir(caminho_real)
        print(f"🛡️  Blindagem Ativa. Diretório de trabalho: {caminho_real}")
        return caminho_real
    except Exception as e:
        print(f"❌ Falha na blindagem de diretório: {e}")
        return "."


def assinatura():
    print("\n" + "█" * 72)
    print("█      P R O J E T O   E S C R I B A   v4.1 (Áudio → PDF)".ljust(71) + "█")
    print("█      ------------------------------------------------   ".ljust(71) + "█")
    print("█      Pipeline: Whisper (OpenAI)  ➜  Gemini (Resumo)     ".ljust(71) + "█")
    print("█      Forge by: Regia LCN  &  Charlotte                  ".ljust(71) + "█")
    print("█" * 72 + "\n")


def transcrever_audio_whisper_local(audio_path: str) -> str | None:
    """
    Usa o Whisper local (open-source) para transcrever um arquivo de áudio .mp3.
    Não consome créditos da OpenAI, mas usa CPU/GPU da sua máquina.
    """
    print(f"🎙️  Transcrevendo áudio (Whisper local): {audio_path}...")
    try:
        # Modelos possíveis: "tiny", "base", "small", "medium", "large"
        # Quanto maior, mais preciso e mais pesado.
        model = whisper.load_model("base")
        result = model.transcribe(audio_path, language="pt")
        transcricao = (result.get("text") or "").strip()
        if transcricao:
            print("✅  Transcrição concluída (local).")
            return transcricao
        else:
            print("⚠️  Whisper local não retornou texto.")
            return None
    except Exception as e:
        print(f"❌ Erro na transcrição com Whisper local: {e}")
        return None


def gerar_resumo_gemini(model, transcricao: str) -> str | None:
    """Usa o Gemini para transformar a transcrição em um resumo organizado."""
    print("🧠  Gerando resumo com Gemini...")
    try:
        prompt = f"""
Você recebeu a transcrição literal de um arquivo de áudio (reunião, aula, conversa, podcast, etc.).

TRANSCRIÇÃO:
\"\"\"{transcricao}\"\"\"

TAREFA:
- Identifique o tema geral do áudio.
- Organize um resumo em português do Brasil, em seções e tópicos.
- Destaque decisões, tarefas e próximos passos quando existirem.
- Use alguns emojis discretos para deixar a leitura agradável (sem exageros).

FORMATO:
1. Um título geral.
2. Seção "Visão Geral" em 2–5 frases.
3. Seção "Pontos Principais" em tópicos.
4. Seção "Decisões e Ações" (se existir).
5. Seção "Próximos Passos" (se existir).
"""
        response = model.generate_content(prompt)
        resumo = (response.text or "").strip()
        print("✅  Resumo gerado.")
        return resumo
    except Exception as e:
        print(f"❌ Erro ao gerar resumo com Gemini: {e}")
        return None


def salvar_pdf(conteudo: str, caminho_pdf: str):
    """Gera um PDF simples com o conteúdo em texto, com quebra de linha automática."""
    print(f"📄  Gerando PDF: {caminho_pdf}...")
    try:
        c = canvas.Canvas(caminho_pdf, pagesize=A4)
        width, height = A4

        margem_x = 50
        margem_top = 50
        margem_bottom = 50
        y = height - margem_top

        wrapper = textwrap.TextWrapper(width=95, replace_whitespace=False)

        for linha in conteudo.splitlines():
            # Quebra linhas muito longas
            linhas_quebradas = wrapper.wrap(linha) or [""]
            for sublinha in linhas_quebradas:
                if y <= margem_bottom:
                    c.showPage()
                    y = height - margem_top
                c.drawString(margem_x, y, sublinha)
                y -= 14  # espaçamento de linha

        c.save()
        print("✅  PDF salvo com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao gerar PDF: {e}")


def main():
    # --- ESCUDO GLOBAL DE ERRO ---
    try:
        assinatura()

        # 1. Ativa a Blindagem
        folder_path = blindagem_de_diretorio()

        # 2. Configura a API do Gemini
        genai.configure(api_key=API_KEY_GEMINI)

        # 3. Configurações de Segurança do Gemini
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        # 4. Carrega o Modelo Gemini com a System Instruction para resumos
        try:
            model = genai.GenerativeModel(
                model_name="gemini-2.5-pro",  # modelo mais avançado
                system_instruction=SYSTEM_INSTRUCTION,
                safety_settings=safety_settings,
            )
        except Exception as e:
            print(f"❌ Erro crítico ao carregar o modelo Gemini: {e}")
            print("💡 Dica: Verifique se sua API Key do Gemini tem acesso ao modelo solicitado.")
            raise e

        print("💜 Invocação bem sucedida. O pacto foi aceito, A Escriba agora está ouvindo tudo (Whisper local).")

        valid_extensions = {".mp3"}
        files = os.listdir(folder_path)
        files.sort()  # Ordena para ficar bonito no log

        processados = 0

        for filename in files:
            name, ext = os.path.splitext(filename)
            if ext.lower() not in valid_extensions:
                continue

            audio_path = os.path.join(folder_path, filename)
            pdf_filename = f"{name}.pdf"

            if os.path.exists(pdf_filename):
                print(f"⏭️  Pulado (PDF já existe): {pdf_filename}")
                continue

            # 6. Transcreve o áudio com Whisper local
            transcricao = transcrever_audio_whisper_local(audio_path)
            if not transcricao:
                print("⚠️  Sem transcrição, pulando este arquivo.")
                continue

            # 7. Gera resumo com Gemini (se possível)
            resumo = gerar_resumo_gemini(model, transcricao)
            if not resumo:
                print("⚠️  Sem resumo (falha no Gemini). O PDF será gerado apenas com a transcrição.")
                resumo = "Resumo não gerado devido a erro no serviço Gemini (ex.: quota/429).\n" \
                         "Abaixo segue apenas a transcrição completa do áudio. 💜"

            # 8. Monta conteúdo final do PDF (transcrição + resumo ou só transcrição)
            conteudo_pdf = (
                f"Arquivo de origem: {filename}\n"
                f"{'-' * 80}\n"
                f"RESUMO ORGANIZADO\n"
                f"{'-' * 80}\n\n"
                f"{resumo}\n\n"
                f"{'-' * 80}\n"
                f"TRANSCRIÇÃO COMPLETA\n"
                f"{'-' * 80}\n\n"
                f"{transcricao}\n"
            )

            salvar_pdf(conteudo_pdf, pdf_filename)
            processados += 1

            # Pequena pausa de gentileza com as APIs
            time.sleep(1.5)

        print("\n" + "=" * 40)
        print(f"✅ SUCESSO! {processados} arquivo(s) .mp3 transcritos e convertidos em PDF.")
        print("O Pacto foi concluído, retornando ao sono eterno 💜")
        print("=" * 40)

    except Exception as e:
        print("\n" + "☠️" * 20)
        print(f"ERRO FATAL (A Escriba caiu): {e}")
        print("☠️" * 20)

    input("\nPressione Enter para encerrar...")


if __name__ == "__main__":
    main()
