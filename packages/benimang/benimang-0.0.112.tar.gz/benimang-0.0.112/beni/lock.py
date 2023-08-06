import asyncio
from contextlib import asynccontextmanager, contextmanager
from functools import wraps
from pathlib import Path
from typing import Any, Callable, cast

import portalocker
from colorama.ansi import Fore

import beni
import beni.print as bprint


@contextmanager
def key(*keys: str, timeout: float = 0, quite: bool = False):
    lock_list: list[portalocker.Lock] = []
    keyfile_list: list[Path] = []
    for key in keys:
        lock, keyfile = _lock_acquire(key, timeout, quite)
        lock_list.append(lock)
        keyfile_list.append(keyfile)
    try:
        yield
    finally:
        for lock in lock_list:
            lock.release()
        for keyfile in keyfile_list:
            try:
                beni.remove(keyfile)
            except:
                pass


@asynccontextmanager
async def async_key(*keys: str, timeout: float = 0, quite: bool = False):
    with key(*keys, timeout=timeout, quite=quite):
        yield


def w_key(*keys: str, timeout: float = 0, quite: bool = False):
    def wraperfun(func: beni.Fun) -> beni.Fun:
        @wraps(func)
        def wraper(*args: Any, **kwargs: Any):
            with key(*keys, timeout=timeout, quite=quite):
                return func(*args, **kwargs)
        return cast(Any, wraper)
    return wraperfun


def wa_key(*keys: str, timeout: float = 0, quite: bool = False):
    def wraperfun(func: beni.AsyncFun) -> beni.AsyncFun:
        @wraps(func)
        async def wraper(*args: Any, **kwargs: Any):
            async with async_key(*keys, timeout=timeout, quite=quite):
                return await func(*args, **kwargs)
        return cast(Any, wraper)
    return wraperfun


class _Limit():
    def __init__(self, current: int, limit: int):
        self.current = current
        self.limit = limit


_limit_dict: dict[int, _Limit] = {}


def wa_limit(limit: int = 1):
    def wraperfun(func: beni.AsyncFun) -> beni.AsyncFun:
        @wraps(func)
        async def wraper(*args: Any, **kwargs: Any):
            funkey = id(func)
            if funkey not in _limit_dict:
                _limit_dict[funkey] = _Limit(0, limit)
            locknum = _limit_dict[funkey]
            try:
                while True:
                    if locknum.current < locknum.limit:
                        break
                    await asyncio.sleep(0)
                locknum.current += 1
                return await func(*args, **kwargs)
            finally:
                locknum.current -= 1

        return cast(Any, wraper)
    return wraperfun


def set_limit(fun: Callable, limit: int):
    funkey = id(fun)
    if funkey not in _limit_dict:
        _limit_dict[funkey] = _Limit(0, limit)
    else:
        _limit_dict[funkey].limit = limit


def _lock_acquire(key: str, timeout: float = 0, quite: bool = False):
    '''不对外部提供，只提供给 async_keylock 方法使用'''
    keyfile = beni.getpath_workspace(f'.lock/{beni.crcstr(key)}.lock')
    beni.makedir(keyfile.parent)
    while True:
        try:
            lock = portalocker.Lock(keyfile, timeout=timeout, fail_when_locked=timeout == 0)
            f = lock.acquire()
            f.write(key)
            f.flush()
            break
        except:
            if quite:
                raise Exception(f'资源被锁定无法继续操作 key={key} keyfile={keyfile}')
            else:
                bprint.print_color(f'资源被锁定无法继续操作 key={key} keyfile={keyfile}', colorList=[Fore.LIGHTRED_EX])
                inputvalue = beni.hold(f'重试（retry）或退出（exit）', False, 'retry', 'exit')
                match inputvalue:
                    case 'retry':
                        print('正在重试...')
                    case 'exit':
                        raise Exception(f'资源被锁定无法继续操作 - {key}')
                    case _:
                        pass
    return lock, keyfile
