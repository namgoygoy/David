from flask import Flask, request, Response
import os
from io import BytesIO
from gtts import gTTS

DEFAULT_LANG = os.getenv('DEFAULT_LANG', 'ko')
app = Flask(__name__)

@app.route("/")
def home():
    text = "Hello, DevOps"
    lang = request.args.get('lang', DEFAULT_LANG)
    fp = BytesIO()
    gTTS(text, "com", lang).write_to_fp(fp)
    # 읽을 문자, 도메인, 언어 설정. 음성을 가상의 공간의 저장
    return Response(fp.getvalue(), mimetype='audio/mpeg')
    # 메모리에 저장된 음성 데이터를 가지고 와 사용자에게 응답
    # write to fp 로 저장 -> fp.getvalue 가지고 옴

if __name__ == "__main__":
    app.run('0.0.0.0', 80)
