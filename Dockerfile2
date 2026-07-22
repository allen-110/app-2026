FROM nginxinc/nginx-unprivileged:alpine

# 这个镜像已经默认监听 8080，不需要改端口
# 缓存目录已经在镜像构建时设好了合适的权限，不需要运行时创建

COPY <<'EOF' /usr/share/nginx/html/index.html
<!DOCTYPE html>
<html>
<head><title>PandaStack Test</title></head>
<body><h1>Hello from PandaStack!</h1><p>NGINX container deployed successfully.</p></body>
</html>
EOF

EXPOSE 8080
