import pytest
from department import Department
from employee import Employee

class TestDepartmentORM:

    def setup_method(self):
        Department.drop_table()
        Employee.drop_table()
        Department.create_table()
        Employee.create_table()
        self.department = Department.create("Engineering", "Building B")
        self.employee = Employee.create("Alice", self.department.id)

    def test_save(self):
        assert self.department.id is not None

    def test_create(self):
        department = Department.create("Marketing", "Building C")
        assert department.name == "Marketing"
        assert department.location == "Building C"

    def test_find_by_id(self):
        found_department = Department.find_by_id(self.department.id)
        assert found_department.name == self.department.name

    def test_find_by_name(self):
        found_department = Department.find_by_name("Engineering")
        assert found_department.location == self.department.location

    def test_update(self):
        self.department.name = "R&D"
        self.department.update()
        updated_department = Department.find_by_id(self.department.id)
        assert updated_department.name == "R&D"

    def test_delete(self):
        self.department.delete()
        deleted_department = Department.find_by_id(self.department.id)
        assert deleted_department is None

    def test_get_all(self):
        departments = Department.get_all()
        assert len(departments) == 1
        assert departments[0].name == "Engineering"

    def test_employees(self):
        employees = self.department.employees()
        assert len(employees) == 1
        assert employees[0].name == "Alice"

    def teardown_method(self):
        Department.drop_table()
        Employee.drop_table()
