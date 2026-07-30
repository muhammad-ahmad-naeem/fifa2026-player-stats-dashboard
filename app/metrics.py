import numpy as np

def per_90(player_time, player_goals):
    if player_goals is None or (isinstance(player_goals, float) and np.isnan(player_goals)):
        return None
    if player_time == 0:
        return None
    goals_per_90_min = (player_goals / player_time) * 90
    return goals_per_90_min


import numpy as np

def z_score(player_value, group_values):
    if player_value is None or (isinstance(player_value, float) and np.isnan(player_value)):
        return None

    group_arr = np.array(group_values, dtype=float)
    group_arr = group_arr[~np.isnan(group_arr)]

    if len(group_arr) == 0:
        return None

    mean = np.mean(group_arr)
    std_dev = np.std(group_arr)

    if std_dev == 0:
        return None
    z = (player_value - mean) / std_dev
    return z


def impact_score(z_scores_list):
    valid_scores = [z for z in z_scores_list if z is not None]
    if len(valid_scores) == 0:
        return None
    return sum(valid_scores) / len(valid_scores)


CORE_COMPARISON_STATS = [
    "total_goals",
    "total_assists",
    "total_shots_on_target",
    "total_tackles",
    "total_clean_sheets",
    "avg_pass_accuracy_pct",
]

def compare_teams(team_a_row, team_b_row):
    team_a_score = 0
    team_b_score = 0
    stat_breakdown = {}

    for stat in CORE_COMPARISON_STATS:
        a_value = team_a_row[stat]
        b_value = team_b_row[stat]

        if a_value > b_value:
            team_a_score += 1
            stat_breakdown[stat] = {"winner": "team_a", "team_a_value": a_value, "team_b_value": b_value}
        elif b_value > a_value:
            team_b_score += 1
            stat_breakdown[stat] = {"winner": "team_b", "team_a_value": a_value, "team_b_value": b_value}
        else:
            stat_breakdown[stat] = {"winner": "tie", "team_a_value": a_value, "team_b_value": b_value}

    if team_a_score > team_b_score:
        winner = "team_a"
        tiebreaker_used = False
    elif team_b_score > team_a_score:
        winner = "team_b"
        tiebreaker_used = False
    else:
        team_a_cards = team_a_row["total_yellow_cards"] + team_a_row["total_red_cards"]
        team_b_cards = team_b_row["total_yellow_cards"] + team_b_row["total_red_cards"]

        if team_a_cards < team_b_cards:
            winner = "team_a"
        elif team_b_cards < team_a_cards:
            winner = "team_b"
        else:
            winner = "draw"
        tiebreaker_used = True

    return {
        "winner": winner,
        "tiebreaker_used": tiebreaker_used,
        "stat_breakdown": stat_breakdown,
        "team_a_score": team_a_score,
        "team_b_score": team_b_score,
    }


POSITION_STATS = {
    "GK":  ["saves", "clean_sheets", "pass_accuracy_pct"],
    "CB":  ["tackles", "clean_sheets", "pass_accuracy_pct"],
    "RB":  ["tackles", "clean_sheets", "pass_accuracy_pct"],
    "LB":  ["tackles", "clean_sheets", "pass_accuracy_pct"],
    "CDM": ["tackles", "assists", "pass_accuracy_pct"],
    "CM":  ["assists", "pass_accuracy_pct", "tackles"],
    "CAM": ["assists", "goals", "pass_accuracy_pct"],
    "LW":  ["goals", "assists", "shots_on_target"],
    "RW":  ["goals", "assists", "shots_on_target"],
    "ST":  ["goals", "assists", "shots_on_target"],
}


def score_player(player_row, peer_group_df, position_stats=POSITION_STATS):
    position = player_row["position"]
    relevant_stats = position_stats.get(position, [])

    player_z_scores = []
    for stat in relevant_stats:
        player_value = player_row[stat]
        peer_group_values = peer_group_df[stat]
        z = z_score(player_value, peer_group_values)
        player_z_scores.append(z)

    return impact_score(player_z_scores)