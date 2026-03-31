# simulation/run_experiment.py
"""Eksperimen NN vs GA pada berbagai warehouse dan order size"""

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.warehouse import Warehouse
from utils.order import generate_order, map_order_to_access_points
from routing.nn import nearest_neighbor_route
from routing.ga import genetic_algorithm
from simulation.config import ExperimentConfig
import time
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# Set style untuk grafik
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("Set2")

def create_visualizations(df, results_dir):
    """Buat semua grafik dari hasil eksperimen"""
    
    print("\n  Membuat grafik...")
    
    # ========== GRAFIK 1: Distance Comparison (Line Plot) ==========
    plt.figure(figsize=(10, 6))
    
    summary = df.groupby('order_size').agg({
        'nn_distance': 'mean',
        'ga_distance': 'mean'
    }).reset_index()
    
    plt.plot(summary['order_size'], summary['nn_distance'], 'o-', 
             linewidth=2, markersize=8, label='Nearest Neighbor (NN)', color='#E74C3C')
    plt.plot(summary['order_size'], summary['ga_distance'], 's-', 
             linewidth=2, markersize=8, label='Genetic Algorithm (GA)', color='#2ECC71')
    
    plt.xlabel('Order Size (Number of Items)', fontsize=12)
    plt.ylabel('Total Distance', fontsize=12)
    plt.title('NN vs GA: Total Distance Comparison', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(results_dir / '1_distance_comparison.png', dpi=150)
    plt.close()
    print("     1_distance_comparison.png")
    
    # ========== GRAFIK 2: Improvement Percentage (Bar Plot) ==========
    plt.figure(figsize=(10, 6))
    
    improvement = df.groupby('order_size')['improvement_pct'].mean().reset_index()
    colors = ['#2ECC71' if x > 0 else '#E74C3C' for x in improvement['improvement_pct']]
    
    bars = plt.bar(improvement['order_size'].astype(str), improvement['improvement_pct'], 
                   color=colors, edgecolor='black', alpha=0.7)
    plt.axhline(y=0, color='black', linestyle='-', linewidth=1)
    plt.xlabel('Order Size', fontsize=12)
    plt.ylabel('Improvement (%)', fontsize=12)
    plt.title('GA Improvement over NN', fontsize=14, fontweight='bold')
    
    # Tambahkan nilai di atas bar
    for bar, imp in zip(bars, improvement['improvement_pct']):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{imp:.1f}%', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(results_dir / '2_improvement_percentage.png', dpi=150)
    plt.close()
    print("     2_improvement_percentage.png")
    
    # ========== GRAFIK 3: Time Comparison (Line Plot) ==========
    plt.figure(figsize=(10, 6))
    
    time_summary = df.groupby('order_size').agg({
        'nn_time_ms': 'mean',
        'ga_time_ms': 'mean'
    }).reset_index()
    
    plt.plot(time_summary['order_size'], time_summary['nn_time_ms'], 'o-', 
             linewidth=2, markersize=8, label='NN (ms)', color='#E74C3C')
    plt.plot(time_summary['order_size'], time_summary['ga_time_ms'], 's-', 
             linewidth=2, markersize=8, label='GA (ms)', color='#3498DB')
    
    plt.xlabel('Order Size', fontsize=12)
    plt.ylabel('Time (milliseconds)', fontsize=12)
    plt.title('Computation Time: NN vs GA', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(results_dir / '3_time_comparison.png', dpi=150)
    plt.close()
    print("     3_time_comparison.png")
    
    # ========== GRAFIK 4: Box Plot Distribusi Improvement ==========
    plt.figure(figsize=(10, 6))
    
    # Siapkan data untuk box plot
    box_data = []
    order_sizes = sorted(df['order_size'].unique())
    for size in order_sizes:
        improvements = df[df['order_size'] == size]['improvement_pct'].values
        box_data.append(improvements)
    
    bp = plt.boxplot(box_data, tick_labels=[str(s) for s in order_sizes], patch_artist=True, showmeans=True)
    
    # Warna box plot
    for box in bp['boxes']:
        box.set_facecolor('#2ECC71')
        box.set_alpha(0.7)
    
    plt.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.5)
    plt.xlabel('Order Size', fontsize=12)
    plt.ylabel('Improvement (%)', fontsize=12)
    plt.title('Distribution of GA Improvement Across Multiple Runs', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(results_dir / '4_improvement_distribution.png', dpi=150)
    plt.close()
    print("     4_improvement_distribution.png")
    
    # ========== GRAFIK 5: Heatmap Improvement per Warehouse ==========
    plt.figure(figsize=(10, 8))
    
    # Buat pivot table
    heatmap_data = df.pivot_table(
        values='improvement_pct',
        index='warehouse_width',
        columns='order_size',
        aggfunc='mean'
    )
    
    sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='RdYlGn', center=0,
                linewidths=0.5, linecolor='gray')
    plt.title('GA Improvement by Warehouse Size and Order Size (%)', fontsize=14, fontweight='bold')
    plt.xlabel('Order Size', fontsize=12)
    plt.ylabel('Warehouse Width', fontsize=12)
    plt.tight_layout()
    plt.savefig(results_dir / '5_improvement_heatmap.png', dpi=150)
    plt.close()
    print("     5_improvement_heatmap.png")

def run_experiment():
    """Jalankan eksperimen untuk semua konfigurasi"""
    
    config = ExperimentConfig()
    
    # Buat folder results jika belum ada
    results_dir = Path(config.RESULTS_DIR)
    results_dir.mkdir(parents=True, exist_ok=True)
    
    results = []
    
    print("="*80)
    print("EXPERIMEN: NN vs GA")
    print("="*80)
    
    if config.QUICK_TEST:
        print("  QUICK TEST MODE (hanya 1 warehouse, 1 seed)")
    else:
        print(f"Warehouse sizes: {config.WAREHOUSE_SIZES}")
        print(f"Order sizes: {config.ORDER_SIZES}")
        print(f"Seeds per config: {len(config.RANDOM_SEEDS)}")
    
    print(f"Results will be saved to: {results_dir}")
    print("="*80)
    
    # Get active config
    active = config.get_active_config()
    warehouse_sizes = active['warehouse_sizes']
    order_sizes = active['order_sizes']
    random_seeds = active['random_seeds']
    ga_pop = active['ga_population_size']
    ga_gen = active['ga_generations']
    
    total_exp = len(warehouse_sizes) * len(order_sizes) * len(random_seeds)
    exp_count = 0
    
    for width, height in warehouse_sizes:
        print(f"\n{'='*60}")
        print(f"WAREHOUSE: {width} x {height}")
        print(f"{'='*60}")
        
        wh = Warehouse(width, height)
        wh.generate_layout()
        start = (0, 0)
        rack_count = len(wh.rack_positions)
        print(f"Jumlah rack: {rack_count}")
        
        for order_size in order_sizes:
            if order_size > rack_count:
                print(f"  Skip order size {order_size} > racks {rack_count}")
                continue
                
            print(f"\n  Order Size: {order_size}")
            
            for seed in random_seeds:
                exp_count += 1
                
                # Generate order
                order = generate_order(wh.rack_positions, k=order_size, seed=seed)
                mapped = map_order_to_access_points(wh, order)
                
                # RUN NEAREST NEIGHBOR
                start_time = time.perf_counter()
                nn_route, nn_distance = nearest_neighbor_route(wh, start, mapped)
                nn_time = (time.perf_counter() - start_time) * 1000
                
                # RUN GENETIC ALGORITHM
                start_time = time.perf_counter()
                ga_route, ga_distance = genetic_algorithm(
                    wh, start, mapped,
                    population_size=ga_pop,
                    generations=ga_gen,
                    mutation_rate=config.GA_MUTATION_RATE,
                    elite_size=config.GA_ELITE_SIZE,
                    early_stop_patience=config.GA_EARLY_STOP_PATIENCE
                )
                ga_time = (time.perf_counter() - start_time) * 1000
                
                # Hitung improvement
                improvement = ((nn_distance - ga_distance) / nn_distance * 100) if nn_distance > 0 else 0
                
                # Simpan hasil
                results.append({
                    'warehouse_width': width,
                    'warehouse_height': height,
                    'rack_count': rack_count,
                    'order_size': order_size,
                    'seed': seed,
                    'nn_distance': nn_distance,
                    'nn_time_ms': nn_time,
                    'ga_distance': ga_distance,
                    'ga_time_ms': ga_time,
                    'improvement_pct': improvement,
                    'ga_better': ga_distance < nn_distance
                })
                
                # Progress report
                if ga_distance < nn_distance:
                    status = " GA BETTER"
                elif ga_distance == nn_distance:
                    status = "  SAME"
                else:
                    status = " NN BETTER"
                    
                print(f"    [{exp_count}/{total_exp}] Seed {seed}: NN={nn_distance}, GA={ga_distance}, Imp={improvement:.1f}% {status}")
    
    # ========== KONVERSI KE DATAFRAME ==========
    df = pd.DataFrame(results)
    
    # ========== SIMPAN RAW RESULTS ==========
    raw_path = results_dir / 'raw_results.csv'
    df.to_csv(raw_path, index=False)
    print(f"\n Raw results saved to: {raw_path}")
    
    # ========== BUAT RINGKASAN ==========
    print("\n" + "="*80)
    print("RINGKASAN PER ORDER SIZE")
    print("="*80)
    
    summary = df.groupby('order_size').agg({
        'nn_distance': ['mean', 'std', 'min', 'max'],
        'ga_distance': ['mean', 'std', 'min', 'max'],
        'improvement_pct': ['mean', 'std', 'min', 'max'],
        'ga_better': 'sum',
        'nn_time_ms': 'mean',
        'ga_time_ms': 'mean'
    }).round(2)
    
    # Flatten column names
    summary.columns = ['NN_Mean', 'NN_Std', 'NN_Min', 'NN_Max',
                       'GA_Mean', 'GA_Std', 'GA_Min', 'GA_Max',
                       'Imp_Mean', 'Imp_Std', 'Imp_Min', 'Imp_Max',
                       'GA_Wins', 'NN_Time_ms', 'GA_Time_ms']
    
    print(summary.to_string())
    
    # Simpan summary
    summary_path = results_dir / 'summary.csv'
    summary.to_csv(summary_path)
    print(f"\n Summary saved to: {summary_path}")
    
    # ========== BUAT VISUALISASI ==========
    create_visualizations(df, results_dir)
    
    # ========== KESIMPULAN AKHIR ==========
    print("\n" + "="*80)
    print("KESIMPULAN")
    print("="*80)
    
    total_wins = df['ga_better'].sum()
    total_instances = len(df)
    win_percentage = total_wins / total_instances * 100
    
    # Rata-rata improvement untuk order size besar (>8)
    large_orders = df[df['order_size'] >= 8]
    avg_improvement_large = large_orders['improvement_pct'].mean() if len(large_orders) > 0 else 0
    
    print(f"\n STATISTIK:")
    print(f"   Total eksperimen: {total_instances}")
    print(f"   GA lebih baik: {total_wins}/{total_instances} ({win_percentage:.0f}%)")
    print(f"   Rata-rata improvement (order >=8): {avg_improvement_large:.1f}%")
    
    print(f"\n OUTPUT FILES:")
    print(f"   1. {results_dir / 'raw_results.csv'} - Data mentah")
    print(f"   2. {results_dir / 'summary.csv'} - Ringkasan statistik")
    print(f"   3. {results_dir / '1_distance_comparison.png'} - Grafik perbandingan jarak")
    print(f"   4. {results_dir / '2_improvement_percentage.png'} - Grafik improvement")
    print(f"   5. {results_dir / '3_time_comparison.png'} - Grafik waktu komputasi")
    print(f"   6. {results_dir / '4_improvement_distribution.png'} - Distribusi improvement")
    print(f"   7. {results_dir / '5_improvement_heatmap.png'} - Heatmap improvement")
    
    if avg_improvement_large > 5:
        print(f"\n KESIMPULAN UNTUK PAPER:")
        print(f"   GA menghasilkan rute {avg_improvement_large:.1f}% lebih pendek untuk order >=8 item")
        print(f"   Trade-off: GA {df['ga_time_ms'].mean()/df['nn_time_ms'].mean():.0f}x lebih lambat")
        print(f"   Rekomendasi: GA untuk order besar (>8), NN untuk order kecil")
    else:
        print(f"\n  Perlu tuning GA parameter untuk improvement yang lebih baik")
    
    return df

if __name__ == "__main__":
    results_df = run_experiment()
    print("\n Eksperimen selesai!")