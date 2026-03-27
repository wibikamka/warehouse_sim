from collections import deque

def bfs_distance(warehouse, start, goal):
    queue = deque()
    visited = set()

    # (x, y, distance)
    queue.append((start[0], start[1], 0))
    visited.add(start)

    while queue:
        x, y, dist = queue.popleft()

        # jika sampai tujuan
        if (x, y) == goal:
            return dist

        # 4 arah gerakan
        directions = [
            (0, 1),   # bawah
            (0, -1),  # atas
            (1, 0),   # kanan
            (-1, 0)   # kiri
        ]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if (nx, ny) not in visited and warehouse.is_walkable(nx, ny):
                visited.add((nx, ny))
                queue.append((nx, ny, dist + 1))

    return float('inf')  # jika tidak ada jalur