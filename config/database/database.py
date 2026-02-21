from sqlalchemy import text
from config.settings import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine


class DatabaseManager:
    def __init__(self):
        self.engines = {}
        self.sessions = {} 
        if hasattr(settings, "DATABASES") and isinstance(settings.DATABASES, dict):
            for db_name, db_config in settings.DATABASES.items():
                print(self._create_connection_string(db_config),"==========")
                engine = create_async_engine(
                    self._create_connection_string(db_config), echo=True)
                self.engines[db_name] = engine
                self.sessions[db_name] = sessionmaker(
                    bind=engine, class_=AsyncSession, expire_on_commit=False
                )

    @staticmethod
    def _create_connection_string(db_config):
        return (
            f"{db_config['ENGINE']}://{db_config['USER']}:{db_config['PASSWORD']}@"
            f"{db_config['HOST']}:{db_config['PORT']}/{db_config['NAME']}"
        )

    async def get_db(self, db_name="investment_db"):
        if db_name not in self.sessions:
            raise ValueError(f"Database '{db_name}' not found in settings.")

        session = self.sessions[db_name]()
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            print(f"Database error: {e}")
            raise
        finally:
            await session.close()

    @asynccontextmanager
    async def get_context_db(self, db_name="investment_db"):
        if db_name not in self.sessions:
            raise ValueError(f"Database '{db_name}' not found in settings.")

        session = self.sessions[db_name]()
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            print(f"Database error: {e}")
            raise
        finally:
            await session.close()

    async def validate_connections(self): 
        if not self.engines:
            print("No DATABASES found in settings. Skipping DB validation.")
            return

        for db_name, engine in self.engines.items():
            try:
                async with engine.begin() as conn:
                    await conn.execute(text("SELECT 1"))
                print(f"Connected to {db_name} database successfully!")
            except SQLAlchemyError as e:
                print(f"Database Connection Error in {db_name}: {e}")
                exit(1)


db_manager = DatabaseManager()