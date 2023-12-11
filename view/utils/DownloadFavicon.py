import requests
import favicon


def download_favicon(url, save_path='favicon.ico'):
    user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/35.0.1916.47 Safari/537.36')
    headers = {'User-Agent': user_agent}
    # Get the favicon URL from the provided website
    favicon_url = favicon.get(url, headers=headers, timeout=2)

    if favicon_url:
        # Download the favicon
        icon = favicon_url[0]
        response = requests.get(icon.url, stream=True)
        with open(f"{save_path}.{icon.format}", 'wb') as image:
            for chunk in response.iter_content(1024):
                image.write(chunk)

        print(f"Favicon downloaded: {icon.url}")
    else:
        print("No favicon found for the provided URL.")



# Example usage
website_url = 'https://reapercomics.com/'
download_favicon(website_url, "D:\\Projects_and_Tasks\\Personal Projects\\WebtoonDownloader\\assets\\reaperscans")
