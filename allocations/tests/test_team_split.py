import random

from django.test import SimpleTestCase

from allocations.team_split import make_initial_teams, plan_team_sizes


def make_students(n, seed=0):
    rng = random.Random(seed)
    return [
        {
            "first_name": f"First{i}",
            "last_name": f"Last{i}",
            "email": f"s{i}@example.com",
            "gender": rng.choice([0, 1, 2, 3]),
            "c_score": rng.randint(0, 100),
        }
        for i in range(n)
    ]


class PlanTeamSizesTests(SimpleTestCase):

    def test_feasible_sizes_cover_everyone_within_limits(self):
        for n in [4, 5, 8, 9, 10, 13, 53, 300]:
            sizes = plan_team_sizes(n, 4, 5)
            self.assertIsNotNone(sizes, f"{n} students should be feasible")
            self.assertEqual(sum(sizes), n)
            self.assertTrue(all(4 <= s <= 5 for s in sizes))

    def test_53_students_gives_11_teams(self):
        self.assertEqual(sorted(plan_team_sizes(53, 4, 5)), [4, 4] + [5] * 9)

    def test_impossible_sizes_return_none(self):
        for n in [1, 2, 3, 6, 7, 11]:
            self.assertIsNone(plan_team_sizes(n, 4, 5), f"{n} students should be infeasible")

    def test_invalid_settings_return_none(self):
        self.assertIsNone(plan_team_sizes(0, 4, 5))
        self.assertIsNone(plan_team_sizes(10, 0, 5))
        self.assertIsNone(plan_team_sizes(10, 6, 5))


class MakeInitialTeamsTests(SimpleTestCase):

    def test_every_student_appears_exactly_once(self):
        students = make_students(53)
        result = make_initial_teams(students, 4, 5)
        self.assertTrue(result["is_feasible"])
        allocated = [s["email"] for team in result["teams"].values() for s in team]
        self.assertEqual(sorted(allocated), sorted(s["email"] for s in students))

    def test_team_sizes_within_limits(self):
        result = make_initial_teams(make_students(53), 4, 5)
        self.assertEqual(len(result["teams"]), 11)
        self.assertTrue(all(4 <= len(team) <= 5 for team in result["teams"].values()))

    def test_teams_are_named(self):
        result = make_initial_teams(make_students(9), 4, 5)
        self.assertEqual(list(result["teams"].keys()), ["Team 1", "Team 2"])

    def test_teams_are_grouped_by_c_score(self):
        teams = list(make_initial_teams(make_students(53), 4, 5)["teams"].values())
        for earlier, later in zip(teams, teams[1:]):
            self.assertLessEqual(
                max(s["c_score"] for s in earlier),
                min(s["c_score"] for s in later),
            )

    def test_missing_c_scores_are_spread_across_teams(self):
        students = make_students(20)
        for s in students[:3]:
            s["c_score"] = None
        del students[3]["c_score"]
        result = make_initial_teams(students, 4, 5)
        self.assertTrue(result["is_feasible"])
        for team in result["teams"].values():
            missing = [s for s in team if s.get("c_score") is None]
            self.assertEqual(len(missing), 1)

    def test_all_c_scores_missing_still_allocates_everyone(self):
        students = make_students(13)
        for s in students:
            s["c_score"] = None
        result = make_initial_teams(students, 4, 5)
        self.assertTrue(result["is_feasible"])
        allocated = [s["email"] for team in result["teams"].values() for s in team]
        self.assertEqual(sorted(allocated), sorted(s["email"] for s in students))
        self.assertTrue(all(4 <= len(team) <= 5 for team in result["teams"].values()))

    def test_impossible_size_is_reported(self):
        result = make_initial_teams(make_students(7), 4, 5)
        self.assertFalse(result["is_feasible"])
        self.assertIsNone(result["teams"])
        self.assertIn("7 students cannot be split", result["message"])

    def test_invalid_settings_are_reported(self):
        result = make_initial_teams(make_students(10), 6, 5)
        self.assertFalse(result["is_feasible"])
        self.assertIn("Invalid team size settings", result["message"])

    def test_no_students_is_reported(self):
        result = make_initial_teams([], 4, 5)
        self.assertFalse(result["is_feasible"])

    def test_original_list_is_not_changed(self):
        students = make_students(20)
        before = [s["email"] for s in students]
        make_initial_teams(students, 4, 5)
        self.assertEqual([s["email"] for s in students], before)