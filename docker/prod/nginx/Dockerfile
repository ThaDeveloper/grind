FROM nginx:1.17.6-alpine
LABEL MAINTAINTER="Justin Ndwiga"
#remove the default nginx config file and replace it with our custom file
RUN rm /etc/nginx/conf.d/default.conf 
COPY nginx.conf /etc/nginx/
