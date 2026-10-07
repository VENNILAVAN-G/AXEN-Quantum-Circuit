"""
=============================================================================
UNPROTECTED NORMAL QUANTUM CIRCUIT (BASELINE - WITHOUT QEC SOLUTION)
=============================================================================
This is the standard, unshielded 1-qubit quantum circuit.
It suffers from raw hardware noise and manual errors without any error-correction.

Run this on Laptop A (Normal Circuit) to compare accuracy against Laptop B (QEC Solution).
"""

import sys
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, pauli_error

# Ensure clean Windows console unicode output
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def run_unprotected_experiment(inject_error=True, shots=1000):
    """
    Creates and simulates a normal 1-qubit quantum circuit.
    - Prepares logical state |1>
    - Subjected to manual error (X gate)
    - Measures output
    """
    qr = QuantumRegister(1, 'q')
    cr = ClassicalRegister(1, 'meas')
    qc = QuantumCircuit(qr, cr, name="Unprotected_Normal_Circuit")

    # 1. State Preparation: Prepare target state |1>
    qc.x(qr[0])
    qc.barrier(label="Prep")

    # 2. Environmental Error / Disturbance (Pauli X Bit-Flip)
    if inject_error:
        qc.x(qr[0])  # Error flips |1> to |0>
        qc.barrier(label="Error")
    else:
        qc.barrier(label="Clean")

    # 3. Measurement (No error correction, no ancilla qubits)
    qc.measure(qr[0], cr[0])

    # Run simulation on Qiskit Aer
    sim = AerSimulator()
    job = sim.run(qc, shots=shots)
    counts = job.result().get_counts()

    # Calculate Accuracy / Fidelity for target state |1>
    success_count = counts.get('1', 0)
    failed_count = counts.get('0', 0)
    accuracy = (success_count / shots) * 100.0
    error_rate = 100.0 - accuracy

    return qc, counts, accuracy, error_rate

def run_noise_sweep_experiment(shots=2000):
    """Measures accuracy under increasing physical noise."""
    p_values = [0.01, 0.05, 0.10, 0.15, 0.20]
    print("\n" + "=" * 65)
    print("  PHYSICAL CHANNEL NOISE ACCURACY TEST (UNPROTECTED):")
    print("=" * 65)
    print(f"{'Noise Rate (p)':<18} | {'Accuracy (%)':<16} | {'Error Rate (%)'}")
    print("-" * 65)

    for p in p_values:
        nm = NoiseModel()
        err = pauli_error([('X', p), ('I', 1.0 - p)])
        nm.add_all_qubit_quantum_error(err, ['id'])

        qr = QuantumRegister(1, 'q')
        cr = ClassicalRegister(1, 'c')
        qc = QuantumCircuit(qr, cr)
        qc.x(0)
        qc.id(0) # exposed to noise
        qc.measure(0, 0)

        sim = AerSimulator(noise_model=nm)
        counts = sim.run(qc, shots=shots).result().get_counts()
        acc = (counts.get('1', 0) / shots) * 100.0
        print(f"{p*100:<17.1f}% | {acc:<16.2f}% | {100.0 - acc:.2f}%")

    print("=" * 65)

def main():
    print("=" * 72)
    print("  LAPTOP A: UNPROTECTED NORMAL QUANTUM CIRCUIT (NO QEC)")
    print("========================================================================")
    print("This circuit has NO error detection, NO ancilla qubits, NO correction.")
    print("Watch what happens to accuracy when an error strikes!\n")

    while True:
        print("\nChoose an action:")
        print("  [1] Run with MANUAL ERROR INJECTION (Simulate bit-flip)")
        print("  [2] Run CLEAN (No error)")
        print("  [3] Run NOISE SWEEP (Evaluate hardware noise degradation)")
        print("  [q] Quit")

        choice = input("\nEnter choice [1, 2, 3, or q]: ").strip().lower()

        if choice == 'q':
            print("Exiting. Ready for hackathon comparison!")
            break

        if choice == '1':
            qc, counts, acc, err = run_unprotected_experiment(inject_error=True)
            print("\n" + "-" * 72)
            print("  >>> EXPERIMENT RESULT (MANUAL ERROR INJECTED):")
            print("-" * 72)
            print(f"  • Expected Target State : |1>")
            print(f"  • Raw Measured Output   : {counts}")
            print(f"  • Accuracy / Fidelity   : {acc:.1f}%")
            print(f"  • Error Rate            : {err:.1f}%")
            print(f"  • Status                : ❌ [FAILED] Information completely destroyed!")
            print("-" * 72)
            print("\nCircuit Diagram:")
            print(qc.draw(output='text'))

        elif choice == '2':
            qc, counts, acc, err = run_unprotected_experiment(inject_error=False)
            print("\n" + "-" * 72)
            print("  >>> EXPERIMENT RESULT (CLEAN RUN - NO ERROR):")
            print("-" * 72)
            print(f"  • Expected Target State : |1>")
            print(f"  • Raw Measured Output   : {counts}")
            print(f"  • Accuracy / Fidelity   : {acc:.1f}%")
            print(f"  • Status                : ✅ [PASSED] 100% (Only because no error occurred)")
            print("-" * 72)

        elif choice == '3':
            run_noise_sweep_experiment()

        else:
            print("Invalid input! Enter 1, 2, 3, or q.")

if __name__ == "__main__":
    main()
