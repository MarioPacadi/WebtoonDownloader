from uuid import UUID

from view.utils.FileManager import import_classes_from_directory_of_subclass_webtoons_downloader, \
    file_exists_in_directory
from webscrappers.AsuraScans import AsuraScans
from webscrappers.FlameScans import FlameScans
from webscrappers.MangaDemon import MangaDemon
from webscrappers.ReaperScans import ReaperScans

scrapper_directory_path = '../webscrappers'
images_directory_path = '../assets'


def get_all_webtoon_scrappers():
    all_class_instances = import_classes_from_directory_of_subclass_webtoons_downloader(scrapper_directory_path)
    return [type(instance).__name__ for instance in all_class_instances]


def get_icon_by_scrapper_name(scrapper_name) -> str:
    image_exists = file_exists_in_directory(images_directory_path, scrapper_name)
    return '../assets/ScraperPlaceholder.png' if not image_exists else image_exists


def get_webtoon_downloader(id_webtoon: UUID, webscrapper: str, name: str, url: str, save_to: str):
    all_class_instances = import_classes_from_directory_of_subclass_webtoons_downloader(scrapper_directory_path)
    print(webscrapper.lower())
    for instance in all_class_instances:
        scrapper_name = instance.__class__.__name__
        print(scrapper_name.lower())
        if webscrapper.lower() == scrapper_name.lower():
            instance.id_webtoon = id_webtoon
            instance.name = name
            instance.starting_url = url
            instance.folder_path = save_to
            instance.icon_path = get_icon_by_scrapper_name(scrapper_name)
            return instance

    return None

    # match webscrapper:
    #     case AsuraScans.__name__:
    #         return AsuraScans(starting_url=url,
    #                           folder_path=save_to, name=name, icon_path="../assets/AsuraScans.png")
    #     case ReaperScans.__name__:
    #         return ReaperScans(starting_url=url,
    #                            folder_path=save_to, name=name, icon_path="../assets/ReaperScans.png")
    #     case FlameScans.__name__:
    #         return FlameScans(starting_url=url,
    #                           folder_path=save_to, name=name, icon_path="../assets/FlameScans.png")
    #     case MangaDemon.__name__:
    #         return MangaDemon(starting_url=url,
    #                           folder_path=save_to, name=name, icon_path="../assets/MangaDemon.png")
