# Bulletproof build for Railway (used automatically, bypasses railpack/nixpacks).
FROM node:20-slim

WORKDIR /app

# install deps first for layer caching
COPY package.json package-lock.json* ./
RUN npm install --omit=dev --no-audit --no-fund

# app source
COPY server.js ./
COPY public ./public

ENV NODE_ENV=production
# Railway injects PORT; default to 3000 locally
EXPOSE 3000
CMD ["node", "server.js"]
