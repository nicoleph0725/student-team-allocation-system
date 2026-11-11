from django.test import TestCase
from allocations.policies import AttainmentHomogeneityPolicy

class TestAttainmentHomogeneityPolicy(TestCase):
    
    def setUp(self):
        # setUp runs before every test, keeping your code DRY (Don't Repeat Yourself)
        self.policy = AttainmentHomogeneityPolicy(max_allowed_spread=10)

    def test_team_passes_with_tight_spread(self):
        # Arrange
        team_alpha = [
            {"first_name": "Rahul", "c_score": 73},
            {"first_name": "Winston", "c_score": 71}
        ]
        
        # Act
        result = self.policy.evaluate("Team Alpha", team_alpha)
        
        # Assert
        self.assertTrue(result["is_satisfied"])

    def test_team_fails_with_wide_spread(self):
        # Arrange
        team_bravo = [
            {"first_name": "Zoya", "c_score": 46},
            {"first_name": "Andre", "c_score": 88}
        ]
        
        # Act
        result = self.policy.evaluate("Team Bravo", team_bravo)
        
        # Assert
        self.assertFalse(result["is_satisfied"])