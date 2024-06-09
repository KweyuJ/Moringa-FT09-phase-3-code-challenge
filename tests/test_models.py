import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine

class TestModels(unittest.TestCase):
    def test_author_creation(self):
        author1 = Author(1, "John Doe")
        self.assertEqual(author1.name, "John Doe")

        author2 = Author(2, "Jane Smith")
        self.assertEqual(author2.name, "Jane Smith")

    def test_article_creation(self):
        article1 = Article(1, "Test Title", "Test Content", 1, 1)
        self.assertEqual(article1.title, "Test Title")

        article2 = Article(2, "Climate Change", "Test Content part two", 2, 2)
        self.assertEqual(article2.title, "Climate Change")

    def test_magazine_creation(self):
        magazine1 = Magazine(1, "Tech Weekly")
        self.assertEqual(magazine1.name, "Tech Weekly")

        magazine2 = Magazine(2, "Science Monthly", "Science")
        self.assertEqual(magazine2.name, "Science Monthly")

if __name__ == "__main__":
    unittest.main()
