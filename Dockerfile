version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - postgres
    environment:
      - DATABASE_URL=postgresql://smartuser:smartpass@postgres:5432/smartmosque

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


volumes:
  postgres_data:
  