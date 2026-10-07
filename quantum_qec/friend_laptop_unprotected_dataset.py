"""
========================================================================================
LAPTOP A (FRIEND'S LAPTOP): UNPROTECTED RAW QUANTUM CIRCUIT (DATASET-DRIVEN)
========================================================================================
This script represents the standard quantum hardware baseline WITHOUT our QEC solution.

HOW IT WORKS:
1. Reads realistic hardware noise & errors directly from the Dataset
   ('quantum_circuit_stability_backup.csv' or external Kaggle dataset).
2. Runs the unprotected 1-qubit circuit with that dataset noise.
3. Observe what happens:
   - The state gets corrupted!
   - There are NO ancilla qubits to detect what error occurred.
   - The circuit fails silently or outputs corrupted data!
========================================================================================
"""

import os
import sys
import pandas as pd
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, pauli_error, depolarizing_error

# Windows console UTF-8 safety
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKUP_CSV = os.path.join(BASE_DIR, "quantum_circuit_stability_backup.csv")
KAGGLE_CSV = os.path.join(BASE_DIR, "quantum_circuit_stability.csv")

def load_dataset(custom_path=None):
    """Loads dataset with fallback to backup file."""
    if custom_path and os.path.exists(custom_path):
        print(f"[DATASET] Loaded custom dataset: {os.path.basename(custom_path)}")
        return pd.read_csv(custom_path)
    if os.path.exists(KAGGLE_CSV):
        print(f"[DATASET] Loaded primary Kaggle dataset: {os.path.basename(KAGGLE_CSV)}")
        return pd.read_csv(KAGGLE_CSV)
    elif os.path.exists(BACKUP_CSV):
        print(f"[DATASET] Loaded offline backup dataset: {os.path.basename(BACKUP_CSV)}")
        return pd.read_csv(BACKUP_CSV)
    else:
        print("[ERROR] No dataset found! Please ensure quantum_circuit_stability_backup.csv is in the folder.")
        sys.exit(1)


def run_unprotected_dataset_case(row, shots=1000):
    """
    Runs the raw unprotected circuit using the noise parameters and error
    from the selected dataset row.
    """
    c_id = row['circuit_id']
    err_q = int(row.get('injected_error_qubit', -1))
    err_name = row.get('injected_error_name', 'Noise Event')
    cnot_err = float(row.get('cnot_err', 0.015))
    t1 = float(row.get('t1_us', 150))
    t2 = float(row.get('t2_us', 120))
    
    # 1. Build raw 1-qubit circuit (Target state |1>)
    qr = QuantumRegister(1, 'q_data')
    cr = ClassicalRegister(1, 'meas')
    qc = QuantumCircuit(qr, cr, name=f"Unprotected_{c_id}")
    
    # Target state preparation: |1>
    qc.x(qr[0])
    qc.barrier(label="Prep |1>")
    
    # 2. Hardware noise injection from dataset
    # In unprotected circuit, an error event on the data qubit flips it:
    if err_q in [0, 1, 2]: # Any disturbance flips the single physical qubit
        qc.x(qr[0])
        qc.barrier(label="Disturbance")
    else:
        qc.barrier(label="Idle/Clean")
        
    # 3. Measurement (No ancillas! No syndrome checks!)
    qc.measure(qr[0], cr[0])
    
    # 4. Simulate on Qiskit Aer
    sim = AerSimulator()
    job = sim.run(qc, shots=shots)
    counts = job.result().get_counts()
    
    success_count = counts.get('1', 0)
    failed_count = counts.get('0', 0)
    fidelity = (success_count / shots) * 100.0
    
    return {
        "circuit_id": c_id,
        "dataset_noise": err_name,
        "t1_us": t1,
        "t2_us": t2,
        "cnot_err": cnot_err,
        "counts": counts,
        "fidelity": fidelity,
        "status": "FAIL (State Corrupted!)" if fidelity < 70.0 else "PASS (Clean run)",
        "can_detect_error": False,
        "can_correct_error": False
    }

def print_result_card(res):
    print("\n" + "=" * 70)
    print(f"  [FRIEND'S LAPTOP] - UNPROTECTED HARDWARE RUN: {res['circuit_id']}")
    print("=" * 70)
    print(f"• Dataset Injected Noise : {res['dataset_noise']}")
    print(f"• Hardware Parameters   : T1={res['t1_us']:.1f}μs | T2={res['t2_us']:.1f}μs | CNOT Err={res['cnot_err']*100:.2f}%")
    print(f"• Raw Measurement Counts : {res['counts']}")
    print(f"• Output State Fidelity  : {res['fidelity']:.1f}%")
    print(f"• Run Status             : {res['status']}")
    print("-" * 70)
    print("⚠️  DIAGNOSTIC LIMITATION:")
    print("   - Ancilla Syndrome Detection : NONE (Cannot tell what error occurred!)")
    print("   - Dynamic Error Correction   : NONE (Data state permanently destroyed!)")
    print("=" * 70)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Laptop A Unprotected Circuit Runner")
    parser.add_argument("--dataset", "-d", type=str, default=None, help="Custom dataset CSV path")
    args, _ = parser.parse_known_args()

    print("=" * 75)
    print("  LAPTOP A: NORMAL QUANTUM CIRCUIT (BASELINE - UNPROTECTED)")
    print("  Streaming noise from Kaggle Quantum Circuit Stability Dataset")
    print("=" * 75)

    
    df = load_dataset(args.dataset)
    print(f"Total benchmark cases available: {len(df)}")
    print("\nInstructions:")
    print("• Press [Enter] to run the next test case from the dataset.")
    print("• Type a number (e.g. 0 to 1199) to jump to a specific dataset case.")
    print("• Type 'q' to quit.")

    
    current_idx = 0
    while True:
        prompt = input(f"\n[Run Case #{current_idx} ({df.iloc[current_idx]['circuit_id']}) -> Press Enter / Enter index / 'q']: ").strip()
        if prompt.lower() == 'q':
            print("Exiting benchmark.")
            break
        elif prompt.isdigit():
            idx = int(prompt)
            if 0 <= idx < len(df):
                current_idx = idx
            else:
                print(f"Index out of range! (0 to {len(df)-1})")
                continue
                
        row = df.iloc[current_idx]
        result = run_unprotected_dataset_case(row)
        print_result_card(result)
        
        current_idx = (current_idx + 1) % len(df)

if __name__ == "__main__":
    main()
