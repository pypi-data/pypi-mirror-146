import traceback
from datetime import datetime as Datetime
from functools import wraps
from pathlib import Path
from typing import Any, Final, cast
from uuid import uuid4

import nest_asyncio
import typer
from colorama import Back, Fore

import beni
import beni.log as blog
import beni.print as bprint

_startTime: Datetime | None = None
_logFile: Path | None = None

nest_asyncio.apply()
app: Final = typer.Typer()


def w_task(func: beni.Fun) -> beni.Fun:
    @wraps(func)
    def wraper(*args: Any, **kwargs: Any):
        global _startTime
        _startTime = Datetime.now()
        try:
            blog.init(logFile=_logFile)
            return func(*args, **kwargs)
        except BaseException as ex:
            if type(ex) is SystemExit and ex.code == 0:
                pass
            else:
                bprint.set_color(Fore.LIGHTRED_EX)
                blog.error(str(ex))
                blog.error('执行失败')
                traceback.print_exc()
        finally:

            if blog.getcount_critical():
                color = Fore.LIGHTWHITE_EX + Back.LIGHTMAGENTA_EX
            elif blog.getcount_error():
                color = Fore.LIGHTWHITE_EX + Back.LIGHTRED_EX
            elif blog.getcount_warning():
                color = Fore.BLACK + Back.LIGHTYELLOW_EX
            else:
                color = Fore.BLACK + Back.LIGHTGREEN_EX

            bprint.set_color(color)
            blog.info('-' * 75)

            msgAry = ['任务结束']
            if blog.getcount_critical():
                msgAry.append(f'critical({blog.getcount_critical()})')
            if blog.getcount_error():
                msgAry.append(f'error({blog.getcount_error()})')
            if blog.getcount_warning():
                msgAry.append(f'warning({blog.getcount_warning()})')

            bprint.set_color(color)
            blog.info(' '.join(msgAry))

            passTime = str(Datetime.now() - _startTime)
            if passTime.startswith('0:'):
                passTime = '0' + passTime
            blog.info(f'用时: {passTime}')

    return cast(Any, wraper)


def set_log_path(log_path: Path):
    if _startTime:
        blog.warning('task.setLogDir 必须在任务启动前调用，本次忽略执行')
    else:
        global _logFile
        _logFile = beni.getpath(log_path, f'{uuid4()}.log')


@w_task
def run():
    app()


@w_task
def debug(*args: str):
    from typer.testing import CliRunner
    CliRunner().invoke(app, args)
