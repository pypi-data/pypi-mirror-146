from typing import Any, Final

import yaml

import beni
import beni.file as bfile


_storagePath: Final = beni.getpath_workspace('.storage')


def _getStorageFile(key: str):
    return beni.getpath(_storagePath, f'{key}.yaml')


async def a_get_storage(key: str, default: Any = None):
    storageFile = _getStorageFile(key)
    if storageFile.is_file():
        content = await bfile.readfile_text(storageFile)
        return yaml.safe_load(content)
    else:
        return default


async def a_set_storage(key: str, value: Any):
    storageFile = _getStorageFile(key)
    content = yaml.safe_dump(value)
    return await bfile.writefile_text(storageFile, content)


async def clear_storage(*keyList: str):
    for key in keyList:
        storageFile = _getStorageFile(key)
        beni.remove(storageFile)


async def clear_all_storage():
    for storageFile in beni.list_file(_storagePath):
        beni.remove(storageFile)
