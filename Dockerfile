FROM nginx:alpine

# 构建阶段（root权限）直接把监听端口改成固定值，比如 8080
RUN sed -i 's/listen  *80;/listen 8080;/' /etc/nginx/conf.d/default.conf

RUN echo '<!DOCTYPE html><html><head><title>PandaStack Test</title></head><body><h1>Hello from PandaStack!</h1><p>NGINX container deployed successfully.</p></body></html>' > /usr/share/nginx/html/index.html

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
