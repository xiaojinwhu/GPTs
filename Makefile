-include .env
export $(shell sed 's/=.*//' .env)
export current_dir=$(shell pwd)

IMAGE_NAME=gpts
VERSION=1.0
PORT=8051
CONTAINER_NAME=gpts-func


test-local-api:
	uvicorn api_server.api:app  --port ${PORT} --host 0.0.0.0 --reload 


build:
	docker build -t ${IMAGE_NAME}:${VERSION} .

deploy-test:
	docker rm -f ${CONTAINER_NAME} || true
	docker run -d --name ${CONTAINER_NAME} \
	--network llm \
	-v ${current_dir}/log:/log \
	-p ${PORT}:80 \
	-e MAX_WORKERS=2 \
	-e MODEL_NAME=/Qwen-7B-Chat \
	-e API_BASE=http://llm:8080/v1 \
	   ${IMAGE_NAME}:${VERSION}
