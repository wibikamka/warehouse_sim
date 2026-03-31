def debug_bfs_basic(warehouse, bfs_distance):
    print("\n=== BFS BASIC TEST ===")

    tests = [
        ((0, 0), (1, 0)),  # harus 1
        ((0, 0), (2, 0)),  # harus 2
        ((0, 0), (0, 2)),  # harus >2 (karena rack blocking)
    ]

    for start, goal in tests:
        dist = bfs_distance(warehouse, start, goal)
        print(f"{start} -> {goal} = {dist}")


def debug_reachability(warehouse, bfs_distance, points):
    print("\n=== REACHABILITY TEST ===")

    start = warehouse.start

    for p in points:
        dist = bfs_distance(warehouse, start, p)
        if dist == float('inf'):
            print(f" UNREACHABLE: {p}")
        else:
            print(f" reachable: {p} distance = {dist}")


def debug_mapping(order, mapped):
    print("\n=== MAPPING CHECK ===")

    if len(order) != len(mapped):
        print(" ERROR: jumlah order != mapped")
    else:
        print(" mapping size correct")

    for r, m in zip(order, mapped):
        print(f"rack {r} -> access {m}")


def debug_route(route, targets):
    print("\n=== ROUTE VALIDATION ===")

    visited = route[1:-1]  # exclude start & end

    if len(visited) != len(targets):
        print(" ERROR: jumlah node tidak sesuai")
    else:
        print(" jumlah node sesuai")

    if set(visited) != set(targets):
        print(" ERROR: ada node hilang / duplikat")
        print("visited:", visited)
        print("targets:", targets)
    else:
        print(" semua target dikunjungi tepat sekali")


def debug_total_distance(warehouse, bfs_distance, route):
    print("\n=== DISTANCE CHECK ===")

    total = 0

    for i in range(len(route) - 1):
        a = route[i]
        b = route[i + 1]
        dist = bfs_distance(warehouse, a, b)

        print(f"{a} -> {b} = {dist}")

        if dist == float('inf'):
            print(" ERROR: path tidak valid!")

        total += dist

    print("Recomputed total =", total)
    return total