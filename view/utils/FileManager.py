import importlib
import json
import os

from Models.WebtoonDownloader import WebtoonsDownloader
from view.utils.WebtoonEncoder import webtoon_decoder


def import_classes_from_directory_of_subclass_webtoons_downloader(directory):
    class_instances = []

    # Loop through all files in the directory
    for file_name in os.listdir(directory):
        if file_name.endswith('.py'):
            module_name = f"{os.path.basename(directory)}.{file_name[:-3]}"  # Combine directory name and file name
            # print(module_name)

            # Import the module dynamically
            module = importlib.import_module(module_name)

            # Find all classes in the module that inherit from WebtoonsDownloader
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (
                        isinstance(attr, type) and
                        issubclass(attr, WebtoonsDownloader) and
                        attr is not WebtoonsDownloader  # Exclude the abstract class itself
                ):
                    class_instances.append(attr())

    return class_instances


def import_classes_from_directory(directory: str):
    class_instances = []

    # Loop through all files in the directory
    for file_name in os.listdir(directory):
        if file_name.endswith('.py'):
            class_name = file_name[:-3]
            module_name = f"{os.path.basename(directory)}.{class_name}"  # Combine directory name and file name
            # print(module_name)
            module_path = os.path.join(directory, file_name)

            # Import the module dynamically
            module = importlib.import_module(module_name)

            class_ = getattr(module, class_name)
            if isinstance(class_, type):
                class_instances.append(class_)

            # Find allclasses in the module
            # for attr_name in dir(module):
            #     attr = getattr(module, attr_name)
            #     if isinstance(attr, type):
            #         class_instances.append(attr())

    return class_instances


def get_image_files_in_directory(directory):
    """
    Get a list of image files in a directory.

    Parameters:
    - directory: The directory path to search for image files.

    Returns:
    - A list of image files in the directory.
    """
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.ico'}  # Add more if needed
    image_files = []

    for file in os.listdir(directory):
        _, ext = os.path.splitext(file)
        if ext.lower() in image_extensions:
            image_files.append(file)

    return image_files


def file_exists_in_directory(directory, file_name: str):
    """
    Check if a file with a specific name exists in a directory.

    Parameters:
    - directory: The directory path to search for the file.
    - file_name: The name of the file (without the extension).

    Returns:
    - True if the file exists, False otherwise.
    """
    for file in os.listdir(directory):
        base, ext = os.path.splitext(file)
        if base.lower() == file_name.lower():
            return os.path.join(directory, file)
    return None


def read_from_json_file(filename='data.json', decoder=None):
    with open(filename, 'r+', encoding='utf-8') as f:
        return json.load(f, object_hook=decoder)


def write_to_json_file(data, filename='data.json', encoder=None):
    with open(filename, 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4, cls=encoder)