## 반달곰 커피 홈페이지

참조링크: https://반달곰 커피

문구: 오디오 출력 소스코드

```python
lang = request.args.get('lang', DEFAULT_LANG)
fp = BytesIO()
gTTS(text, "com", lang).write_to_fp(fp)

![david](https://github.com/user-attachments/assets/b515263f-02ab-4d5c-a31e-b347325a1e37)
