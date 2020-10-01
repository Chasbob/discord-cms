FROM node

RUN mkdir -p /opt/frontend
WORKDIR /opt/frontend

COPY ./package.json ./yarn.lock /opt/frontend/
RUN yarn install

COPY . /opt/frontend

EXPOSE 3000

CMD ./docker-entrypoint.sh
