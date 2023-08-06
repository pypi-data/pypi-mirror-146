from __future__ import annotations

import asyncio
import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Iterable, Sequence

import aiosqlite

sqlite3.register_converter("bool", lambda x: bool(x))


class SqliteDbPool():

    _avaliable_list: asyncio.Queue[_SqliteDb]
    _using_list: list[_SqliteDb]

    def __init__(self, db_file: str | Path, count: int = 1):
        self._avaliable_list = asyncio.Queue()
        self._using_list = []
        self._db_file = db_file
        self._count = count

    async def close(self):
        while self._using_list or not self._avaliable_list.empty():
            xx = await self._avaliable_list.get()
            await xx.close()

    @asynccontextmanager
    async def get(self):
        if len(self._using_list) < self._count:
            if self._avaliable_list.empty():
                db = _SqliteDb()
                db.db = await aiosqlite.connect(self._db_file, detect_types=sqlite3.PARSE_DECLTYPES)
                db.db.row_factory = sqlite3.Row
            else:
                db = self._avaliable_list.get_nowait()
        else:
            db = await self._avaliable_list.get()
        self._using_list.append(db)
        try:
            yield db
            await db.commit()
        except:
            await db.rollback()
            raise
        finally:
            self._using_list.remove(db)
            await self._avaliable_list.put(db)


class _SqliteDb():

    db: aiosqlite.Connection

    async def insert(self, table: str, data: dict[str, Any]):
        keylist = sorted(data.keys())
        fieldname_list = ','.join([f'"{x}"' for x in keylist])
        placement_list = ','.join(['?' for _ in range(len(keylist))])
        fieldvalue_list = [data[x] for x in keylist]
        async with self.db.execute(
            f'''
            INSERT INTO "{table}" ({fieldname_list}) 
            VALUES 
                ({placement_list});
            ''',
            fieldvalue_list,
        ) as cursor:
            return cursor.lastrowid

    async def insert_many(self, table: str, data_list: Sequence[dict[str, Any]]):
        keylist = sorted(data_list[0].keys())
        fieldname_list = ','.join([f'`{x}`' for x in keylist])
        placement_list = ','.join(['?' for _ in range(len(keylist))])
        fieldvalue_list = [[data[x] for x in keylist] for data in data_list]
        cursor = await self.db.executemany(
            f'''
            INSERT INTO "{table}" ({fieldname_list}) 
            VALUES 
                ({placement_list});
            ''',
            fieldvalue_list
        )
        await cursor.close()

    async def fetch_all(self, sql: str, parameters: Iterable[Any] | None = None):
        async with self.db.execute(sql, parameters) as cursor:
            return await cursor.fetchall()

    async def fetch_one(self, sql: str, parameters: Iterable[Any] | None = None):
        async with self.db.execute(sql, parameters) as cursor:
            return await cursor.fetchone()

    async def execute(self, sql: str, parameters: Iterable[Any] | None = None):
        async with self.db.execute(sql, parameters) as cursor:
            return cursor.rowcount

    async def commit(self):
        await self.db.commit()

    async def rollback(self):
        await self.db.rollback()

    async def close(self):
        await self.db.close()
