import json
from pathlib import Path
from typing import Union
from uuid import UUID

from metagen.base import Leaf


# helper functions

def create_file(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def check_path(path: Union[Path, str]) -> Path:
    if not isinstance(path, Path):
        return Path(path)
    return path


def prepare_data_for_leaf(obj: dict) -> dict:
    new = obj.copy()
    data = new.pop('data')
    new.update(data)
    return new


def open_json(path: Union[str, Path], encoding='utf8'):
    with open(path, 'r', encoding=encoding) as file:
        return json.load(file)


def set_key_from_input(value: Union[str, UUID, Leaf]):
    """
    Helper method used as validator in pydantic model.
    For input string, Leaf or UUID return valid UUID
    """
    if isinstance(value, Leaf):
        return value.key
    if isinstance(value, str):
        return UUID(value)
    return value


# helper class
class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return json.JSONEncoder.default(self, obj)
