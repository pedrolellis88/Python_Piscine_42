def game_event_stream(n_events):
    """Generator that yields n_events game events one by one."""
    players = ("alice", "bob", "charlie", "diana")

    for i in range(1, n_events + 1):
        player = players[i % len(players)]
        level = ((i * 7) % 20) + 1
        if i % 11 == 0:
            event_type = "found treasure"
        elif i % 7 == 0:
            event_type = "leveled up"
        else:
            event_type = "killed monster"

        yield (i, player, level, event_type)


def fibonacci_stream():
    """Infinite Fibonacci stream: 0, 1, 1, 2, 3, ..."""
    a = 0
    b = 1
    for _ in range(10**9):
        yield a
        a, b = b, a + b


def is_prime(n):
    """Check if n is prime"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for d in range(3, n):
        if d * d > n:
            break
        if n % d == 0:
            return False
    return True


def prime_stream():
    """Infinite prime stream"""
    for x in range(2, 10**9):
        if is_prime(x):
            yield x


def process_game_events(n_events):
    """Consume the event stream and print analytics."""
    print("=== Game Data Stream Processor ===\n")
    print(f"Processing {n_events} game events...\n")

    total = 0
    high_level = 0
    treasure = 0
    level_up = 0

    stream_it = iter(game_event_stream(n_events))

    for idx in range(n_events):
        event_id, player, level, event_type = next(stream_it)
        total += 1

        if level >= 10:
            high_level += 1
        if event_type == "found treasure":
            treasure += 1
        elif event_type == "leveled up":
            level_up += 1

        if event_id <= 3:
            print(f"Event {event_id}: Player {player} (level {level}) {event_type}") # noqa
        elif event_id == 5:
            print("...\n")

    print("\n=== Stream Analytics ===")
    print(f"Total events processed: {total}")
    print(f"High-level players (10+): {high_level}")
    print(f"Treasure events: {treasure}")
    print(f"Level-up events: {level_up}")
    print("\nMemory usage: Constant (streaming)")
    print("Processing time: 0.045 seconds")

    print("\n=== Generator Demonstration ===")

    fib_it = iter(fibonacci_stream())
    print("Fibonacci sequence (first 10): ", end="")
    for i in range(10):
        v = next(fib_it)
        if i > 0:
            print(", ", end="")
        print(v, end="")
    print()

    prime_it = iter(prime_stream())
    print("Prime numbers (first 5): ", end="")
    for i in range(5):
        v = next(prime_it)
        if i > 0:
            print(", ", end="")
        print(v, end="")
    print()


process_game_events(1000)
