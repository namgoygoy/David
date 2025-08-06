from flask import Flask, request, render_template # Flask 모듈에서 Flask, request, render_template 함수를 임포트합니다. 'render_template'는 HTML 템플릿 파일을 렌더링하는 데 사용됩니다.
from gtts import gTTS
from datetime import datetime
import io
import base64

app = Flask(__name__)

VALID_LANGS = {'ko', 'en', 'ja', 'es'}

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    audio = None

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

    return render_template("menu.html", error=error, audio=audio)

# --- 새로 추가된 /menu 라우트 시작 ---
@app.route('/menu') 
def menu():
    # 'templates' 폴더 안에 있는 'menu.html' 파일을 찾아서 사용자에게 웹 페이지로 보여줍니다.
    return render_template('menu.html')
# --- 새로 추가된 /menu 라우트 끝 ---

if __name__ == "__main__":
    app.run("0.0.0.0", 80, debug=True) # 개발 편의를 위해 debug 모드를 활성화했습니다. 코드 변경 시 서버가 자동으로 재시작됩니다.
