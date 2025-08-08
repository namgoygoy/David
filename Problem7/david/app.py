from flask import Flask, request, render_template
from gtts import gTTS
from datetime import datetime
import io
import base64
import socket

app = Flask(__name__)

VALID_LANGS = {'ko', 'en', 'ja', 'es'}

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    audio = None

    if app.debug:
        hostname = '컴퓨터(인스턴스) : ' + socket.gethostname()
    else:
        hostname = ' '

    if request.method == 'POST':
        input_text = request.form.get('input_text', '').strip()
        lang = request.form.get('lang', 'ko')

        if not input_text:
            error = "텍스트를 입력하세요."
        elif lang not in VALID_LANGS:
            error = f"지원하지 않는 언어입니다: {lang}"
        else:
            try:
                with open("input_log.txt", "a", encoding="utf-8") as f:
                    f.write(f"{datetime.now()} - 텍스트: {input_text}, 언어: {lang}\n")

                tts = gTTS(text=input_text, lang=lang)
                mp3_fp = io.BytesIO()
                tts.write_to_fp(mp3_fp)
                mp3_fp.seek(0)
                audio = base64.b64encode(mp3_fp.read()).decode('utf-8')
            except Exception as e:
                error = f"음성 생성 실패: {e}"

    return render_template("menu.html", error=error, audio=audio, computername=hostname)

@app.route('/menu') 
def menu():
    return render_template('menu.html')

@app.route("/test1")
def test1():
    return render_template('test1.html')

@app.route("/test2")
def test2():
    return render_template('test2.html')

if __name__ == "__main__":
    app.run("0.0.0.0", 80, debug=True)
