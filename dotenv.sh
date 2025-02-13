#!/bin/bash

# 현재 스크립트의 위치를 기반으로 프로젝트 루트 경로 설정
PROJECT_ROOT=$(pwd)

# .env 파일 생성 또는 덮어쓰기
echo "PROJECT_ROOT=$PROJECT_ROOT" > .env

# 생성된 .env 내용 확인
echo ".env 파일이 생성되었습니다."
cat .env