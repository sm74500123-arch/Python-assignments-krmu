# inventory.py

import json
import logging
from pathlib import Path
from .book import Book

logging.basicConfig(
    filename="library.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class LibraryInventory:
    def __init__(self, file_path="data/catalog.json"):
        self.file_path = Path(file_path)
        self.books = []
        self.load_from_file()

    def load_from_file(self):
        try:
            if not self.file_path.exists():
                self.file_path.parent.mkdir(exist_ok=True)
                self.file_path.write_text("[]")

            with open(self.file_path, "r") as f:
                data = json.load(f)
                self.books = [Book(**book) for book in data]

        except Exception as e:
            logging.error(f"Failed loading file: {e}")
            self.books = []

    def save_to_file(self):
        try:
            with open(self.file_path, "w") as f:
                json.dump([book.to_dict() for book in self.books], f, indent=4)
        except Exception as e:
            logging.error(f"Error writing file: {e}")

    def add_book(self, book: Book):
        self.books.append(book)
        self.save_to_file()
        logging.info(f"Book added: {book.title}")

    def search_by_title(self, title):
        return [b for b in self.books if title.lower() in b.title.lower()]

    def search_by_isbn(self, isbn):
        return next((b for b in self.books if b.isbn == isbn), None)

    def display_all(self):
        return self.books
