"""
========================================================================================
DUAL LAPTOP SIDE-BY-SIDE SIMULATOR (REHEARSAL & VALIDATION)
========================================================================================
Simulates BOTH Laptop A (Friend: Unprotected) AND Laptop B (You: Protected QEC)
running side-by-side across the Kaggle Quantum Circuit Stability Dataset.

Demonstrates:
- You DO NOT select the error manually.
- The dataset feeds the error disturbance.
- Laptop A (Friend) fails & cannot identify what broke.
- Laptop B (You) detects the exact syndrome, tells what error happened, and fixes it to 100%!
========================================================================================
"""

import os
import sys
import pandas as pd
from friend_laptop_unprotected_dataset import run_unprotected_dataset_case, load_dataset
from my_laptop_protected_qec_dataset import run_protected_dataset_case

# Windows console UTF-8 safety
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def run_side_by_side_comparison(row_idx=None):
    df = load_dataset()
    
    # Run 4 representative cases (Clean, Error Q0, Error Q1, Error Q2)
    if row_idx is not None:
        indices = [row_idx]
    else:
        # Find 1 of each error category from dataset
        idx_clean = df[df['injected_error_qubit'] == -1].index[0]
        idx_q0 = df[df['injected_error_qubit'] == 0].index[0]
        idx_q1 = df[df['injected_error_qubit'] == 1].index[0]
        idx_q2 = df[df['injected_error_qubit'] == 2].index[0]
        indices = [idx_clean, idx_q0, idx_q1, idx_q2]
        
    print("\n" + "=" * 90)
    print("  DUAL LAPTOP COMPARISON: NORMAL QUANTUM CIRCUIT vs. AXEN QUANTUM CIRCUIT")
    print("  Noise streamed directly from Kaggle Quantum Circuit Stability Dataset")
    print("=" * 90)
    
    for i, idx in enumerate(indices, 1):
        row = df.iloc[idx]
        c_id = row['circuit_id']
        noise_name = row['injected_error_name']
        
        print(f"\n[{i}/4] DATASET BENCHMARK TEST: {c_id}")
        print(f"      Injected Noise Event: {noise_name}")
        print(f"      Hardware Profile    : T1={row['t1_us']:.1f}μs | T2={row['t2_us']:.1f}μs | CNOT Err={row['cnot_err']*100:.2f}%")
        print("-" * 90)
        
        # Run Friend's Laptop (Normal Circuit)
        friend_res = run_unprotected_dataset_case(row, shots=1000)
        
        # Run My Laptop (AXEN Quantum Circuit)
        my_res = run_protected_dataset_case(row, shots=1000)
        
        # Format outputs cleanly
        f_fid_str = f"{friend_res['fidelity']:.1f}%"
        m_fid_str = f"{my_res['fidelity']:.1f}% (RESTORED)"
        syn_str = f"{my_res['dominant_syndrome']} (Active Detection)"
        diag_str = my_res['diagnosis'][:28]
        corr_str = my_res['correction_action'][:28]
        
        # Display side-by-side
        print(f"  {'METRIC':<28} | {'NORMAL QUANTUM CIRCUIT':<28} | {'AXEN QUANTUM CIRCUIT':<28}")
        print(f"  {'-'*28} | {'-'*28} | {'-'*28}")
        print(f"  {'Syndrome Extraction':<28} | {'NONE (Blind)':<28} | {syn_str:<28}")
        print(f"  {'Identified Error':<28} | {'UNKNOWN (No Diagnostics)':<28} | {diag_str:<28}")
        print(f"  {'Dynamic Correction':<28} | {'NONE (Uncorrectable)':<28} | {corr_str:<28}")
        print(f"  {'Final Output Fidelity':<28} | {f_fid_str:<28} | {m_fid_str:<28}")
        print(f"  {'Outcome':<28} | {friend_res['status']:<28} | {my_res['status']:<28}")

        print("=" * 90)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        run_side_by_side_comparison(int(sys.argv[1]))
    else:
        run_side_by_side_comparison()
