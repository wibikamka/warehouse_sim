from models.warehouse import Warehouse
from utils.distance import bfs_distance

def main():
    wh = Warehouse(10, 10)
    wh.generate_layout()
    wh.display()

    start = (0, 0)
    rack = (0, 1)

    access_points = wh.get_access_points(rack)

    print("\nRack:", rack)
    print("Access points:", access_points)

    # pilih salah satu access point (sementara)
    if access_points:
        goal = access_points[0]
        dist = bfs_distance(wh, start, goal)

        print("\nDistance from", start, "to", goal, "=", dist)
    else:
        print("No access point available!")

if __name__ == "__main__":
    main()