FROM node:12 as web-build

WORKDIR /frontend

COPY package.json /frontend

RUN yarn && yarn build

CMD ["yarn", "start"]