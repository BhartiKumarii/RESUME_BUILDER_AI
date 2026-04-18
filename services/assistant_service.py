from flask import Blueprint, request, jsonify, send_file, current_app
from flask_cors import CORS
import os
import tempfile
import base64
import time
import concurrent.futures
from deep_translator import GoogleTranslator
import google.generativeai as genai
import pyttsx3

assistant_bp = Blueprint("assistant", __name__)
CORS(assistant_bp)

# ---------- CONFIG ----------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    raise RuntimeError("❌ Please set GEMINI_API_KEY environment variable first.")
genai.configure(api_key=GEMINI_API_KEY)

# Thread pool for pyttsx3
executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)

# Try to keep model object for repeated calls
try:
    gemini_model = genai.GenerativeModel("gemini-2.5-flash")
except Exception:
    gemini_model = None

def text_to_speech_base64(text, lang="en"):
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tmp_path = tmp_file.name
    tmp_file.close()

    def _speak():
        engine = pyttsx3.init()
        engine.setProperty("rate", 170)
        try:
            engine.save_to_file(text, tmp_path)
            engine.runAndWait()
        finally:
            try:
                engine.stop()
            except Exception:
                pass

    future = executor.submit(_speak)
    future.result(timeout=30)

    with open(tmp_path, "rb") as f:
        audio_data = f.read()
    try:
        os.remove(tmp_path)
    except Exception:
        pass

    return base64.b64encode(audio_data).decode("utf-8")

@assistant_bp.route("/chat", methods=["POST"])
def chat():
    start_time = time.time()
    data = request.get_json(force=True)
    user_text = data.get("text", "").strip()
    lang = data.get("lang", "en")
    if not user_text:
        return jsonify({"error": "No text provided"}), 400

    processed = user_text
    if lang == "hi":
        try:
            processed = GoogleTranslator(source="auto", target="en").translate(user_text)
        except Exception:
            pass

    system_prompt = (
        "You are a polite, helpful AI assistant for blue-collar workers. "
        "Give short, clear, friendly answers about skills, jobs, and guidance."
    )

    if not gemini_model:
        return jsonify({"error": "Gemini model initialization failed"}), 500

    try:
        if hasattr(gemini_model, "generate_content"):
            response = gemini_model.generate_content(f"{system_prompt}\nUser: {processed}")
            reply_en = getattr(response, "text", str(response)).strip()
        elif hasattr(gemini_model, "generate"):
            response = gemini_model.generate(input=f"{system_prompt}\nUser: {processed}")
            # attempt to extract text from common response shapes
            reply_en = ""
            if isinstance(response, dict):
                candidates = response.get("candidates") or response.get("outputs") or []
                if candidates:
                    first = candidates[0]
                    reply_en = first.get("output") or first.get("content") or first.get("text") or str(first)
                else:
                    reply_en = str(response)
            else:
                reply_en = getattr(response, "text", str(response))
            reply_en = reply_en.strip()
        else:
            raise RuntimeError("Gemini client missing generate method")
    except Exception as e:
        return jsonify({"error": f"Gemini API failed: {e}"}), 500

    reply = reply_en
    if lang == "hi":
        try:
            reply = GoogleTranslator(source="en", target="hi").translate(reply_en)
        except Exception:
            pass

    try:
        audio_b64 = text_to_speech_base64(reply, lang)
    except Exception as e:
        return jsonify({"error": f"TTS failed: {e}"}), 500

    duration = round(time.time() - start_time, 2)
    current_app.logger.info(f"Assistant reply ready in {duration}s")

    return jsonify({"reply": reply, "audio_base64": audio_b64, "response_time": duration})

@assistant_bp.route("/assistant_icon.png")
def assistant_icon():
    root = current_app.root_path
    icon_path = os.path.join(root, "assistant_icon.png")
    if os.path.exists(icon_path):
        return send_file(icon_path)
    # fallback 1x1 transparent PNG
    transparent = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8Xw8AAoMBgXr4XxkAAAAASUVORK5CYII="
    )
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    try:
        tmp.write(transparent)
        tmp.flush()
        tmp.close()
        return send_file(tmp.name, mimetype="image/png")
    finally:
        try:
            os.remove(tmp.name)
        except Exception:
            pass