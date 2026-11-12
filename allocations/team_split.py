import math

def plan_team_sizes(n, min_size, max_size):
    """Return a list of team sizes covering all n students, or None if impossible.

    Uses the fewest teams that respect max_size, then spreads students
    evenly so team sizes differ by at most one.
    """
    if n <= 0 or min_size < 1 or min_size > max_size:
        return None

    team_count = math.ceil(n / max_size)
    if team_count * min_size > n:
        return None

    base, extra = divmod(n, team_count)
    return [base + 1] * extra + [base] * (team_count - extra)


def starting_split(students, sizes):
    """Sort scored students by c_score into teams, and spread students
    with no c_score evenly across the teams (one per team in turn)."""
    scored = sorted(
        (s for s in students if s.get("c_score") is not None),
        key=lambda s: s["c_score"],
    )
    unscored = [s for s in students if s.get("c_score") is None]
    team_count = len(sizes)

    teams = {}
    start = 0
    for index, size in enumerate(sizes):
        team_unscored = unscored[index::team_count]
        take = size - len(team_unscored)
        teams[f"Team {index + 1}"] = scored[start:start + take] + team_unscored
        start += take
    return teams


def make_initial_teams(students, min_size, max_size):
    """Split students into starting teams, or explain why it is impossible."""
    if min_size < 1 or min_size > max_size:
        return {
            "is_feasible": False,
            "teams": None,
            "message": f"Invalid team size settings: minimum {min_size}, maximum {max_size}.",
        }
    if not students:
        return {"is_feasible": False, "teams": None, "message": "There are no students to allocate."}

    sizes = plan_team_sizes(len(students), min_size, max_size)
    if sizes is None:
        return {
            "is_feasible": False,
            "teams": None,
            "message": (
                f"{len(students)} students cannot be split into teams of "
                f"{min_size} to {max_size} students."
            ),
        }

    return {
        "is_feasible": True,
        "teams": starting_split(students, sizes),
        "message": f"{len(students)} students split into {len(sizes)} teams.",
    }