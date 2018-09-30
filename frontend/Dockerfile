FROM node:alpine
WORKDIR /usr/app

EXPOSE 443
EXPOSE 80

CMD ["node", "-r", "esm", "index.js"]

COPY ./package.json /usr/app
COPY ./package-lock.json /usr/app
RUN npm install

COPY . /usr/app/
RUN npm run build
