#!/bin/bash

BOOKFILE="book_links_PDF.txt"

idx=1
while read book; do
        echo $book
        curl -o $idx $book
        idx=$(( $idx +1 ))
done <$BOOKFILE
