import urllib.request
from bs4 import BeautifulSoup
import requests
import os
import shutil

class Downloader:

    # Files
    links = "links.txt"
    page_links = "book_links_to_parse.txt"
    pdf_links = "book_links_PDF.txt"
    epub_links = "book_links_EPUB.txt"

    # Folders
    pdf_directory = "PDFs"
    epub_directory = "EPUBs"

    def get_urls(self):
        # Lo que mando el mago no son los links como tal
        # sino que el link esta dentro de una linea de texto.
        # Yo he usado Vim para limpiarlos con una macro.

        # Ademas, esos links no son los links de los PDF,
        # sino que es un link que dirige a la pagina de 
        # Springer donde aparece el libro.

        # Para obtener esos links buenos, priemro carga
        # los links "limpios". Leelos y quita espacios que sobren:
        try:
            links_file = self.links
        except:
            print("No se encuentra {}".format(self.links))

        with open(links_file) as f:
            content_links = f.read().splitlines()

        # Crea una lista vacia para almacenar los links buenos:
        books_links_to_parse = list()

        # Conectate al link y obten la URL a la que te redirecciona
        for link in content_links:
            webUrl = urllib.request.urlopen(link)
            books_links_to_parse.append(webUrl.url)

        # Almacenalos en un archivo
        with open(self.page_links, 'w') as f:
            for item in books_links_to_parse:
                f.write("{}\n".format(item))

    def get_files(self):
        # El archivo book_links_to_parse.txt tiene el link de la
        # pagina donde aparecen los botones que tienen el PDF y 
        # el EPUB.
        # El link de cada archivo es casi igual que el de ese
        # archivo, salvo por una diferencia en la URL:
        #    Para los PDF, cambia: book --> content/pdf
        #    Para los EPUB, cambia: book --> download/epub

        # Yo he triplicado el archivo book_links_to_parse.txt
        # para modificarlo y tener los links de la pagina, del PDF
        # y del EPUB, para cada uno de los libros.

        with open(self.page_links) as f:
            page_links_list = f.read().splitlines()

        with open(self.pdf_links) as f:
            pdf_links_list = f.read().splitlines()

        with open(self.epub_links) as f:
            epub_links_list = f.read().splitlines()

        # Crea carpetas para tenerlo mas organizado
        for directory in [self.pdf_directory, self.epub_directory]:
            if not os.path.exists(directory):
                os.makedirs(directory)

        return page_links_list, pdf_links_list, epub_links_list

    def download_books(self, page_links, book_links, book_directory):
        # Ahora, vamos a decargar los archivos.
        # Como el PDF no viene con nombre (o yo no se sacarlo),
        # lo que voy a hacer es sacarlo de la pagina.

        flag_type = "PDFs" if book_directory == self.pdf_directory else "EBOOKs"
        print("\nDescargando {}...".format(flag_type))

        # Iteramos sobre todos las paginas de los libros/PDF
        for idx, (link_book, link_page) in enumerate(zip(book_links, page_links)):
            # Muestra progreso
            print("Descargando {} de 408".format(idx+1))
            # Primero abrimos la URL de la pagina
            pageWebUrl = urllib.request.urlopen(link_page)
            # Leemos la pagina (devuelve el html entero)
            response = pageWebUrl.read()
            # Parseamos lo que hemos leido suponiendo que es HTML
            soup = BeautifulSoup(response, 'html.parser')
            # Para obtener el nombre del libro, usamos el inspector web
            # hasta dar con el elemento del titulo qur tiene el nombre
            # del libro.
            name_box = soup.find('div', attrs={'class': 'page-title'})
            # Se limpia antes
            name = name_box.text[1:-1].replace('\n',' - ')
            # Ahora abrimos la URL del documento (pdf/ebook)
            # request = urllib2.Request(link_book, postBackData)
            try:
                bookWebUrl = urllib.request.urlopen(link_book)
                # Creamos un archivo para almacenar el PDF con el nombre
                if book_directory == self.pdf_directory:
                    file_extension = ".pdf"
                    with open('{}/{}.{}'.format(book_directory, name, file_extension), 'wb') as file_name:
                        # Obtenemos la web (que es el libro)
                        req = requests.get(bookWebUrl.url)
                        # Grabamos el contenido de la web
                        file_name.write(req.content)
                else:
                    request = requests.get(bookWebUrl, stream=True)
                    if request.status_code == 200:
                        with requests.get(bookWebUrl , stream=True) as req:
                            tmp_file = '{}/{}.pdf'.format(book_directory, name)
                            with open(tmp_file, 'wb') as out_file:
                                shutil.copyfileobj(req.raw, out_file)
                                out_file.close()

            except Exception:  # urllib.error.URLError=="HTTP Error 404: Not Found":
                print("\tNo se encuentra el documento {}...(snip).".format(name[:15]))
                print("\tQuizas no tenga ebook.")

    def download(self):
        page_links_list, pdf_links_list, epub_links_list = self.get_files()
        # self.download_books(page_links_list, pdf_links_list, self.pdf_directory)
        self.download_books(page_links_list, epub_links_list, self.epub_directory)


if __name__=="__main__":
    downloader = Downloader()
    downloader.download()


