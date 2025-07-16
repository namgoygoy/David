# 🐧 Linux 명령어 정리

## 📂 디렉토리 관련 명령어

### `ls` – 디렉토리 내용을 나열합니다.
- 예시: `ls -l`  
  (자세한 리스트 출력)

### `cd` – 디렉토리를 변경합니다.
- 예시: `cd /home`  
  (home 디렉토리로 이동)

- 예시: `cd Problem1`  
  (현재 위치에서 하위 폴더 Problem1로 이동)

- 예시: `cd ..`  
  (상위 디렉토리로 이동)

### `pwd` – 현재 작업 중인 디렉토리의 경로를 출력합니다.
- 예시: `pwd`

### `mkdir` – 새로운 디렉토리를 생성합니다.
- 예시: `mkdir new_directory`

### `rmdir` – 빈 디렉토리를 삭제합니다.
- 예시: `rmdir empty_directory`

---

## 📄 파일 관련 명령어

### `touch` – 새 파일을 생성하거나 파일의 타임스탬프를 변경합니다.
- 예시: `touch newfile.txt`

### `cp` – 파일이나 디렉토리를 복사합니다.
- 예시: `cp source.txt destination.txt`

### `mv` – 파일이나 디렉토리를 이동하거나 이름을 변경합니다.
- 예시: `mv oldname.txt newname.txt`

### `rm` – 파일이나 디렉토리를 삭제합니다.
- 예시: `rm unwanted.txt`

### `echo` – 텍스트를 출력하거나 파일에 텍스트를 작성합니다.
- 예시: `echo "Hello World" > hello.txt`

### `cat` – 파일의 내용을 화면에 출력합니다.
- 예시: `cat file.txt`

---

필요하면 GitHub에 올릴 수 있도록 `README.md` 스타일로도 바꿔줄 수 있어 😎  
이제 이 파일을 `linux-cheatsheet` 프로젝트 디렉토리에 저장하고 `git add .`로 관리하면 돼!  
원할 경우 push까지 도와줄게.
<<<<<<< HEAD
=======

깃 설치 확인
git --version

전역 설정 확인
git config --global core.autocrlf
git config --global user.name
git config --global user.email
git config --global init.defaultBranch

전역 설정 전체 보기
git config --global --list

전역 설정 에디터 보기
git config --global -e

기본 에디터 확인
git config --global core.editor

cd Problem4
Ls
ls -a

원격 저장소
git remote -v

가상환경 작동 
source venv/bin/activate

가상환경 비활성화 
deactivate

