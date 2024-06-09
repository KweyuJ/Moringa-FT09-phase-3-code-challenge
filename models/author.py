# models/author.py
from database.connection import get_db_connection

class Author:
    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Author {self.name}>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name) > 0:
            self._name = name
        else:
            raise ValueError("Name must be a non-empty string")

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Author instances """
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL)
        """
        cursor.execute(sql)
        conn.commit()
        conn.close()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Author instances """
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "DROP TABLE IF EXISTS authors"
        cursor.execute(sql)
        conn.commit()
        conn.close()

    def save(self):
        """ Insert a new row with the name value of the current Author object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key """
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO authors (name) VALUES (?)"
        cursor.execute(sql, (self.name,))
        conn.commit()
        self.id = cursor.lastrowid
        type(self).all[self.id] = self
        conn.close()

    def update(self):
        """ Update the table row corresponding to the current Author instance. """
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "UPDATE authors SET name = ? WHERE id = ?"
        cursor.execute(sql, (self.name, self.id))
        conn.commit()
        conn.close()

    def delete(self):
        """ Delete the table row corresponding to the current Author instance,
        delete the dictionary entry, and reassign id attribute """
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "DELETE FROM authors WHERE id = ?"
        cursor.execute(sql, (self.id,))
        conn.commit()
        conn.close()
        # Delete the dictionary entry using id as the key
        del type(self).all[self.id]
        # Set the id to None
        self.id = None

    @classmethod
    def create(cls, name):
        """ Initialize a new Author instance and save the object to the database """
        author = cls(name)
        author.save()
        return author

    @classmethod
    def instance_from_db(cls, row):
        """ Return an Author object having the attribute values from the table row. """
        author = cls.all.get(row[0])
        if author:
            author.name = row[1]
        else:
            author = cls(row[1])
            author.id = row[0]
            cls.all[author.id] = author
        return author

    @classmethod
    def get_all(cls):
        """ Return a list containing one Author object per table row """
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM authors"
        rows = cursor.execute(sql).fetchall()
        conn.close()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """ Return Author object corresponding to the table row matching the specified primary key """
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM authors WHERE id = ?"
        row = cursor.execute(sql, (id,)).fetchone()
        conn.close()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        """ Return Author object corresponding to the first table row matching the specified name """
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM authors WHERE name = ?"
        row = cursor.execute(sql, (name,)).fetchone()
        conn.close()
        return cls.instance_from_db(row) if row else None
