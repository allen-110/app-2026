FROM alpine:latest

# 安装 ttyd 和基础 shell 工具
RUN apk add --no-cache ttyd bash curl

EXPOSE 8080

# -p 8080 监听端口，-c 是 Basic Auth 的用户名:密码，务必换成你自己的强密码
CMD ["ttyd", "-p", "8080", "-c", "admin:a12345", "bash"]
