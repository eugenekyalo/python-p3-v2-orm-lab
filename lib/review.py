import sqlite3
from lib import CONN, CURSOR
from lib.employee import Employee  # Make sure Employee class is properly imported

class Review:
    def __init__(self, year, summary, employee_id, id=None):
        self.year = year
        self.summary = summary
        self.employee_id = employee_id
        self.id = id

    def __repr__(self):
        return f"<Review id={self.id} year={self.year} summary='{self.summary}' employee_id={self.employee_id}>"

    @classmethod
    def create_table(cls):
        with CONN:
            CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year INTEGER NOT NULL,
                summary TEXT NOT NULL,
                employee_id INTEGER NOT NULL,
                FOREIGN KEY (employee_id) REFERENCES employees(id)
            )
            """)

    @classmethod
    def drop_table(cls):
        with CONN:
            CURSOR.execute("DROP TABLE IF EXISTS reviews")

    def save(self):
        if self.id is None:
            CURSOR.execute("""
                INSERT INTO reviews (year, summary, employee_id)
                VALUES (?, ?, ?)
            """, (self.year, self.summary, self.employee_id))
            self.id = CURSOR.lastrowid
        else:
            CURSOR.execute("""
                UPDATE reviews
                SET year = ?, summary = ?, employee_id = ?
                WHERE id = ?
            """, (self.year, self.summary, self.employee_id, self.id))
        CONN.commit()

    @classmethod
    def create(cls, year, summary, employee_id):
        review = cls(year, summary, employee_id)
        review.save()
        return review

    @classmethod
    def instance_from_db(cls, row):
        id, year, summary, employee_id = row
        return cls(year, summary, employee_id, id)

    @ @classmethod
    def instance_from_db(cls, row):
        from lib.employee import Employee  # Import here to avoid circular import
        id, content, employee_id = row
        return cls(content, employee_id, id)

    def update(self):
        if self.id:
            CURSOR.execute("""
                UPDATE reviews
                SET year = ?, summary = ?, employee_id = ?
                WHERE id = ?
            """, (self.year, self.summary, self.employee_id, self.id))
            CONN.commit()

    def delete(self):
        if self.id:
            CURSOR.execute("DELETE FROM reviews WHERE id = ?", (self.id,))
            CONN.commit()
            self.id = None

    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM reviews")
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        if not isinstance(value, int) or value < 2000:
            raise ValueError("Year must be an integer greater than or equal to 2000")
        self._year = value

    @property
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Summary must be a non-empty string")
        self._summary = value

    @property
    def employee_id(self):
        return self._employee_id

    @employee_id.setter
    def employee_id(self, value):
        if not isinstance(value, int):
            raise ValueError("Employee ID must be an integer")
        self._employee_id = value
