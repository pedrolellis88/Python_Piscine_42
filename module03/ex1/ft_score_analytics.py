import sys


def score_analytics():
    """Processes numeric scores from command-line arguments and displays statistics.""" # noqa
    print("=== Player Score Analytics ===")
    if len(sys.argv) == 1:
        print("No scores provided. Usage: python3 ft_score_analytics.py <score1> <score2> ...") # noqa
        return
    scores = []
    invalid = []

    i = 1
    while i < len(sys.argv):
        try:
            score = int(sys.argv[i])
            scores.append(score)
        except:  # noqa
            invalid.append(sys.argv[i])
        i += 1

    if len(scores) == 0:
        print("No valid scores provided. Please enter integer scores only.")
        if len(invalid) > 0:
            print(f"Invalid entries ignored: {invalid}")
        return

    print(f"Scores processed: {scores}")
    print(f"Total players: {len(scores)}")
    print(f"Total score: {sum(scores)}")
    print(f"Average score: {sum(scores) / len(scores)}")
    print(f"High score: {max(scores)}")
    print(f"Low score: {min(scores)}")
    print(f"Score range: {max(scores) - min(scores)}")
    if len(invalid) > 0:
        print(f"Invalid entries ignored: {invalid}")


score_analytics()
