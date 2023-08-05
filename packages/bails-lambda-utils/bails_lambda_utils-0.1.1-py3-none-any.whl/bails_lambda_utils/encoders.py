import json
import datetime
import re


class ModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "attribute_values"):
            return ModelEncoder.transform_object(
                obj.attribute_values,
                obj.get_legacy_fields() if hasattr(obj, "get_legacy_fields") else {},
            )
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

    @staticmethod
    def transform_object(obj, extra_attributes):
        new_obj = {}
        for key in obj:
            new_obj[ModelEncoder.transform_key(key)] = obj[key]
        return {**new_obj, **extra_attributes}

    @staticmethod
    def transform_key(key):
        return re.sub(r"(?!^)_([a-zA-Z])", lambda m: m.group(1).upper(), key)
