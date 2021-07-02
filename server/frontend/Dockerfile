FROM node:12-slim

WORKDIR /frontend

COPY package.json ./
RUN yarn install -- && yarn add tailwindcss@npm:@tailwindcss/postcss7-compat postcss@^7 autoprefixer@^9

COPY . ./
EXPOSE 3000

CMD ["yarn", "start"]