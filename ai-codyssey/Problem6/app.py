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
    gTTS(text, lang=lang).write_to_fp(fp)
    
    return Response(fp.getvalue(), mimetype='audio/mpeg')

if __name__ == "__main__":
    # 포트 번호를 5000으로 변경하여 실행 (기존 80에서 변경됨)
    app.run('0.0.0.0', 5000)
