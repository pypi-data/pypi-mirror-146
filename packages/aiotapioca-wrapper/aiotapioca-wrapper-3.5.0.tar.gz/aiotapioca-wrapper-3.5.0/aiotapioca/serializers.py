import arrow
from decimal import Decimal

from pydantic import BaseModel


class BaseSerializer:
    def deserialize(self, method_name, value, **kwargs):
        if hasattr(self, method_name):
            return getattr(self, method_name)(value, **kwargs)
        raise NotImplementedError("Desserialization method not found")

    def serialize_dict(self, data):
        serialized = {}

        for key, value in data.items():
            serialized[key] = self.serialize(value)

        return serialized

    def serialize_list(self, data):
        serialized = []
        for item in data:
            serialized.append(self.serialize(item))

        return serialized

    def serialize(self, data):
        data_type = type(data).__name__

        serialize_method = ("serialize_" + data_type).lower()
        if hasattr(self, serialize_method):
            return getattr(self, serialize_method)(data)

        return data


class SimpleSerializer(BaseSerializer):
    def to_datetime(self, value):
        return arrow.get(value).datetime

    def to_decimal(self, value):
        return Decimal(value)

    def serialize_decimal(self, data):
        return str(data)

    def serialize_datetime(self, data):
        return arrow.get(data).isoformat()


class PydanticSerializer(BaseSerializer):
    def to_pydantic(self, data, model=None):
        if not model:
            raise ValueError(
                """
                The model parameter is not specified in the resource mapping
                or is not passed as a function parameter.
                """
            )
        if isinstance(data, str):
            serialized = model.parse_raw(data)
        else:
            serialized = model.parse_obj(data)
        return serialized

    def serialize_pydantic(self, data):
        results = data.dict()
        if "__root__" in results:
            return results["__root__"]
        return results

    def serialize(self, data):
        if isinstance(data, BaseModel):
            data = self.serialize_pydantic(data)
        return super().serialize(data)
