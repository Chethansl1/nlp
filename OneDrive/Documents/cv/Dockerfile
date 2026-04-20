FROM node:18-alpine AS frontend

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY public ./public
COPY src ./src

RUN npm run build

FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt ./backend/
RUN pip install -r backend/requirements.txt

COPY backend/ ./backend/
COPY --from=frontend /app/build ./static

EXPOSE 5000 3000

CMD ["python", "backend/app.py"]
