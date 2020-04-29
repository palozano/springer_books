#!/bin/bash

BOOKFILE="book_links_PDF.txt"
BOOKFOLDER="PDFs"

mkdir "$BOOKFOLDER"

idx=1
while read book; do
        echo $book
        curl -o $BOOKFOLDER/$idx $book
        idx=$(( $idx +1 ))
done <$BOOKFILE
