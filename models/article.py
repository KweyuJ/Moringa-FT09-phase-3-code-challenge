
from database.connection import get_db_connection
from models.author import Author
from models.magazine import Magazine

class Article:
    all = {}

    def __init__(self, title, content, author_id, magazine_id, id=None):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return f'<Article {self.title}>'

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if isinstance(title, str) and 5 <= len(title) <= 50:
            self._title = title
        else:
            raise ValueError("Title must be a string between 5 and 50 characters")

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        if isinstance(content, str) and len(content) > 0:
            self._content = content
        else:
            raise ValueError("Content must be a non-empty string")

    @property
    def author_id(self):
        return self._author_id

    @author_id.setter
    def author_id(self, author_id):
        if isinstance(author_id, int):
            self._author_id = author_id
        else:
            raise ValueError("Author ID must be an integer")

    @property
    def magazine_id(self):
        return self._magazine_id

    @magazine_id.setter
    def magazine_id(self, magazine_id):
        if isinstance(magazine_id, int):
            self._magazine_id = magazine_id
        else:
            raise ValueError("Magazine ID must be an integer")

    @classmethod
    def create_table(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            magazine_id INTEGER NOT NULL,
            FOREIGN KEY (author_id) REFERENCES authors(id),
            FOREIGN KEY (magazine_id) REFERENCES magazines(id))
        """
        cursor.execute(sql)
        conn.commit()
        conn.close()

    @classmethod
    def drop_table(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "DROP TABLE IF EXISTS articles"
        cursor.execute(sql)
        conn.commit()
        conn.close()

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        if self.id:
            sql = "UPDATE articles SET title = ?, content = ?, author_id = ?, magazine_id = ? WHERE id = ?"
            cursor.execute(sql, (self.title, self.content, self.author_id, self.magazine_id, self.id))
        else:
            sql = "INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)"
            cursor.execute(sql, (self.title, self.content, self.author_id, self.magazine_id))
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()
        type(self).all[self.id] = self

    def delete(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "DELETE FROM articles WHERE id = ?"
        cursor.execute(sql, (self.id,))
        conn.commit()
        conn.close()
        del type(self).all[self.id]
        self.id = None

    @classmethod
    def create(cls, title, content, author, magazine):
        article = cls(title, content, author.id, magazine.id)
        article.save()
        return article

    @classmethod
    def instance_from_db(cls, row):
        article = cls.all.get(row[0])
        if article:
            article.title = row[1]
            article.content = row[2]
            article.author_id = row[3]
            article.magazine_id = row[4]
        else:
            article = cls(row[1], row[2], row[3], row[4])
            article.id = row[0]
            cls.all[article.id] = article
        return article

    @classmethod
    def get_all(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM articles"
        rows = cursor.execute(sql).fetchall()
        conn.close()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM articles WHERE id = ?"
        row = cursor.execute(sql, (id,)).fetchone()
        conn.close()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_title(cls, title):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM articles WHERE title = ?"
        row = cursor.execute(sql, (title,)).fetchone()
        conn.close()
        return cls.instance_from_db(row) if row else None
