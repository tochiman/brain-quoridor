FROM node:18.18.0-alpine

USER node:node

WORKDIR /home/node/app/

ENV WATCHPACK_POLLING=true

COPY brain-quoridor-front/package.json ./
RUN yarn install  --no-progress --network-timeout 1000000

EXPOSE 3000

CMD ["yarn", "dev"]
