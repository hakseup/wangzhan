FROM node:24-bookworm-slim
ENV NODE_ENV=production
WORKDIR /app
COPY dist ./dist
COPY server ./server
RUN mkdir -p /app/data/runtime && chown -R node:node /app/data
USER node
EXPOSE 3000
CMD ["node","server/start.mjs"]
