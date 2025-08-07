from flask import Flask, request, render_template # Flask 모듈을 임포트합니다.
from gtts import gTTS
from datetime import datetime
import io
import base64
import socket # 컴퓨터의 호스트 이름을 가져오기 위해 socket 모듈을 임포트합니다.

app = Flask(__name__)

VALID_LANGS = {'ko', 'en', 'ja', 'es'}

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    audio = None

    # 디버그 모드에서만 컴퓨터(인스턴스) 이름을 표시합니다.
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
                # 텍스트 변환 로그를 파일에 기록합니다.
                with open("input_log.txt", "a", encoding="utf-8") as f:
                    f.write(f"{datetime.now()} - 텍스트: {input_text}, 언어: {lang}\n")

                tts = gTTS(text=input_text, lang=lang)
                mp3_fp = io.BytesIO()
                tts.write_to_fp(mp3_fp)
                mp3_fp.seek(0)
                audio = base64.b64encode(mp3_fp.read()).decode('utf-8')
            except Exception as e:
                error = f"음성 생성 실패: {e}"

    # render_template 호출 시 컴퓨터 이름(hostname)을 인자로 전달합니다.
    return render_template("index.html", error=error, audio=audio, computername=hostname)

# --- 메뉴 화면 라우트 시작 ---
@app.route('/menu') 
def menu():
    # 'templates' 폴더 안의 'menu.html' 파일을 렌더링합니다.
    return render_template('menu.html')
# --- 메뉴 화면 라우트 끝 ---

if __name__ == "__main__":
    # 개발 편의를 위해 debug 모드를 활성화하고 서버를 실행합니다.
    app.run("0.0.0.0", 80, debug=True)