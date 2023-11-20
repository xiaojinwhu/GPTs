# 第一阶段：构建
FROM python:3.10 AS builder

# RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
# RUN sed -i s@/security.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN apt-get clean && apt-get update
# RUN apt-get -o Dpkg::Options::="--force-confmiss" install --reinstall --yes build-essential && apt-get clean && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 安装Poetry
RUN pip install --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple/ pip \
    && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ poetry nuitka ordered-set

# 复制项目文件
COPY pyproject.toml poetry.lock ./

# 安装依赖
RUN poetry config virtualenvs.create false  \ 
    && poetry install --only main --no-interaction --no-ansi --no-root


COPY . /app/

RUN python -m nuitka --module api_server --include-package=api_server && \
    python -m nuitka --module gpts --include-package=gpts 

# 第二阶段：运行
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10-slim

# 设置工作目录
WORKDIR /app
ENV PYTHONPATH=/app/pkgs
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ --upgrade pydantic fastapi

COPY data /app/data
# 复制构建阶段的Python依赖
# COPY --from=builder /app/assets/ /assets/
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /app/*.so /app/pkgs/

ENV MODULE_NAME=api_server.app 
ENV DATA_PATH=/app/data/drugs.csv
