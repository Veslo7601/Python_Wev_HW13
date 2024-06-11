import asyncio
import asyncpg

async def main():
    db_host = 'localhost'
    db_port = 5432
    db_user = 'postgres'
    db_password = 'postgres'
    db_name = 'postgres_async'

    connection = await asyncpg.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        database=db_name
    )

    try:
        result = await connection.fetch('SELECT 1')
        print('Підключення успішне:', result)
    finally:
        await connection.close()

asyncio.run(main())
