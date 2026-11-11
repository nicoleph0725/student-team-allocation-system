class AttainmentHomogeneityPolicy:
    def __init__(self, max_allowed_spread: int = 15):
        self.max_allowed_spread = max_allowed_spread

    def evaluate(self, team_name: str, students: list[dict]) -> dict:
        if not students:
            return {"is_satisfied": False, "spread": None, "error": "Team is empty"}

        c_scores = [student.get("c_score", 0) for student in students]
        spread = max(c_scores) - min(c_scores)

        return {
            "is_satisfied": spread <= self.max_allowed_spread,
            "spread": spread,
            "max_allowed": self.max_allowed_spread
        }