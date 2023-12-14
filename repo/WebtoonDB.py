from Models.WebtoonDownloader import WebtoonsDownloader
from view.utils.FileManager import read_from_json_file, write_to_json_file
from view.utils.WebtoonEncoder import webtoon_decoder, WebtoonEncoder

json_db_path = "./repo/webtoon_list.json"
json_settings_path = "./repo/settings.json"


def add_data_to_json_file(data: list, filename='data.json', decoder=webtoon_decoder, encoder=WebtoonEncoder):
    old_data: list = read_from_json_file(filename, decoder=decoder)
    for webtoon in data:
        old_data.append(webtoon)
    write_to_json_file(old_data, filename=filename, encoder=encoder)


def read_data_from_json_file(filename='data.json', decoder=webtoon_decoder):
    webtoon_list: list = read_from_json_file(filename, decoder=decoder)
    return webtoon_list


def update_data_of_json_file(update_target: WebtoonsDownloader,
                             filename='data.json',
                             decoder=webtoon_decoder,
                             encoder=WebtoonEncoder):
    old_data: list = read_from_json_file(filename, decoder=decoder)
    print(old_data)
    print(update_target.id_webtoon)
    old_webtoon: WebtoonsDownloader
    for old_webtoon in old_data:
        if old_webtoon.id_webtoon == update_target.id_webtoon:
            old_data.remove(old_webtoon)
            old_data.append(update_target)
            break
    write_to_json_file(old_data, filename=filename, encoder=encoder)
