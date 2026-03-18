"""
Project: Analyzing Baseball Data
A module for filtering, aggregating, and computing top statistics
from professional baseball datasets.
"""

def filter_by_year(statistics, year):
    """
    Returns a list of dictionaries containing stats for a specific year.
    """
    return [entry for entry in statistics if entry['yearID'] == year]

def top_player_ids(info, formula, num_players):
    """
    Returns a list of top player IDs sorted by a provided formula.
    In case of ties, sorts alphabetically by playerID.
    """
    # Sort by (formula_result, playerID) to handle ties alphabetically
    sorted_data = sorted(info.items(), 
                         key=lambda item: (formula(item[1]), item[0]), 
                         reverse=True)
    
    # Return only the playerID (the key) for the top N players
    return [player[0] for player in sorted_data[:num_players]]

def lookup_player_names(info, player_ids):
    """
    Maps player IDs to their full names using a master info dictionary.
    """
    names = []
    for p_id in player_ids:
        if p_id in info:
            full_name = f"{info[p_id]['nameFirst']} {info[p_id]['nameLast']}"
            names.append(full_name)
    return names

def aggregate_by_player_id(statistics):
    """
    Aggregates yearly stats into a single career dictionary per player.
    """
    career_stats = {}
    keys_to_sum = ['G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'SB']
    
    for entry in statistics:
        p_id = entry['playerID']
        if p_id not in career_stats:
            career_stats[p_id] = entry.copy()
        else:
            for key in keys_to_sum:
                career_stats[p_id][key] += entry[key]
                
    return career_stats

def compute_top_stats_year(statistics, formula, num_players, year):
    """
    Computes top players for a specific year.
    """
    year_data = filter_by_year(statistics, year)
    # Convert list of dicts to dict of dicts for top_player_ids
    year_dict = {entry['playerID']: entry for entry in year_data}
    return top_player_ids(year_dict, formula, num_players)

def compute_top_stats_career(statistics, formula, num_players):
    """
    Computes top players based on their entire career totals.
    """
    career_dict = aggregate_by_player_id(statistics)
    return top_player_ids(career_dict, formula, num_players)

# --- Example Formulas for Testing ---

def batting_average(stats):
    """Formula for Batting Average: H / AB"""
    if stats['AB'] > 0:
        return stats['H'] / stats['AB']
    return 0.0

def slugging_percentage(stats):
    """Formula for Slugging Percentage: Total Bases / AB"""
    if stats['AB'] > 0:
        singles = stats['H'] - (stats['2B'] + stats['3B'] + stats['HR'])
        total_bases = singles + (2 * stats['2B']) + (3 * stats['3B']) + (4 * stats['HR'])
        return total_bases / stats['AB']
    return 0.0