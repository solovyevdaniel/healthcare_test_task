import config
from connectors.postgres import PostgresDb

postgres = PostgresDb(
    user=config.DB_USER,
    password=config.DB_PASS,
    host=config.DB_HOST,
    port=config.DB_PORT,
    db_name=config.DB_NAME,
)

db = postgres