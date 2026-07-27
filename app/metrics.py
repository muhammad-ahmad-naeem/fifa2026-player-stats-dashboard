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