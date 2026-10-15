# Production Dockerfile for Tax Calculator Application
FROM node:18-alpine AS production

# Set working directory
WORKDIR /app

# Set production environment
ENV NODE_ENV=production
ENV PORT=3000

# Copy package manifests first to leverage Docker layer caching
COPY package*.json ./

# Install only production dependencies
RUN npm ci --omit=dev --ignore-scripts && npm cache clean --force

# Copy application source files
COPY server.js ./
COPY taxCalculator.js ./
COPY index.html ./
COPY script.js ./
COPY style.css ./
COPY favicon.ico ./

# Use non-root node user provided by the official Node Alpine image for security
USER node

# Expose configurable application port
EXPOSE 3000

# Container healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

# Start the application
CMD ["node", "server.js"]
