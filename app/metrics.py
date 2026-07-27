import numpy as np

def per_90(player_time, player_goals):
    if player_time==0:
        return(None)
    goals_per_90_min=(player_goals/player_time)*90
    return(goals_per_90_min)


def z_score(player_value, group_values):
    group_arr = np.array(group_values, dtype=float)

    mean = np.mean(group_arr)
    std_dev = np.std(group_arr)

    if std_dev == 0:
        return None   
    z = (player_value - mean) / std_dev
    return z


def impact_score(z_scores_list):
    """
    Takes a list of z-scores (some may be None) and returns their average,
    skipping any None values. Returns None if no valid z-scores exist.
    """
    valid_scores = [z for z in z_scores_list if z is not None]
    
    if len(valid_scores) == 0:
        return None
    
    return sum(valid_scores) / len(valid_scores)