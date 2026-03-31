# simulation/config.py
"""Konfigurasi untuk eksperimen warehouse"""

class ExperimentConfig:
    """Semua parameter eksperimen di sini"""
    
    # ========== EKSPERIMEN PARAMETERS ==========
    
    # Warehouse sizes (width, height)
    WAREHOUSE_SIZES = [
        (10, 10),   # Small
        (15, 15),   # Medium
        (20, 20),   # Large
    ]
    
    # Order sizes (number of items to pick)
    ORDER_SIZES = [5, 8, 10, 12, 15]
    
    # Random seeds untuk reproducibility (3 seeds per config)
    RANDOM_SEEDS = [42, 123, 456]
    
    # ========== GA PARAMETERS ==========
    
    GA_POPULATION_SIZE = 50
    GA_GENERATIONS = 100
    GA_MUTATION_RATE = 0.1
    GA_ELITE_SIZE = 2
    GA_EARLY_STOP_PATIENCE = 30
    
    # ========== OUTPUT ==========
    
    SAVE_RESULTS = True
    RESULTS_DIR = "simulation/results"
    VERBOSE = True
    
    # ========== QUICK TEST MODE ==========
    # Set ke True untuk testing cepat (hanya 1 seed, order size kecil)
    QUICK_TEST = False
    
    @classmethod
    def get_active_config(cls):
        """Return config berdasarkan mode (quick test atau full)"""
        if cls.QUICK_TEST:
            return {
                'warehouse_sizes': [(10, 10)],
                'order_sizes': [5, 8],
                'random_seeds': [42],
                'ga_population_size': 20,
                'ga_generations': 50,
            }
        else:
            return {
                'warehouse_sizes': cls.WAREHOUSE_SIZES,
                'order_sizes': cls.ORDER_SIZES,
                'random_seeds': cls.RANDOM_SEEDS,
                'ga_population_size': cls.GA_POPULATION_SIZE,
                'ga_generations': cls.GA_GENERATIONS,
            }