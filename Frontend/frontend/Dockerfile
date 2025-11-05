# Dockerfile (Next.js production)
# Stage 1: builder
FROM node:20-alpine AS builder
WORKDIR /app
ENV NODE_ENV=production

# instalar dependencias
COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* /app/
RUN if [ -f package-lock.json ]; then npm ci; else npm install; fi

COPY . .
RUN npm run build

# Stage 2: runner
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
# copiar artefactos
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

EXPOSE 3000
CMD ["npm", "start"]
