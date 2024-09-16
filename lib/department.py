import sqlite3
from lib import CONN, CURSOR

class Department:
    def __init__(self, name, location, id=None):
        self.name = name
        self.location = location
        self.id = id

    def __repr__(self):
        return f"<Department id={self.id} name='{self.name}' location='{self.location}'>"

    @classmethod
    def create_table(cls):
        with CONN:
            CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                location TEXT NOT NULL
            )
            """)

    @classmethod
    def drop_table(cls):
        with CONN:
            CURSOR.execute("DROP TABLE IF EXISTS departments")

    def save(self):
        if self.id is None:
            CURSOR.execute("""
                INSERT INTO departments (name, location)
                VALUES (?, ?)
            """, (self.name, self.location))
            self.id = CURSOR.lastrowid
        else:
            CURSOR.execute("""
                UPDATE departments
                SET name = ?, location = ?
                WHERE id = ?
            """, (self.name, self.location, self.id))
        CONN.commit()

    @classmethod
    def create(cls, name, location):
        department = cls(name, location)
        department.save()
        return department

    @classmethod
    def instance_from_db(cls, row):
        id, name, location = row
        return cls(name, location, id)

    @classmethod
    def find_by_id(cls, id):
        CURSOR.execute("SELECT * FROM departments WHERE id = ?", (id,))
        row = CURSOR.fetchone()
        if row:
            return cls.instance_from_db(row)
        return None

    def update(self):
        if self.id:
            CURSOR.execute("""
                UPDATE departments
                SET name = ?, location = ?
                WHERE id = ?
            """, (self.name, self.location, self.id))
            CONN.commit()

    def delete(self):
        if self.id:
            CURSOR.execute("DELETE FROM departments WHERE id = ?", (self.id,))
            CONN.commit()
            self.id = None

    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM departments")
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string")
        self._name = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Location must be a non-empty string")
        self._location = value
