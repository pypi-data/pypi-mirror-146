# general and helper function and classe

from pathlib import Path
from typing import Union, Optional, List, Any
from pydantic import BaseModel, Field, root_validator
from pydantic.utils import ROOT_KEY
from abc import ABC, abstractmethod
from uuid import UUID, uuid4
import json


# helper class
class SingletonMeta(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instance[cls]


class BaseModelWithDynamicKey(BaseModel):
    """
    Pydantic workaoround for custom dynamic key
    ref: https://stackoverflow.com/questions/60089947/creating-pydantic-model-schema-with-dynamic-key
    """
    def __init__(self, **data: Any) -> None:
        if self.__custom_root_type__ and data.keys() != {ROOT_KEY}:
            data = {ROOT_KEY: data}
        super().__init__(**data)


# base
class LeafABC(BaseModel, ABC):
    key: UUID

    @abstractmethod
    def __nodes__(self) -> str:
        pass

    @property
    @abstractmethod
    def hash_attrs(self) -> tuple:
        pass


# element base parent
class Leaf(LeafABC):
    key: Optional[Union[UUID, str]] = Field(default_factory=uuid4)

    def to_dict(self):
        data = self.dict(by_alias=True, exclude_none=True)
        key = data.pop('key')
        return {"key": str(key), "data": data}

    @root_validator(pre=True, allow_reuse=True)
    def set_key(cls, values: dict) -> dict:
        return {k: (v.key if isinstance(v, Leaf) else v) for k, v in values.items()}

    def __hash__(self) -> int:
        return hash(tuple([self.__dict__.get(attr) if not isinstance(self.__dict__.get(attr), list)
                                   else tuple(self.__dict__.get(attr)) for attr in self.hash_attrs]))


# serialization & deserialization
class Serializer(BaseModel, ABC):

    @abstractmethod
    def to_dict(self):
        pass

    @abstractmethod
    def to_json(self, path: Union[Path, str]) -> None:
        pass


class DeSerializer(BaseModel, ABC):

    @abstractmethod
    def load(self, path: Path, **kwargs) -> None:
        pass


from metagen.register import register
from metagen.utils import check_path, create_file, open_json, UUIDEncoder


class JSONSerializer(Serializer):
    structure: dict = Field(default={})

    def to_dict(self) -> dict:
        for _, element in register.hashs.items():
            nodes = element.__nodes__().split('.')
            self.set_node(self.structure, nodes, element)
        return self.structure

    def set_node(self, structure: dict, nodes: list, element: Leaf):
        node = nodes.pop(0)
        if len(nodes) > 0:
            if not structure.get(node):
                structure[node] = {}
            self.set_node(structure[node], nodes, element)
        else:
            if not structure.get(node):
                structure[node] = []
            structure[node].append(element.to_dict())

    def to_json(self, path: Union[Path, str]) -> None:
        structure = self.to_dict()

        path = check_path(path)

        if not path.parent:
            create_file(path.parent)

        with open(path, 'w') as file:
            json.dump(structure, file, indent=6, cls=UUIDEncoder)


from metagen.elements import ElementFactory, element_factory


class JSONDeserializer(DeSerializer):
    factory: ElementFactory = element_factory

    def load(self, path: Path, encoding='utf8') -> None:

        path = check_path(path)

        obj = open_json(path, encoding)

        for node, structure in obj.items():
            self._parse(node, structure)

    def _parse(self, nodes: str, obj: Union[dict, list]) -> None:

        if isinstance(obj, dict):
            for node, structure in obj.items():
                self._parse(f'{nodes}.{node}', structure)
        elif isinstance(obj, list):
            for data in obj:
                self.factory.create_element(nodes, data)


class Generator(BaseModel):
    serializer: Serializer = Field(default=JSONSerializer())
    deserializer: DeSerializer = Field(default=JSONDeserializer())

    def load_fixtures(self, path: Path, encoding='utf8') -> None:
        self.deserializer.load(path, encoding=encoding)

    def to_dict(self) -> dict:
        return self.serializer.to_dict()

    def to_json(self, path: Path) -> None:
        self.serializer.to_json(path)

    def get_element_by_nameInternal(self, name: str) -> LeafABC:
        """Return element of given nameInternal"""
        if self.register.get_by_name(name):
            return register.get_by_name(name)
        else:
            raise ValueError(f'Element with nameInternal {name} did not find')

    def get_element_by_uuid(self, uuid: str) -> LeafABC:
        """Return element of given uuid"""
        if self.register.get_by_uuid(uuid):
            return register.get_by_name(uuid)
        else:
            raise ValueError(f'Element with uuid {uuid} did not find')

    @property
    def register(self):
        return register

    def get_elements_by_type(self, element: Leaf) -> List[Leaf]:
        """Return list of all elements of given element type"""
        return [v for k, v in self.register.name.items() if isinstance(v, element.__wrapped__)]

    def get_elements_by_name(self, name: str) -> List[Leaf]:
        """Return list of elements that internal name contains part of input string"""
        return [v for k, v in self.register.name.items() if k.__contains__(name)]
