from utils.distance import bfs_distance

def nearest_neighbor_route(warehouse, start, targets):
    unvisited = targets.copy()
    current = start

    route = [start]
    total_distance = 0

    while unvisited:
        print("\nFrom", current)

        nearest = None
        best_distance = float('inf')

        for point in unvisited:
            dist = bfs_distance(warehouse, current, point)
            print("  to", point, "=", dist)

            if dist < best_distance:
                best_distance = dist
                nearest = point

        print(" choose", nearest, "distance =", best_distance)

        route.append(nearest)
        total_distance += best_distance

        current = nearest
        unvisited.remove(nearest)

    # kembali ke start
    back_distance = bfs_distance(warehouse, current, start)
    total_distance += back_distance
    route.append(start)

    return route, total_distance