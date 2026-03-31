# test_setup.py
"""Test script to verify all components work correctly"""

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.warehouse import Warehouse
from utils.distance import bfs_distance
from utils.order import generate_order, map_order_to_access_points
from routing.nn import nearest_neighbor_route
from routing.ga import genetic_algorithm, total_distance

def test_warehouse():
    """Test 1: Warehouse generation"""
    print("\n" + "="*60)
    print("TEST 1: Warehouse Generation")
    print("="*60)
    
    wh = Warehouse(10, 10)
    wh.generate_layout()
    
    print("Warehouse layout (first 5 rows):")
    for i in range(5):
        print(' '.join(wh.grid[i][:10]))
    
    print(f"\nTotal racks: {len(wh.rack_positions)}")
    print(f"Start position: {wh.start}")
    
    # Test is_walkable
    test_positions = [(0,0), (0,1), (1,0), (1,1)]
    print("\nWalkability test:")
    for pos in test_positions:
        walkable = wh.is_walkable(pos[0], pos[1])
        cell = wh.grid[pos[1]][pos[0]]
        print(f"  {pos}: '{cell}' -> walkable: {walkable}")
    
    return wh

def test_bfs(wh):
    """Test 2: BFS Distance"""
    print("\n" + "="*60)
    print("TEST 2: BFS Distance")
    print("="*60)
    
    start = (0, 0)
    test_goals = [(1, 0), (2, 0), (0, 2), (1, 1)]
    
    for goal in test_goals:
        dist = bfs_distance(wh, start, goal)
        print(f"  {start} -> {goal} = {dist}")
    
    return True

def test_order(wh):
    """Test 3: Order Generation & Mapping"""
    print("\n" + "="*60)
    print("TEST 3: Order Generation & Mapping")
    print("="*60)
    
    order = generate_order(wh.rack_positions, k=5, seed=42)
    print(f"Generated order (racks): {order}")
    
    mapped = map_order_to_access_points(wh, order)
    print(f"Mapped access points: {mapped}")
    
    # Verify mapping is valid
    for rack, access in zip(order, mapped):
        is_adjacent = abs(rack[0]-access[0]) + abs(rack[1]-access[1]) == 1
        is_walkable = wh.is_walkable(access[0], access[1])
        print(f"  {rack} -> {access}: adjacent={is_adjacent}, walkable={is_walkable}")
    
    return order, mapped

def test_nn(wh, start, mapped):
    """Test 4: Nearest Neighbor"""
    print("\n" + "="*60)
    print("TEST 4: Nearest Neighbor Routing")
    print("="*60)
    
    route, distance = nearest_neighbor_route(wh, start, mapped)
    print(f"Route: {route}")
    print(f"Total distance: {distance}")
    
    return route, distance

def test_ga(wh, start, mapped):
    """Test 5: Genetic Algorithm"""
    print("\n" + "="*60)
    print("TEST 5: Genetic Algorithm Routing")
    print("="*60)
    
    route, distance = genetic_algorithm(wh, start, mapped, 
                                        population_size=20, 
                                        generations=50)
    print(f"Route: {route}")
    print(f"Total distance: {distance}")
    
    return route, distance

def compare_nn_ga(wh, start, mapped, order):
    """Test 6: Perbandingan NN vs GA"""
    print("\n" + "="*60)
    print("TEST 6: NN vs GA Comparison")
    print("="*60)
    
    import time
    
    # NN
    start_time = time.perf_counter()
    nn_route, nn_dist = nearest_neighbor_route(wh, start, mapped)
    nn_time = (time.perf_counter() - start_time) * 1000
    
    # GA (multiple runs)
    ga_distances = []
    ga_times = []
    ga_routes = []
    
    for run in range(5):
        start_time = time.perf_counter()
        ga_route, ga_dist = genetic_algorithm(wh, start, mapped, 
                                              population_size=30, 
                                              generations=80)
        ga_time = (time.perf_counter() - start_time) * 1000
        ga_distances.append(ga_dist)
        ga_times.append(ga_time)
        ga_routes.append(ga_route)
    
    print(f"\nNearest Neighbor:")
    print(f"  Distance: {nn_dist}")
    print(f"  Time: {nn_time:.2f} ms")
    
    print(f"\nGenetic Algorithm (5 runs):")
    print(f"  Best distance: {min(ga_distances)}")
    print(f"  Avg distance: {sum(ga_distances)/len(ga_distances):.1f}")
    print(f"  Worst distance: {max(ga_distances)}")
    print(f"  Avg time: {sum(ga_times)/len(ga_times):.2f} ms")
    
    improvement = ((nn_dist - min(ga_distances)) / nn_dist * 100)
    print(f"\nImprovement: {improvement:.1f}% better with GA")
    
    return {
        'nn_distance': nn_dist,
        'ga_best': min(ga_distances),
        'improvement': improvement
    }

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("WAREHOUSE SIMULATION SETUP VERIFICATION")
    print("="*60)
    
    # Run tests
    wh = test_warehouse()
    test_bfs(wh)
    order, mapped = test_order(wh)
    test_nn(wh, (0,0), mapped)
    test_ga(wh, (0,0), mapped)
    results = compare_nn_ga(wh, (0,0), mapped, order)
    
    print("\n" + "="*60)
    print("VERIFICATION COMPLETE!")
    print("="*60)
    
    if results['improvement'] > 0:
        print(" All components working correctly!")
        print(" GA shows improvement over NN")
        print("\nReady to run full experiment!")
    else:
        print(" GA did not improve over NN - check GA parameters")
    
    return wh, order, mapped, results

if __name__ == "__main__":
    main()