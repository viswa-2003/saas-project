FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Install wait-for-it for health checks
RUN apk add --no-cache curl

# Expose port
EXPOSE 5000

# Start command with migration and seed
CMD ["sh", "-c", "sleep 10 && npm run seed && npm start"]

