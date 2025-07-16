from flask import Flask
app = Flask(__name__)

VALID_LANGS = {'ko', 'en', 'ja', 'es'}

@app.route('/', methods=['GET', 'POST'])
def index():
    # 한번 초기화를 위하여
    error = None
    audio = None

    if request.method == 'POST':
        input_text = request.form.get('input_text', '').strip()
        lang = request.form.get('lang', 'ko')
        # 아무 언어도 사용하지 안았을 경우 ko 사용 했을 떄 해당하는 언어 

        # 입력 검증
        if not input_text:
            error = "텍스트를 입력하세요."
        elif lang not in VALID_LANGS:
            error = f"지원하지 않는 언어입니다: {lang}"
        else:
            try:
                # 로그 기록
                with open("input_log.txt", "a", encoding="utf-8") as f:
                    # 객체 이름 f
                    f.write(f"{datetime.now()} - 텍스트: {input_text}, 언어: {lang}\n")

                # TTS 처리
                tts = gTTS(text=input_text, lang=lang)
                mp3_fp = io.BytesIO()
                tts.write_to_fp(mp3_fp)
                mp3_fp.seek(0)
                audio = base64.b64encode(mp3_fp.read()).decode('utf-8')
            except Exception as e:
                error = f"음성 생성 실패: {e}"

    return render_template("index.html", error=error, audio=audio)

if __name__ == "__main__":
    app.run("0.0.0.0", 80)
