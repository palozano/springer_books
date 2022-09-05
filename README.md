Springer is giving out free books. Go get them.

## Usage
You can use `make`, `make <TYPE>`, `python <SCRIPT>`, or run the bash script yourself.

### Option 1
Just run `make` if you want everything tidy and are lazy.

This runs the Python script and downloads every free document into folders, naming everything.

### Option 2
Run the python script as `$ python get_books.py` to download both PDFs and Ebooks, if you don't know what `make` is.

This will name every file and separate them in folders.

### Option 3
To download the files without names (just the ID numbers from Springer), first do `$ chmod +x get_books_XXX.sh`, then run the individual script(s) `./get_books_XXX.sh`.

You can also use `make pdfs` and/or `make epubs` to do the above.

