# main.py
from models.warehouse import Warehouse
from utils.distance import bfs_distance
from utils.order import generate_order, map_order_to_access_points
from routing.nn import nearest_neighbor_route
from routing.ga import genetic_algorithm
from utils.debug import (
    debug_bfs_basic,
    debug_reachability,
    debug_mapping,
    debug_route,
    debug_total_distance
)
import time
import argparse

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Warehouse Routing Simulation')
    parser.add_argument('--algo', type=str, default='nn', choices=['nn', 'ga', 'both'],
                        help='Algorithm to use: nn, ga, or both')
    parser.add_argument('--order-size', type=int, default=5,
                        help='Number of items in order')
    parser.add_argument('--seed', type=int, default=42,
                        help='Random seed for reproducibility')
    args = parser.parse_args()
    
    # Initialize warehouse
    wh = Warehouse(10, 10)
    wh.generate_layout()
    wh.display()
    
    start = (0, 0)
    
    # Generate order
    print(f"\nGenerating order with {args.order_size} items (seed={args.seed})")
    order = generate_order(wh.rack_positions, k=args.order_size, seed=args.seed)
    print("Order (racks):", order)
    
    # Map to access points
    mapped = map_order_to_access_points(wh, order)
    print("Mapped access points:", mapped)
    
    # Run selected algorithm
    if args.algo in ['nn', 'both']:
        print("\n" + "="*50)
        print("NEAREST NEIGHBOR")
        print("="*50)
        start_time = time.perf_counter()
        nn_route, nn_distance = nearest_neighbor_route(wh, start, mapped)
        nn_time = (time.perf_counter() - start_time) * 1000
        print(f"Route: {nn_route}")
        print(f"Total distance: {nn_distance}")
        print(f"Time: {nn_time:.2f} ms")
    
    if args.algo in ['ga', 'both']:
        print("\n" + "="*50)
        print("GENETIC ALGORITHM")
        print("="*50)
        start_time = time.perf_counter()
        ga_route, ga_distance = genetic_algorithm(
            wh, start, mapped,
            population_size=50,
            generations=100,
            mutation_rate=0.1,
            elite_size=2,
            early_stop_patience=30
        )
        ga_time = (time.perf_counter() - start_time) * 1000
        print(f"Route: {ga_route}")
        print(f"Total distance: {ga_distance}")
        print(f"Time: {ga_time:.2f} ms")
    
    # Comparison if both run
    if args.algo == 'both':
        print("\n" + "="*50)
        print("COMPARISON")
        print("="*50)
        improvement = ((nn_distance - ga_distance) / nn_distance * 100)
        print(f"NN distance: {nn_distance}")
        print(f"GA distance: {ga_distance}")
        print(f"Improvement: {improvement:.1f}%")
        print(f"NN time: {nn_time:.2f} ms")
        print(f"GA time: {ga_time:.2f} ms")
        print(f"GA is {ga_time/nn_time:.1f}x slower")
    
    # Debug phase (optional)
    if args.algo == 'nn':
        debug_bfs_basic(wh, bfs_distance)
        debug_reachability(wh, bfs_distance, mapped)
        debug_mapping(order, mapped)
        debug_route(nn_route, mapped)
        recomputed = debug_total_distance(wh, bfs_distance, nn_route)
        print(f"\nOriginal total: {nn_distance}")
        print(f"Recomputed total: {recomputed}")

if __name__ == "__main__":
    main()