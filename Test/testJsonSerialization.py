from webscrappers.ReaperScans import ReaperScans


if __name__ == '__main__':
    downloader = ReaperScans(
        "https://reapercomics.com/comics/5150-sss-class-suicide-hunter/chapters/14091450-chapter-105",
        "D:/Webtoons/SSS-Class Suicide Hunter")  # Replace with actual URL
    jsonStr = downloader.to_json()
    print(jsonStr)
    tester = ReaperScans.from_json(jsonStr)
    print(tester)

