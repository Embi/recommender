FROM node:23-alpine as build

COPY . app/
WORKDIR /app

RUN npm install
RUN npm run build

FROM nginx

COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY nginx/env.template /etc/nginx/templates/env.template
COPY --from=build /app/dist /usr/share/nginx/html
