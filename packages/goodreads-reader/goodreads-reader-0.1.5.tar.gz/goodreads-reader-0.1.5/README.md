# Goodreads Reader
A smalls scraper for getting Goodreads data

### Installation
```
pip install goodreads-reader
```

### Get started
How to read all books for a user:

```Python
from goodreads_reader import Reader

R = Reader(1)
R.get_books_list()

