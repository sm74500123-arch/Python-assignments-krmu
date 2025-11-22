# main.py

from library_manager.inventory import LibraryInventory
from library_manager.book import Book

def menu():
    print("\n===== Library Inventory Manager =====")
    print("1. Add Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. View All Books")
    print("5. Search Book")
    print("6. Exit")
    return input("Choose an option: ")

def run():
    inventory = LibraryInventory()

    while True:
        choice = menu()

        try:
            if choice == "1":
                title = input("Enter title: ")
                author = input("Enter author: ")
                isbn = input("Enter ISBN: ")

                book = Book(title, author, isbn)
                inventory.add_book(book)
                print("Book added!")

            elif choice == "2":
                isbn = input("Enter ISBN to issue: ")
                book = inventory.search_by_isbn(isbn)
                if book and book.issue():
                    inventory.save_to_file()
                    print("Book issued!")
                else:
                    print("Book not available.")

            elif choice == "3":
                isbn = input("Enter ISBN to return: ")
                book = inventory.search_by_isbn(isbn)
                if book and book.return_book():
                    inventory.save_to_file()
                    print("Book returned!")
                else:
                    print("Invalid return action.")

            elif choice == "4":
                for b in inventory.display_all():
                    print(b)

            elif choice == "5":
                t = input("Search title: ")
                results = inventory.search_by_title(t)
                for r in results:
                    print(r)
                if not results:
                    print("No matching books found.")

            elif choice == "6":
                print("Goodbye!")
                break

            else:
                print("Invalid option. Try again.")

        except Exception as e:
            print("An error occurred.")
            print(e)

if __name__ == "__main__":
    run()
 