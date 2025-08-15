# 이미지 받기
docker pull python:3

# 컨테이너 실행
docker run -it -p 80:80 --name test python:3 bash

# 컨테이너 재접속
docker exec -it test bash

# 호스트 → 컨테이너로 파일 복사
docker cp ./myproject test:/workspace

# 현재 상태를 이미지로 저장
docker commit test my_image

# 컨테이너 정지 및 삭제
docker stop test
docker rm test
