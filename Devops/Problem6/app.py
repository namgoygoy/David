from flask import Flask, request, Response
import os
from io import BytesIO
from gtts import gTTS

DEFAULT_LANG = os.getenv('DEFAULT_LANG', 'ko')
app = Flask(__name__)

@app.route("/")
def home():
    text = "Hello, DevOpss"
    lang = request.args.get('lang', DEFAULT_LANG)
    fp = BytesIO()
    gTTS(text, "com", lang).write_to_fp(fp)
    return Response(fp.getvalue(), mimetype='audio/mpeg')

if __name__ == "__main__":
    # 5000 번대로 수정 합니다.
    app.run('0.0.0.0', 80)
