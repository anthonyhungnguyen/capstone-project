FROM node:12-slim as build
WORKDIR /frontend
COPY package.json ./
COPY . ./
RUN yarn 
RUN yarn build

FROM nginx:stable-alpine
WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY --from=build /frontend/build .

COPY --from=build /frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]