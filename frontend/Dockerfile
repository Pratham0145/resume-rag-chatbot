FROM node:20

WORKDIR /app

# Copy package files first
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy remaining files
COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]