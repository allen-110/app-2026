FROM python:3.12-alpine

# 常用工具全部在构建阶段（root权限）装好，运行时不再需要写系统目录
RUN apk add --no-cache bash curl wget git vim less procps net-tools iputils

WORKDIR /app
COPY server.py .

# 关闭 python 的 buffering，日志直接走 stdout，不写文件，避免任何文件写入权限问题
ENV PYTHONUNBUFFERED=1
ENV HOME=/app

EXPOSE 8080
CMD ["python", "-u", "server.py"]
