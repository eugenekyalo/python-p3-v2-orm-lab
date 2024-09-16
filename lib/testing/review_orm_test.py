import pytest
from review import Review
from employee import Employee

class TestReviewORM:

    def setup_method(self):
        Employee.create_table()
        Review.drop_table()
        Review.create_table()
        self.employee = Employee.create("John Doe", None)
        self.review = Review.create(2024, "Excellent work", self.employee.id)

    def test_save(self):
        assert self.review.id is not None

    def test_create(self):
        review = Review.create(2024, "Great job", self.employee.id)
        assert review.year == 2024
        assert review.summary == "Great job"
        assert review.employee_id == self.employee.id

    def test_find_by_id(self):
        found_review = Review.find_by_id(self.review.id)
        assert found_review.summary == self.review.summary

    def test_update(self):
        self.review.summary = "Needs improvement"
        self.review.update()
        updated_review = Review.find_by_id(self.review.id)
        assert updated_review.summary == "Needs improvement"

    def test_delete(self):
        self.review.delete()
        deleted_review = Review.find_by_id(self.review.id)
        assert deleted_review is None

    def test_get_all(self):
        reviews = Review.get_all()
        assert len(reviews) == 1
        assert reviews[0].summary == "Excellent work"

    def teardown_method(self):
        Review.drop_table()
        Employee.drop_table()
