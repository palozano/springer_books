.PHONY : message_all message_EPUBs message_PDFs python pdfs epubs clean all

all: python

message_all:
	@echo "Downloading PDFs and EPUBs..."

message_PDFs:
	@echo "Downloading only PDFs..."

message_EPUBs:
	@echo "Downloading only EPUBs..."

python: message_all
	@python get_books.py
	@clean

pdfs: message_PDFs
	@./get_books_PDF.sh

epubs: message_EPUBs
	@./get_books_EPUB.sh

clean:
	@rm -rf __pycache__