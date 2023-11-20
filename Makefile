-include .env
export $(shell sed 's/=.*//' .env)
export current_dir=$(shell pwd)

IMAGE_NAME=gpts
VERSION=1.0
PORT=8000
CONTAINER_NAME=gpts-func


test-local-api:
	uvicorn api_server.app:app  --port ${PORT} --host 0.0.0.0 --reload 


build:
	docker build -t ${IMAGE_NAME}:${VERSION} .

push-docker:
	docker tag ${IMAGE_NAME}:${VERSION} xiaojinwhu/${IMAGE_NAME}:${VERSION}
	docker push xiaojinwhu/${IMAGE_NAME}:${VERSION}

deploy:
	docker rm -f ${CONTAINER_NAME} || true
	docker run -d --name ${CONTAINER_NAME} \
	-v ${current_dir}/log:/log \
	-p ${PORT}:80 \
	-e MAX_WORKERS=1 \
	${IMAGE_NAME}:${VERSION}
