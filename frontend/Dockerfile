FROM node:9

WORKDIR /usr/app
COPY . /usr/app/

RUN npm install
RUN npm run build

EXPOSE 443
EXPOSE 80

CMD ["node", "-r", "esm", "index.js"]