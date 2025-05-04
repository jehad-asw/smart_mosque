version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
    environment:
      - DATABASE_URL=postgresql://smartuser:smartpass@postgres:5432/smartmosque
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - REDIS_PASSWORD=redispass
    volumes:
      - .:/app

  postgres:
    image: postgres:13
    environment:
      - POSTGRES_USER=smartuser
      - POSTGRES_PASSWORD=smartpass
      - POSTGRES_DB=smartmosque
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6-alpine
    command: redis-server --requirepass redispass
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data: