class Config:
    DB_URL = "postgresql+asyncpg://postgres:567234@localhost:5432/postgres"


config = Config

"""
docker run --name db-postgres -p 5432:5432 -e POSTGRES_PASSWORD=567234 -d postgres

"""
