FROM nginx:alpine
RUN echo '<!DOCTYPE html><html><head><title>PandaStack Test</title></head><body><h1>Hello from PandaStack!</h1></body></html>' > /usr/share/nginx/html/index.html
# 如果平台要求特定端口，用 sed 动态改写 nginx 配置监听该端口
CMD sh -c "sed -i 's/listen  *80;/listen ${PORT:-80};/' /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"
