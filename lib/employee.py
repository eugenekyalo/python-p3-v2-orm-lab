from lib import CONN, CURSOR
from lib.review import Review  # Ensure this import is correct

class Employee:
    def __init__(self, name, job_title, department_id, id=None):
        self.name = name
        self.job_title = job_title
        self.department_id = department_id
        self.id = id

    def __repr__(self):
        return f"<Employee id={self.id} name='{self.name}' job_title='{self.job_title}' department_id={self.department_id}>"

    @classmethod
    def create_table(cls):
        with CONN:
            CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                job_title TEXT NOT NULL,
                department_id INTEGER,
                FOREIGN KEY (department_id) REFERENCES departments(id)
            )
            """)

    @classmethod
    def drop_table(cls):
        with CONN:
            CURSOR.execute("DROP TABLE IF EXISTS employees")

    def save(self):
        if self.id is None:
            CURSOR.execute("""
                INSERT INTO employees (name, job_title, department_id)
                VALUES (?, ?, ?)
            """, (self.name, self.job_title, self.department_id))
            self.id = CURSOR.lastrowid
        else:
            CURSOR.execute("""
                UPDATE employees
                SET name = ?, job_title = ?, department_id = ?
                WHERE id = ?
            """, (self.name, self.job_title, self.department_id, self.id))
        CONN.commit()

    @classmethod
    def create(cls, name, job_title, department_id):
        employee = cls(name, job_title, department_id)
        employee.save()
        return employee

    @classmethod
    def instance_from_db(cls, row):
        id, name, job_title, department_id = row
        return cls(name, job_title, department_id, id)

    @classmethod
    def find_by_id(cls, id):
        CURSOR.execute("SELECT * FROM employees WHERE id = ?", (id,))
        row = CURSOR.fetchone()
        if row:
            return cls.instance_from_db(row)
        return None

    def update(self):
        if self.id:
            CURSOR.execute("""
                UPDATE employees
                SET name = ?, job_title = ?, department_id = ?
                WHERE id = ?
            """, (self.name, self.job_title, self.department_id, self.id))
            CONN.commit()

    def delete(self):
        if self.id:
            CURSOR.execute("DELETE FROM employees WHERE id = ?", (self.id,))
            CONN.commit()
            self.id = None

    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM employees")
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]

    def reviews(self):
        from lib.review import Review  # Import here to avoid circular import
        CURSOR.execute("SELECT * FROM reviews WHERE employee_id = ?", (self.id,))
        rows = CURSOR.fetchall()
        return [Review.instance_from_db(row) for row in rows]

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string")
        self._name = value

    @property
    def job_title(self):
        return self._job_title

    @job_title.setter
    def job_title(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Job title must be a non-empty string")
        self._job_title = value

    @property
    def department_id(self):
        return self._department_id

    @department_id.setter
    def department_id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("Department ID must be an integer")
        self._department_id = value
