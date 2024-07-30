
FROM node:14-alpine

# Set the working directory in the container
WORKDIR /app

COPY package*.json ./


RUN npm install

COPY . .

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]