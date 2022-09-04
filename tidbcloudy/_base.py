from enum import Enum
from typing import Callable

from tidbcloudy.context import Context


class TiDBCloudyContextualBase:
    __slots__ = ["_context"]

    def __init__(self, context: Context, **kwargs):
        self._context = context
        super().__init__(**kwargs)

    @property
    def context(self):
        return self._context


class TiDBCloudyBase:
    _keys = None

    def __init_subclass__(cls):
        cls._keys = {}
        for key in cls.__slots__:
            key = key.removeprefix("_")
            cls._keys[key] = getattr(cls, key)

    def __init__(self, **kwargs):
        for key in self._keys:
            setattr(self, key, kwargs.pop(key, None))
        super().__init__(**kwargs)

    @classmethod
    def from_object(cls, context: Context = None, obj: dict = None):
        # Add context argument, and raise Exception when context is None
        #  and base class has TiDBCloudyContextualBase
        if issubclass(cls, TiDBCloudyContextualBase):
            if context is None:
                raise TypeError("context is None")
            inst = cls(context=context)
        else:
            inst = cls()
        inst.assign_object(obj)
        return inst

    def assign_object(self, obj: dict):
        # In from_object, forward context argument when self is subclass of TiDBCloudyContextualBase
        #  and forward a None context argument when self is not subclass of TiDBCloudyContextualBase
        context = self._context if isinstance(self, TiDBCloudyContextualBase) else None
        for key, descriptor in self._keys.items():
            value = obj.get(key, None)
            if value is None:
                continue
            if isinstance(descriptor, TiDBCloudyListField):
                setattr(self, key, [descriptor.item_type.from_object(context, item) for item in value])
            elif issubclass(descriptor.value_type, TiDBCloudyBase):
                setattr(self, key, descriptor.value_type.from_object(context, value))
            else:
                assert isinstance(descriptor, TiDBCloudyField)
                if descriptor.convert_from is not None:
                    value = descriptor.convert_from(value)
                setattr(self, key, value)

    def to_object(self) -> dict:
        obj = {}
        for key, descriptor in self._keys.items():
            value = getattr(self, key)
            if isinstance(descriptor, TiDBCloudyListField):
                if value is None:
                    value = []
                else:
                    value = [item.to_object() for item in value]
            else:
                assert isinstance(descriptor, TiDBCloudyField)
                if value is None and descriptor.none_is_empty:
                    continue
                if issubclass(descriptor.value_type, TiDBCloudyBase):
                    value = value.to_object()
                else:
                    if descriptor.convert_to is not None:
                        value = descriptor.convert_to(value)
            obj[key] = value
        return obj


class TiDBCloudyField:
    def __init__(self, value_type, convert_from: Callable = None, convert_to: Callable = None, none_is_empty=True):
        self._public = None
        self._private = None
        self.value_type = value_type
        self.convert_from = convert_from
        self.convert_to = convert_to
        self.none_is_empty = none_is_empty

        if issubclass(self.value_type, Enum):
            if self.convert_from is None:
                self.convert_from = lambda x: self.value_type(x.upper())
            if self.convert_to is None:
                self.convert_to = lambda x: x.value

    def __set_name__(self, owner, name):
        self._public = name
        self._private = "_" + name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self._private, None)

    def __set__(self, instance, value):
        setattr(instance, self._private, value)


class TiDBCloudyListField:
    def __init__(self, item_type):
        self._public = None
        self._private = None
        self.item_type = item_type

    def __set_name__(self, owner, name):
        self._public = name
        self._private = "_" + name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self._private)

    def __set__(self, instance, value):
        setattr(instance, self._private, value)
