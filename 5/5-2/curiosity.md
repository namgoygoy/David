Ubuntu란?
Debian 기반의 리눅스 운영체제
데스크탑, 서버, 클라우드, IoT 등 다양한 환경에서 사용
컨테이너용 플랫폼으로도 인기 (Docker, Kubernetes, LXD 등과 잘 호환됨)
개발은 **Canonical Ltd.**가 주도하며, 오픈소스 기반으로 누구나 자유롭게 사용/수정/배포 가능
✅ Docker에서의 Ubuntu 이미지 특징
Canonical이 제공한 공식 root 파일시스템을 기반으로 빌드됨
가장 최근의 LTS 버전이 ubuntu:latest 태그에 할당됨
ubuntu:rolling, ubuntu:devel 등의 태그로 최신 릴리스 또는 개발 버전 사용 가능


✅ "OFFICIAL" 이미지의 기준은?

항목	설명
✅ Official Image	Docker가 직접 관리하거나, Docker와 파트너십을 맺은 조직(Canonical 등)이 제공하는 공식 이미지입니다.
❌ Non-official Image	일반 사용자가 Docker Hub에 업로드한 이미지입니다. 이름은 같을 수 있어도 신뢰성은 보장되지 않습니다.

docker run -it ubuntu:20.04 bash
| 부분             | 의미                                                  |
| -------------- | --------------------------------------------------- |
| `docker run`   | 새로운 컨테이너 실행                                         |
| `-it`          | `-i`(interactive) + `-t`(pseudo-TTY): 터미널 연결을 위한 옵션 |
| `ubuntu:20.04` | 사용할 이미지                                             |
| `bash`         | 컨테이너 내부에서 실행할 명령어 (기본은 `/bin/sh`)                   |

✅ Docker에서 bash 쉘을 실행한다는 건?

docker run -it ubuntu:20.04 bash
이 명령은 다음과 같은 의미를 가집니다:

ubuntu:20.04 이미지를 기반으로
-it 옵션으로 내가 직접 명령어를 입력할 수 있는 터미널 인터페이스를 열고
그 안에서 bash 프로그램을 실행해서
컨테이너 안에 직접 들어가서 작업할 수 있도록 만든다