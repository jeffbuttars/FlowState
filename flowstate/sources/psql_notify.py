import asyncio
import logging
import traceback
from os import environ

import asyncpg

from .base import AsyncSource

logger = logging.getLogger(__name__)

PGHOST = environ.get("PGHOST", "127.0.0.1")
PGPORT = int(environ.get("PGPORT", 5432))
PGUSER = environ.get("PGUSER", "")
PGDATABASE = environ.get("PGDATABASE", "")
PGPASSWORD = environ.get("PGPASSWORD", "")


class PsqlNotify(AsyncSource):
    def __init__(
        self,
        *args,
        host: str = PGHOST,
        port: int = PGPORT,
        user: str = PGUSER,
        password: str = PGPASSWORD,
        database: str = PGDATABASE,
        dsn: str = "",
    ):
        super().__init__(*args)
        self._host: str = host
        self._port: int = port
        self._user: str = user
        self._password: str = password
        self._database: str = database
        self._dsn: str = dsn

        self._db_conn = None
        self.task = None

        self.running = False

    async def wait_for_connection(self):
        self._db_conn = await asyncpg.connect(
            dsn=self._dsn,
            host=self._host,
            port=self._port,
            user=self._user,
            password=self._password,
            database=self._database,
        )

        val = self._db_conn.fetchval("SELECT 1")

        while val != 1:
            logger.info("Waiting for database connection ...")
            await asyncio.sleep(1)
            val = self._db_conn.fetchval("SELECT 1")

        return self._db_conn

    async def start(self):
        self.running = True

    async def stop(self):
        self.running = False

    async def run(self):
        while self.running:
            try:
                self.task = asyncio.create_task(self.task_func(), name="PsqlNotify Task")
                await self.task
            except asyncio.CancelledError:
                pass
            except Exception as exc:
                logger.error("%s", exc)
                logger.error("%s", traceback.format_exc())

                if not self.task.cancelled():
                    self.task.cancel()
                    try:
                        await self.task
                    except asyncio.CancelledError:
                        pass

                self.task = None

    async def task_func(self):
        await self.wait_for_connection()
