from abc import ABC, abstractmethod
from functools import wraps
from uuid import UUID
from warnings import warn

from metagen.base import LeafABC
from pydantic import BaseModel, Field


class ElementRegister(BaseModel, ABC):

    @abstractmethod
    def add(self, element: BaseModel) -> None:
        pass

    @abstractmethod
    def check_register(self, obj: BaseModel) -> bool:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> LeafABC:
        pass

    @abstractmethod
    def get_by_hash(self, hash: int) -> LeafABC:
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: UUID) -> LeafABC:
        pass


# register
class Register(BaseModel):
    hashs: dict = Field(default_factory=dict)
    uuid: dict = Field(default_factory=dict)
    name: dict = Field(default_factory=dict)

    def add(self, element: BaseModel) -> None:
        if not self.check_register(element):
            self.hashs.update({hash(element): element})
            self.uuid.update({element.key: element})
            self.name.update({element.nameInternal: element})
        else:
            raise ValueError(f'PTR element "{element.__class__.__name__}" with nameInternal: {element.nameInternal}, '
                             f'key: {element.key} and hash: {hash(element)} already exist')

    def check_register(self, obj: BaseModel) -> bool:
        return all([self.hashs.get(hash(obj)), self.name.get(obj.nameInternal)])

    def get_by_name(self, name: str) -> LeafABC:
        return self.name.get(name)

    def get_by_hash(self, hash: int) -> LeafABC:
        return self.hashs.get(hash)

    def get_by_uuid(self, uuid: str) -> LeafABC:
        if UUID(uuid):
            return self.uuid.get(uuid)


register = Register()


def exist_in_register(element):
    @wraps(element)
    def checkting_register(*args, **kwargs):
        instance = element(*args, **kwargs)
        if register.check_register(instance):
            registered_element = register.get_by_hash(hash(instance))
            warn(f'Element duplication: Element {instance.__class__.__name__} with parameters: '
                 f'{"; ".join([f"{k}: {v}" for k, v in kwargs.items()])} found in register. Element '
                 f'{registered_element.__repr__()} returned instead')
            return registered_element
        else:
            register.add(instance)
            return instance

    return checkting_register