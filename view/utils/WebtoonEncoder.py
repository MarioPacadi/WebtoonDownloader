import importlib
import json

from Models.WebtoonDownloader import WebtoonsDownloader


class WebtoonEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__dict__'):
            # Include class name and object attributes in the JSON representation
            return {
                '__class__': obj.__class__.__name__,
                '__module__': obj.__module__,
                **obj.__dict__
            }
        return super().default(obj)


def webtoon_decoder(obj):
    if '__class__' in obj:
        class_name = obj.pop('__class__')
        module_name = obj.pop('__module__', None)

        # Import the module dynamically
        module = __import__(module_name, fromlist=[class_name])

        class_ = getattr(module, class_name)
        instance = class_.__new__(class_)
        instance.__dict__.update(obj)
        return instance
    return obj


class WebtoonsListEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, list):
            # Serialize the list of objects with class information
            return [WebtoonEncoder().default(item) for item in obj]
        return super().default(obj)


def webtoons_list_decoder(obj):
    if isinstance(obj, list):
        # Deserialize the list of objects
        return [webtoon_decoder(item) for item in obj]
    return obj
