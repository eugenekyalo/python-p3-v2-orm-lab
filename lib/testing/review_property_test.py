import pytest
from employee import Employee
from review import Review

class TestReviewProperties:
    def setup_method(self):
        Employee.drop_table()
        Review.drop_table()
        Employee.create_table()
        Review.create_table()
        self.employee = Employee.create("John Doe", "Developer", None)

    def test_valid_year(self):
        review = Review(2022, "Valid summary", self.employee)
        assert review.year == 2022

    def test_invalid_year(self):
        with pytest.raises(ValueError):
            Review(1999, "Invalid year", self.employee)

    def test_valid_summary(self):
        review = Review(2022, "Valid summary", self.employee)
        assert review.summary == "Valid summary"

    def test_invalid_summary(self):
        with pytest.raises(ValueError):
            Review(2022, "", self.employee)

    def test_valid_employee(self):
        review = Review(2022, "Valid summary", self.employee)
        assert review.employee == self.employee

    def test_invalid_employee(self):
        with pytest.raises(ValueError):
            Review(2022, "Valid summary", "Not an Employee instance")

    def test_invalid_employee_not_persisted(self):
        unpersisted_employee = Employee("Jane Doe", "Manager", None)
        with pytest.raises(ValueError):
            Review(2022, "Valid summary", unpersisted_employee)