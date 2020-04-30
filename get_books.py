import urllib.request
from bs4 import BeautifulSoup
import requests
import os
import shutil
from tqdm import tqdm

class Downloader:

    page_links = "book_links_to_parse.txt"
    pdf_links = "book_links_PDF.txt"
    epub_links = "book_links_EPUB.txt"

    pdf_directory = "PDFs"
    epub_directory = "EPUBs"

    def get_files(self):
        with open(self.page_links) as f:
            page_links_list = f.read().splitlines()

        with open(self.pdf_links) as f:
            pdf_links_list = f.read().splitlines()

        with open(self.epub_links) as f:
            epub_links_list = f.read().splitlines()

        for directory in [self.pdf_directory, self.epub_directory]:
            if not os.path.exists(directory):
                os.makedirs(directory)

        return page_links_list, pdf_links_list, epub_links_list

    def download_books(self, page_links, book_links, book_directory):
        flag_type = "PDFs" if book_directory == self.pdf_directory else "EBOOKs"
        print("\nDownloading {}...".format(flag_type))

        pbar = tqdm(total=len(book_links))

        for link_book, link_page in zip(book_links, page_links):
            pageWebUrl = urllib.request.urlopen(link_page)
            response = pageWebUrl.read()

            soup = BeautifulSoup(response, 'html.parser')
            name_box = soup.find('div', attrs={'class': 'page-title'})
            name = name_box.text[1:-1].replace('\n',' - ')

            try:
                bookWebUrl = urllib.request.urlopen(link_book)
                file_extension = "pdf" if book_directory == self.pdf_directory else "epub"
                with open('{}/{}.{}'.format(book_directory, name, file_extension), 'wb') as file_name:
                    req = requests.get(bookWebUrl.url)
                    file_name.write(req.content)

            except Exception:
                # print("\tCannot find {}.".format(name))
                # print("\tMaybe it doesn't have an EPUB format.")

            pbar.update(1)
        pbar.close()

    def download(self):
        page_links_list, pdf_links_list, epub_links_list = self.get_files()
        self.download_books(page_links_list, pdf_links_list, self.pdf_directory)
        self.download_books(page_links_list, epub_links_list, self.epub_directory)


if __name__=="__main__":
    downloader = Downloader()
    downloader.download()

