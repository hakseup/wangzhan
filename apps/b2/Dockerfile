FROM node:24-bookworm-slim AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build:pwa
FROM node:24-bookworm-slim
ENV NODE_ENV=production
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=build /app/public/content.json ./public/content.json
COPY --from=build /app/server ./server
RUN mkdir -p /app/data/runtime && chown -R node:node /app/data
USER node
EXPOSE 3000
CMD ["node","server/start.mjs"]
