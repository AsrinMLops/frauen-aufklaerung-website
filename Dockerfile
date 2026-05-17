FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
COPY magazin.html /usr/share/nginx/html/magazin.html
COPY admin.html /usr/share/nginx/html/admin.html
EXPOSE 80
