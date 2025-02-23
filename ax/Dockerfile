FROM node:22-bookworm

WORKDIR /app
COPY . . 
RUN npm i 
CMD ["npm", "run", "dev"]

# # Stage 1: Build the Next.js application
# FROM node:20 AS builder
# WORKDIR /app
#
# # Copy package files and install dependencies
# COPY package*.json ./
# RUN npm install
#
# # Copy source files and build
# COPY . .
# RUN npm run build
#
# # Stage 2: Production environment
# FROM node:20-alpine AS production
# WORKDIR /app
#
# # Set production environment variables
# ENV NODE_ENV production
#
# # Install production dependencies
# COPY package*.json ./
# RUN npm ci --omit=dev
#
# # Copy built assets from builder
# COPY --from=builder /app/.next ./.next
# COPY --from=builder /app/public ./public
# COPY --from=builder /app/package.json ./package.json
#
# # Uncomment if using next.config.js or other config files
# # COPY --from=builder /app/next.config.js ./
#
# # Expose port and start application
# EXPOSE 3000
# CMD ["npm", "start"]
