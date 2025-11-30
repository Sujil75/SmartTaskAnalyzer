from django.test import TestCase

def test_past_due_date():
    task = {
        "id": 1,
        "title": "Old Task",
        "due_date": "1990-01-01",
        "estimated_hours": 2,
        "importance": 5,
        "dependencies": []
    }
    score = get_priority_score(task, [task])
    self.assertTrue(score > 40)  # very urgent


def test_missing_importance():
    task = {
        "id": 1,
        "title": "No Importance",
        "due_date": "2025-12-01",
        "estimated_hours": 2,
        "dependencies": []
    }
    score = get_priority_score(task, [task])
    self.assertIsNotNone(score)
