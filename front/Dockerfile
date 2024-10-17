FROM node:18.18.0-alpine

USER node:node

WORKDIR /home/node/app/

ENV WATCHPACK_POLLING=true

COPY brain-quoridor-front/package.json ./
RUN yarn install  --network-timeout 600000

EXPOSE 3000

CMD ["yarn", "dev"]
