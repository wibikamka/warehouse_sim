import random
from utils.distance import bfs_distance

def generate_order(rack_positions, k, seed=None):
    if seed is not None:
        random.seed(seed)

    if k > len(rack_positions):
        raise ValueError("k lebih besar dari jumlah rack")

    return random.sample(rack_positions, k)


def map_order_to_access_points(warehouse, order):
    start = warehouse.start
    mapped_points = []

    for rack in order:
        access_points = warehouse.get_access_points(rack)

        if not access_points:
            continue  # skip jika tidak ada akses (harusnya jarang)

        # cari access point dengan jarak minimum dari start
        best_point = None
        best_distance = float('inf')

        for ap in access_points:
            dist = bfs_distance(warehouse, start, ap)

            if dist < best_distance:
                best_distance = dist
                best_point = ap

        mapped_points.append(best_point)

    return mapped_points