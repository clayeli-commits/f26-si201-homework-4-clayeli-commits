# SI 201 HW4 (Library Checkout System)
# Your name: Elijah Caybrook
# Your student id: 24041260
# Your email: caybrook@umich.edu
# Who or what you worked with on this homework (including generative AI like ChatGPT):
# If you worked with generative AI also add a statement for how you used it.
# e.g.:
# Asked ChatGPT for hints on debugging and for suggestions on overall code structure
#
# Did your use of GenAI on this assignment align with your goals and guidelines in your Gen AI contract? If not, why?
#
# --- ARGUMENTS & EXPECTED RETURN VALUES PROVIDED --- #
# --- SEE INSTRUCTIONS FOR FULL DETAILS ON METHOD IMPLEMENTATION --- #

import unittest


class Book:
    def __init__(self, book_id, title, author):
        '''
        ARGUMENTS:
            self: the current object
            book_id: an integer representing the unique ID of the book
            title: a string representing the book's title
            author: a string representing the book's author

        RETURNS: None
        '''
        self.book_id = book_id
        self.title = title
        self.author = author
        self.is_checked_out = False
        self.checkout_history = []

    def __str__(self):
        '''
        ARGUMENTS:
            self: the current object

        RETURNS: a string
        '''
        return f'Book {self.book_id}: "{self.title}" by {self.author}'

    def has_been_borrowed_by(self, patron_id):
        '''
        ARGUMENTS:
            self: the current object
            patron_id: an integer representing a patron's unique ID

        RETURNS: a Boolean value (True or False)
        '''
        for patron in self.checkout_history:
            if patron.patron_id == patron_id:
                return True
        return False


class Patron:
    def __init__(self, patron_id, name):
        '''
        ARGUMENTS:
            self: the current object
            patron_id: an integer representing the patron's unique ID
            name: a string representing the patron's name

        RETURNS: None
        '''
        self.patron_id = patron_id
        self.name = name
        self.checked_out_books = []

    def __str__(self):
        '''
        ARGUMENTS:
            self: the current object

        RETURNS: a string
        '''
        return f'Patron {self.patron_id}: {self.name}'


class Library:
    def __init__(self, name):
        '''
        ARGUMENTS:
            self: the current object
            name: a string representing the name of the library

        RETURNS: None
        '''
        self.name = name
        self.books = []
        self.patrons = []
        self.transaction_log = []  # list of tuples: (action, patron_id, book_id, status)

    def __str__(self):
        '''
        ARGUMENTS:
            self: the current object

        RETURNS: a string
        '''
        return f'{self.name} has {len(self.books)} books and {len(self.patrons)} members.'

    def add_book(self, book):
        '''
        ARGUMENTS:
            self: the current object
            book: a Book object

        RETURNS: a Boolean value (True or False) indicating whether the book was added
        '''
        for existing_book in self.books:
            if existing_book.book_id == book.book_id:
                return False
        self.books.append(book)
        return True

    def add_patron(self, patron):
        '''
        ARGUMENTS:
            self: the current object
            patron: a Patron object

        RETURNS: a Boolean value (True or False) indicating whether the patron was added
        '''
        for existing_patron in self.patrons:
            if existing_patron.patron_id == patron.patron_id:
                return False
        self.patrons.append(patron)
        return True

    def checkout_book(self, patron_id, book_id):
        '''
        ARGUMENTS:
            self: the current object
            patron_id: integer representing the patron’s ID
            book_id: integer representing the book’s ID

        RETURNS: a Boolean value (True or False)
        '''

        # TODO: Implement checkout logic following the instructions
        # ==============================
        
        patron = next((p for p in self.patrons if p.patron_id == patron_id), None)
        if patron is None:
            self.transaction_log.append(("checkout", patron_id, book_id, "not_found"))
            return False

        book = next((b for b in self.books if b.book_id == book_id), None)
        if book is None:
            self.transaction_log.append(("checkout", patron_id, book_id, "not_found"))
            return False

        if book.is_checked_out:
            self.transaction_log.append(("checkout", patron_id, book_id, "unavailable"))
            return False

        # Check patron checkout limit
        if len(patron.checked_out_books) >= 4:
            self.transaction_log.append(("checkout", patron_id, book_id, "at_limit"))
            return False

        # Perform checkout operations
        patron.checked_out_books.append(book)
        book.checkout_history.append(patron)
        book.is_checked_out = True
        self.transaction_log.append(("checkout", patron_id, book_id, "success"))
        return True
        
        # ==============================

    def return_book(self, patron_id, book_id):
        '''
        ARGUMENTS:
            self: the current object
            patron_id: integer representing the patron’s ID
            book_id: integer representing the book’s ID

        RETURNS: a Boolean value (True or False)
        '''

        # TODO: Implement return logic following the instructions
        # ==============================
        
        patron = next((p for p in self.patrons if p.patron_id == patron_id), None)
        if patron is None:
            self.transaction_log.append(("return", patron_id, book_id, "not_found"))
            return False

        book = next((b for b in self.books if b.book_id == book_id), None)
        if book is None:
            self.transaction_log.append(("return", patron_id, book_id, "not_found"))
            return False

        if book not in patron.checked_out_books:
            self.transaction_log.append(("return", patron_id, book_id, "not_checked_out"))
            return False

        patron.checked_out_books.remove(book)
        book.is_checked_out = False
        self.transaction_log.append(("return", patron_id, book_id, "success"))
        return True

        # ==============================

    def count_successful_checkouts(self):
        '''
        ARGUMENTS:
            self: the current object

        RETURNS:
            a dictionary mapping each patron_id to the number of times that
            patron has successfully checked out a book
        '''
        # TODO: Implement count_successful_checkouts() following the instructions
        # ==============================

        counts = {}
        for action, patron_id, book_id, status in self.transaction_log:
            if action == "checkout" and status == "success":
                counts[patron_id] = counts.get(patron_id, 0) + 1
        return counts

        # ==============================

    # Extra Credit
    def return_all_books(self, patron_id):
        '''
        ARGUMENTS:
            self: the current object
            patron_id: integer representing the patron’s ID

        RETURNS: a Boolean value (True or False)
        '''

        # TODO (bonus): implement return_all_books() method following the instructions
        # ==============================
        # YOUR CODE STARTS HERE
        # ==============================
        pass
        # ==============================
        # YOUR CODE ENDS HERE
        # ==============================


class TestAllMethods(unittest.TestCase):

    def setUp(self):
        self.library = Library("Ann Arbor District Library")

        self.book1 = Book(101, "The Hobbit", "J.R.R. Tolkien")
        self.book2 = Book(102, "Pride and Prejudice", "Jane Austen")
        self.book3 = Book(103, "1984", "George Orwell")
        self.book4 = Book(104, "Beloved", "Toni Morrison")
        self.book5 = Book(105, "Frankenstein", "Mary Shelley")

        self.patron1 = Patron(1, "Alice")
        self.patron2 = Patron(2, "Bob")
        self.patron3 = Patron(3, "Charlie")

        self.library.add_book(self.book1)
        self.library.add_book(self.book2)
        self.library.add_book(self.book3)
        self.library.add_book(self.book4)
        self.library.add_book(self.book5)

        self.library.add_patron(self.patron1)
        self.library.add_patron(self.patron2)
        self.library.add_patron(self.patron3)

    def test_book_has_been_borrowed_by(self):
        self.assertFalse(self.book1.has_been_borrowed_by(1))
        self.assertTrue(self.library.checkout_book(1, 101))
        self.assertTrue(self.book1.has_been_borrowed_by(1))
        self.assertFalse(self.book1.has_been_borrowed_by(2))

    def test_library_add_book(self):
        new_book = Book(106, "Dune", "Frank Herbert")
        self.assertTrue(self.library.add_book(new_book))
        self.assertFalse(self.library.add_book(new_book))

    def test_library_add_patron(self):
        new_patron = Patron(4, "Dana")
        self.assertTrue(self.library.add_patron(new_patron))
        self.assertFalse(self.library.add_patron(new_patron))


    # test checkout_book
    def test_library_checkout_book_success(self):
        self.assertTrue(self.library.checkout_book(1, 101))
        self.assertIn(self.book1, self.patron1.checked_out_books)
        self.assertEqual(self.book1.checkout_history, [self.patron1])
        self.assertTrue(self.book1.is_checked_out)
        self.assertEqual(self.library.transaction_log[-1], ("checkout", 1, 101, "success"))

    def test_library_checkout_book_patron_does_not_exist(self):
        # Scenario: The patron does not exist in the library.
        self.assertFalse(self.library.checkout_book(999, 101))
        self.assertEqual(self.library.transaction_log[-1], ("checkout", 999, 101, "not_found"))
        self.assertFalse(self.book1.is_checked_out)

    def test_library_checkout_book_book_does_not_exist(self):
        # Scenario: The book does not exist in the library.
        self.assertFalse(self.library.checkout_book(1, 999))
        self.assertEqual(self.library.transaction_log[-1], ("checkout", 1, 999, "not_found"))

    def test_library_checkout_book_book_already_checked_out(self):
        # Scenario: The book is already checked out
        self.assertTrue(self.library.checkout_book(1, 101))
        self.assertFalse(self.library.checkout_book(2, 101))
        self.assertEqual(self.library.transaction_log[-1], ("checkout", 2, 101, "unavailable"))

        self.assertIn(self.book1, self.patron1.checked_out_books)
        self.assertNotIn(self.book1, self.patron2.checked_out_books)
        self.assertTrue(self.book1.is_checked_out)

    def test_library_checkout_book_patron_at_limit(self):
        # Scenario: Patron already has 4 books checked out.
        self.assertTrue(self.library.checkout_book(1, 101))
        self.assertTrue(self.library.checkout_book(1, 102))
        self.assertTrue(self.library.checkout_book(1, 103))
        self.assertTrue(self.library.checkout_book(1, 104))

        self.assertFalse(self.library.checkout_book(1, 105))
        self.assertEqual(self.library.transaction_log[-1], ("checkout", 1, 105, "at_limit"))

    # test return_book
    def test_library_return_book_log_success(self):
        self.assertTrue(self.library.checkout_book(2, 102))
        self.assertTrue(self.book2.is_checked_out)
        self.assertIn(self.book2, self.patron2.checked_out_books)
        self.assertTrue(self.library.return_book(2, 102))
        self.assertFalse(self.book2.is_checked_out)
        self.assertNotIn(self.book2, self.patron2.checked_out_books)
        self.assertEqual(self.library.transaction_log[-1], ("return", 2, 102, "success"))

    def test_library_return_book_patron_does_not_exist(self):
        # Scenario: The patron does not exist in the library.
        self.assertFalse(self.library.return_book(999, 101))
        self.assertEqual(self.library.transaction_log[-1], ("return", 999, 101, "not_found"))

    def test_library_return_book_book_does_not_exist(self):
        # Scenario: The book does not exist in the library.
        self.assertFalse(self.library.return_book(1, 999))
        self.assertEqual(self.library.transaction_log[-1], ("return", 1, 999, "not_found"))

    def test_library_return_book_not_checked_out_by_patron(self):
        # Scenario: The book was not checked out by the patron.
        # TODO: implement test_library_return_book_not_checked_out_by_patron() following the instructions
        # ==============================
        # YOUR CODE STARTS HERE
        # ==============================
        pass
        # ==============================
        # YOUR CODE ENDS HERE
        # ==============================

    # test count_successful_checkouts
    def test_count_successful_checkouts(self):
        self.assertTrue(self.library.checkout_book(1, 101))
        self.assertTrue(self.library.checkout_book(1, 102))
        self.assertTrue(self.library.return_book(1, 101))

        self.assertTrue(self.library.checkout_book(2, 101))

        counts = self.library.count_successful_checkouts()
        self.assertEqual(counts[1], 2)
        self.assertEqual(counts[2], 1)
        # Patron 3 made no successful checkouts, so patron 3 must not appear
        self.assertNotIn(3, counts)

    def test_count_successful_checkouts_no_successful_checkouts(self):
        self.assertFalse(self.library.checkout_book(1, 999))
        self.assertFalse(self.library.checkout_book(2, 888))

        counts = self.library.count_successful_checkouts()
        self.assertEqual(counts, {})

    # test return_all_books
    # TODO (bonus): Uncomment the following test cases when you are ready to test the return_all_books method
    # def test_return_all_books(self):
    #     self.library.checkout_book(1, 101)
    #     self.library.checkout_book(1, 102)

    #     self.assertTrue(self.library.return_all_books(1))
    #     self.assertEqual(self.patron1.checked_out_books, [])
    #     self.assertFalse(self.book1.is_checked_out)
    #     self.assertFalse(self.book2.is_checked_out)

    #     self.assertIn(("return", 1, 101, "success"), self.library.transaction_log)
    #     self.assertIn(("return", 1, 102, "success"), self.library.transaction_log)

    # def test_return_all_books_nonexistent_patron(self):
    #     self.assertFalse(self.library.return_all_books(999))

    # def test_return_all_books_patron_has_no_checked_out_books(self):
    #     self.assertFalse(self.library.return_all_books(1))


if __name__ == "__main__":
    unittest.main(verbosity=2)