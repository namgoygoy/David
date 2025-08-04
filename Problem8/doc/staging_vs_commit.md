# Git: 스테이징 영역에 추가(git add)와 커밋(git commit)의 차이

Git은 변경 사항을 관리할 때 두 단계로 나눠서 처리합니다:  
**1. 스테이징(Stage) 영역에 추가**  
**2. 커밋(Commit)**

---

## ✅ 1. git add: 스테이징 영역에 변경 사항 추가

`git add` 명령어는 **작업 디렉토리에서 수정한 파일을 스테이징 영역(Stage)으로 이동**시킵니다.

### 📌 역할
- 변경된 파일을 커밋 대상으로 지정함.
- 실제 커밋은 하지 않음.

### 🧪 예시
```bash
git add hello.py
hello.py 파일의 변경사항이 스테이징 영역에 올라감. 아직 커밋되지는 않음.
✅ 2. git commit: 스테이징된 변경 사항을 저장소에 기록

git commit 명령어는 스테이징 영역에 있는 변경사항을 Git 저장소에 영구적으로 기록합니다.

📌 역할
프로젝트의 특정 시점 상태를 "스냅샷"처럼 저장함.
메시지와 함께 기록되므로 변경 내역을 추적 가능.
🧪 예시
git commit -m "Fix: update print statement"
-m 옵션은 커밋 메시지를 한 줄로 작성할 때 사용.
🔄 전체 흐름 예시

# 1. 파일 수정
nano app.py

# 2. 변경 내용 확인
git status

# 3. 스테이징 영역에 추가
git add app.py

# 4. 커밋으로 저장소에 반영
git commit -m "Update: improve app.py functionality"
🧠 요약

구분	설명	명령어 예시
git add	수정된 파일을 스테이징 영역에 올림	git add 파일명
git commit	스테이징된 내용을 저장소에 기록함	git commit -m "메시지"
📝 참고

커밋 전에는 항상 git status로 어떤 파일이 스테이징되었는지 확인하세요.
git add . 또는 git add -A는 전체 파일을 스테이징합니다.

---

이제 위 내용을 `git_add_vs_commit.md` 파일로 저장한 후, 아래 명령어로 Git에 업로드하시면 됩니다:

```bash
git add git_add_vs_commit.md
git commit -m "Docs: git add와 commit의 차이 정리 문서 추가"
git push origin main

## 요약 
git add는 수정한 파일을 커밋하기 전 스테이징 영역에 올리는 명령어입니다.
git commit은 스테이징된 파일을 로컬 저장소에 스냅샷으로 기록하는 작업입니다.
즉, add는 준비 단계이고, commit은 실제 기록 단계입니다.