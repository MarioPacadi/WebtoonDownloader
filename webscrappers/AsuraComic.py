from bs4 import BeautifulSoup
import logging

from Models.WebtoonDownloader import WebtoonsDownloader


class AsuraComic(WebtoonsDownloader):

    def _parse_html(self, html_content):
        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # folder_name = f"Chapter {str(self.current_chapter).zfill(2)}"
            # <button class=" px-3 py-2 dropdown-btn"> <h2 class="text-[#9B9B9B] text-[13px] whitespace-nowrap max-[350px]:truncate">Chapter 160</h2></button>
            folder_element = soup.find('button', class_='px-3 py-2 dropdown-btn').find('h2')
            if folder_element:
                chap = folder_element.get_text().strip().replace(f"{self.name} ", "")
                folder_name = self._clean_folder_name(chap)
            else:
                folder_name = f"Chapter {str(self.current_chapter).zfill(2)}"

            # <div class="py-8 -mx-5 md:mx-0 flex flex-col items-center justify-center">/div>
            div_el = soup.find('div', class_='py-8 -mx-5 md:mx-0 flex flex-col items-center justify-center')
            if div_el:
                # <img src=".webp" class="object-cover mx-auto" alt="chapter page">
                img_els = div_el.find_all(name='img', class_='object-cover mx-auto')
                image_links = [img['src'] for img in img_els if
                               self._is_valid_image_link(img.get('src'))]
            else:
                image_links = []

            next_url = self._find_next_url(soup, "ch-next-btn")

            base_url = "https://asuracomic.net"
            next_url = None
            for next_button in soup.find_all('a', href=True):
                if next_button and next_button.find('h2', text='Next'):
                    next_url = next_button['href']
                    if not next_url.startswith('http'):
                        next_url = base_url + next_url

            return image_links, next_url, folder_name
        except Exception as e:
            print(f"An error occurred during parsing: {e}")
            return None, None, None
