from Models.Settings import Settings
from view.utils.FileManager import write_to_json_file


if __name__ == '__main__':
    settings = Settings()
    jsonStr = settings.to_json()
    print(jsonStr)
    tester = Settings.from_json(jsonStr)
    print(tester)
    write_to_json_file(data=jsonStr, filename="../repo/settings.json")

