from typing import Any, Final

import yaml

import beni
import beni.file as bfile


async def get(key: str, default: Any = None):
    storageFile = _get_storage_file(key)
    if storageFile.is_file():
        content = await bfile.readfile_text(storageFile)
        return yaml.safe_load(content)
    else:
        return default


async def set(key: str, value: Any):
    storageFile = _get_storage_file(key)
    content = yaml.safe_dump(value)
    return await bfile.writefile_text(storageFile, content)


async def clear(*keyList: str):
    for key in keyList:
        storageFile = _get_storage_file(key)
        beni.remove(storageFile)


async def clear_all():
    for storageFile in beni.list_file(_storage_path):
        beni.remove(storageFile)

# ------------------------------------------------------------------------------------------

_storage_path: Final = beni.getpath_workspace('.storage')


def _get_storage_file(key: str):
    return beni.getpath(_storage_path, f'{key}.yaml')
