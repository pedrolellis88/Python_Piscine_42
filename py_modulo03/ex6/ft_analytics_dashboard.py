def ft_analytics_dashboard():
    """Demonstration of list/set/dict concepts"""
    print("=== Game Analytics Dashboard ===\n")

    players = [
        {"name": "alice", "score": 2300, "active": True,  "region": "north",   "achievements": ["first_kill", "level_10", "boss_slayer", "collector", "speed_run"]}, # noqa
        {"name": "bob",   "score": 1800, "active": True,  "region": "east",    "achievements": ["first_kill", "team_player", "builder"]}, # noqa
        {"name": "charlie","score": 2150,"active": True,  "region": "central", "achievements": ["first_kill", "level_10", "boss_slayer", "strategist", "survivor", "explorer", "crafter"]}, # noqa
        {"name": "diana", "score": 2050, "active": False, "region": "north",   "achievements": ["first_kill", "explorer"]}, # noqa
    ]

    print("=== List Comprehension Examples ===")
    high_scorers = [p["name"] for p in players if p["score"] > 2000]
    print(f"High scorers (>2000): {high_scorers}")
    scores_doubled = [p["score"] * 2 for p in players]
    print(f"Scores doubled: {scores_doubled}")
    active_players = [p["name"] for p in players if p["active"]]
    print(f"Active players: {active_players}")

    print("\n=== Dict Comprehension Examples ===")
    player_scores = {p["name"]: p["score"] for p in players if p["active"]}
    print(f"Player scores: {player_scores}")
    categories = [
        ("high" if p["score"] >= 2100 else "medium" if p["score"] >= 1900 else "low") # noqa
        for p in players
    ]
    score_categories = {c: len([x for x in categories if x == c]) for c in {"high", "medium", "low"}} # noqa
    print(f"Score categories: {score_categories}")
    achievement_counts = {p["name"]: len(p["achievements"]) for p in players}
    print(f"Achievement counts: {achievement_counts}")

    print("\n=== Set Comprehension Examples ===")
    unique_players = {p["name"] for p in players}
    print(f"Unique players: {unique_players}")
    unique_achievements = {a for p in players for a in p["achievements"]}
    print(f"Unique achievements: {unique_achievements}")
    active_regions = {p["region"] for p in players if p["active"]}
    print(f"Active regions: {active_regions}")

    print("\n=== Combined Analysis ===")

    total_players = len(unique_players)
    total_unique_achievements = len(unique_achievements)
    scores = [p["score"] for p in players]
    avg_score = sum(scores) / len(scores) if len(scores) > 0 else 0
    top_score = max(scores) if len(scores) > 0 else 0
    top_names = [p["name"] for p in players if p["score"] == top_score]
    top_name = sorted(top_names)[0] if len(top_names) > 0 else "none"
    top_achievements = max([len(p["achievements"]) for p in players]) if len(players) > 0 else 0 # noqa
    top_player_ach = [p for p in players if p["name"] == top_name]
    top_player_ach_count = len(top_player_ach[0]["achievements"]) if len(top_player_ach) > 0 else 0 # noqa

    print(f"Total players: {total_players}")
    print(f"Total unique achievements: {total_unique_achievements}")
    print(f"Average score: {avg_score}")
    print(f"Top performer: {top_name} ({top_score} points, {top_player_ach_count} achievements)") # noqa


ft_analytics_dashboard()
