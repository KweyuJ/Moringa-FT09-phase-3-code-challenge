
from database.connection import get_db_connection

class Magazine:
    all = {}

    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
        return f'<Magazine {self.name}>'

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and 2 <= len(name) <= 16:
            self._name = name
        else:
            raise ValueError("Name must be a string between 2 and 16 characters")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        if isinstance(category, str) and len(category) > 0:
            self._category = category
        else:
            raise ValueError("Category must be a non-empty string")

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        if isinstance(id, int):
            self._id = id
        else:
            raise ValueError("ID must be an integer")

    @classmethod
    def create_table(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            CREATE TABLE IF NOT EXISTS magazines (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL)
        """
        cursor.execute(sql)
        conn.commit()
        conn.close()

    @classmethod
    def drop_table(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "DROP TABLE IF EXISTS magazines"
        cursor.execute(sql)
        conn.commit()
        conn.close()

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        if self.id:
            sql = "UPDATE magazines SET name = ?, category = ? WHERE id = ?"
            cursor.execute(sql, (self.name, self.category, self.id))
        else:
            sql = "INSERT INTO magazines (name, category) VALUES (?, ?)"
            cursor.execute(sql, (self.name, self.category))
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()
        type(self).all[self.id] = self

    def delete(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "DELETE FROM magazines WHERE id = ?"
        cursor.execute(sql, (self.id,))
        conn.commit()
        conn.close()
        del type(self).all[self.id]
        self.id = None

    @classmethod
    def create(cls, name, category):
        magazine = cls(name, category)
        magazine.save()
        return magazine

    @classmethod
    def instance_from_db(cls, row):
        magazine = cls.all.get(row[0])
        if magazine:
            magazine.name = row[1]
            magazine.category = row[2]
        else:
            magazine = cls(row[1], row[2])
            magazine.id = row[0]
            cls.all[magazine.id] = magazine
        return magazine

    @classmethod
    def get_all(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM magazines"
        rows = cursor.execute(sql).fetchall()
        conn.close()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM magazines WHERE id = ?"
        row = cursor.execute(sql, (id,)).fetchone()
        conn.close()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM magazines WHERE name = ?"
        row = cursor.execute(sql, (name,)).fetchone()
        conn.close()
        return cls.instance_from_db(row) if row else None
