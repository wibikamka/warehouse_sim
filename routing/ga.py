from utils.distance import bfs_distance
import random
import copy

def total_distance(warehouse, start, route):
    total = 0
    current = start
    for point in route:
        total += bfs_distance(warehouse, current, point)
        current = point
    total += bfs_distance(warehouse, current, start)
    return total

def fitness(warehouse, start, route):
    return 1 / total_distance(warehouse, start, route)

def tournament_selection(population, warehouse, start, k=3):
    """Tournament selection untuk diversity lebih baik"""
    tournament = random.sample(population, k)
    tournament.sort(key=lambda r: total_distance(warehouse, start, r))
    return tournament[0]  # Return terbaik dari tournament

def crossover(parent1, parent2):
    """Order crossover (OX) - sudah benar"""
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [None]*size
    
    child[start:end+1] = parent1[start:end+1]
    
    p2_index = 0
    for i in range(size):
        if child[i] is None:
            while parent2[p2_index] in child:
                p2_index += 1
            child[i] = parent2[p2_index]
    return child

def mutate(route, mutation_rate=0.1):
    """Swap mutation - sudah benar"""
    route = route.copy()
    for i in range(len(route)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(route)-1)
            route[i], route[j] = route[j], route[i]
    return route

def genetic_algorithm(warehouse, start, targets, 
                     population_size=100,  # Increased
                     generations=200, 
                     mutation_rate=0.1,
                     elite_size=2,  # New: elitism
                     early_stop_patience=30):
    
    # Initial population
    population = [random.sample(targets, len(targets)) for _ in range(population_size)]
    
    best_distance = float('inf')
    best_route = None
    no_improve_count = 0
    best_history = []
    
    for gen in range(generations):
        # Evaluate fitness
        fitnesses = [fitness(warehouse, start, route) for route in population]
        
        # Sort by distance (better = smaller distance)
        sorted_pop = sorted(population, key=lambda r: total_distance(warehouse, start, r))
        current_best_distance = total_distance(warehouse, start, sorted_pop[0])
        
        # Track improvement
        if current_best_distance < best_distance:
            best_distance = current_best_distance
            best_route = sorted_pop[0].copy()
            no_improve_count = 0
            print(f"Gen {gen}: New best distance = {best_distance}")
        else:
            no_improve_count += 1
        
        # Early stopping
        if no_improve_count >= early_stop_patience:
            print(f"Early stopping at generation {gen}")
            break
        
        # Elitism: keep best routes
        new_population = sorted_pop[:elite_size]
        
        # Crossover & mutation untuk mengisi populasi
        while len(new_population) < population_size:
            parent1 = tournament_selection(population, warehouse, start)
            parent2 = tournament_selection(population, warehouse, start)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            new_population.append(child)
        
        population = new_population
    
    return best_route, best_distance