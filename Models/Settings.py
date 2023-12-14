from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Settings:
    # driver_path: str = "D:/Program Files (x86)/chromedriver-win64/chromedriver.exe"
    driver_path: str = r"D:\Program Files (x86)\chrome-headless-shell-win64\chrome-headless-shell.exe"
    browser_path: str = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
    run_in_incognito: bool = True
    user_agent: str = ("Mozilla/5.0 (Android 13.0.0; ) AppleWebKit/537.36 (KHTML, like Gecko) Brave/119 Chrome/119 "
                       "Not?A_Brand/24 Mobile Safari/537.36")
