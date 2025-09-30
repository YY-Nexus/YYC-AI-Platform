FROM node:18-alpine

# Set environment variables for M4 optimization
ENV NODE_ENV=production
ENV NPM_CONFIG_LOGLEVEL=warn

WORKDIR /app

# Install dependencies with M4 optimizations
COPY package*.json ./
RUN npm ci --only=production

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Command with M4 optimizations for Apple Silicon
CMD ["node", "--max-old-space-size=512", "--use-largepages=on", "server.js"]