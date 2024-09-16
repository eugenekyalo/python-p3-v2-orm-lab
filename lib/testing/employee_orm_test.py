import pytest
from employee import Employee
from review import Review
from department import Department

class TestEmployeeORM:

    def setup_method(self):
        Employee.drop_table()
        Review.drop_table()
        Department.drop_table()
        Employee.create_table()
        Review.create_table()
        Department.create_table()
        self.department = Department.create("HR", "Building A")
        self.employee = Employee.create("John Doe", self.department.id)

    def test_save(self):
        assert self.employee.id is not None

    def test_create(self):
        employee = Employee.create("Jane Smith", self.department.id)
        assert employee.name == "Jane Smith"
        assert employee.department_id == self.department.id

    def test_find_by_id(self):
        found_employee = Employee.find_by_id(self.employee.id)
        assert found_employee.name == self.employee.name

    def test_update(self):
        self.employee.name = "John Smith"
        self.employee.update()
        updated_employee = Employee.find_by_id(self.employee.id)
        assert updated_employee.name == "John Smith"

    def test_delete(self):
        self.employee.delete()
        deleted_employee = Employee.find_by_id(self.employee.id)
        assert deleted_employee is None

    def test_get_all(self):
        employees = Employee.get_all()
        assert len(employees) == 1
        assert employees[0].name == "John Doe"

    def teardown_method(self):
        Employee.drop_table()
        Review.drop_table()
        Department.drop_table()
