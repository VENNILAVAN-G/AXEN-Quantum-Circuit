"""
Master Runner for QEC Hackathon Project
========================================
Runs:
1. Manual Error Injection & Clearing Demo
2. Noise Model & Baseline Benchmark
3. Visualizations & Circuit Diagrams Generation
"""

import os
import subprocess
import sys

def run_script(script_name):
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    print("\n" + "#" * 80)
    print(f"  RUNNING: {script_name}")
    print("#" * 80)
    res = subprocess.run([sys.executable, script_path], capture_output=False, text=True)
    if res.returncode != 0:
        print(f"Error running {script_name} (Code {res.returncode})")
    return res.returncode

def main():
    print("=" * 80)
    print("  QUANTUM ERROR CORRECTION (QEC) COMPLETE SUITE")
    print("=" * 80)
    
    run_script("1_manual_qec_demo.py")
    run_script("2_noise_model_simulation.py")
    run_script("3_benchmark_and_visualizations.py")
    run_script("4_dynamic_decoupling_study.py")
    run_script("5_quantum_stability_analysis.py")
    
    print("\n" + "=" * 80)
    print("  ALL BENCHMARKS, SIMULATIONS & VISUALIZATIONS COMPLETED!")
    print("  Check visualizations/ for exported figures & circuit diagrams.")
    print("  Read HACKATHON_REPORT.md for comprehensive answers & presentation pitch.")
    print("=" * 80)

if __name__ == "__main__":
    main()
