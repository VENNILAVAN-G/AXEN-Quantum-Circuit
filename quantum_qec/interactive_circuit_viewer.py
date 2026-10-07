"""
Interactive Quantum Error Correction (QEC) Circuit Viewer
===========================================================
Native Matplotlib GUI with 100% Pure White Background (No Black Screen!)
Features:
- Big Clickable Buttons: [💥 Qubit 0 Error] [💥 Qubit 1 Error] [💥 Qubit 2 Error] [✨ Clean]
- Draws the real Qiskit circuit diagram dynamically using native Matplotlib!
- Live status banner showing Syndrome (s1 s0), Error Location, Correction, and 100% Fidelity!
"""

import sys
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def build_qec_circuit(error_target=0):
    """Builds the 3-qubit bit-flip QEC circuit for a specific error target."""
    qr = QuantumRegister(3, 'data')
    ar = QuantumRegister(2, 'ancilla')
    cr_syn = ClassicalRegister(2, 'syn')
    cr_out = ClassicalRegister(1, 'out')
    
    label = f"Error on Qubit {error_target}" if error_target is not None else "Clean (No Error)"
    qc = QuantumCircuit(qr, ar, cr_syn, cr_out, name=label)

    # 1. State Prep (|1>)
    qc.x(qr[0])
    qc.barrier(label="Prep")

    # 2. Encode
    qc.cx(qr[0], qr[1])
    qc.cx(qr[0], qr[2])
    qc.barrier(label="Encode")

    # 3. Manual Error Strike
    if error_target is not None:
        qc.x(qr[error_target])
    qc.barrier(label=f"Err_Q{error_target}" if error_target is not None else "No_Err")

    # 4. Syndrome Extraction (Ancillas)
    qc.cx(qr[0], ar[0])
    qc.cx(qr[1], ar[0])
    qc.cx(qr[1], ar[1])
    qc.cx(qr[2], ar[1])
    qc.measure(ar[0], cr_syn[0])
    qc.measure(ar[1], cr_syn[1])
    qc.barrier(label="Syndrome")

    # 5. Dynamic Conditional Correction
    with qc.if_test((cr_syn, 1)):
        qc.x(qr[0])
    with qc.if_test((cr_syn, 2)):
        qc.x(qr[2])
    with qc.if_test((cr_syn, 3)):
        qc.x(qr[1])
    qc.barrier(label="Correct")

    # 6. Decode
    qc.cx(qr[0], qr[2])
    qc.cx(qr[0], qr[1])
    qc.measure(qr[0], cr_out[0])

    return qc

class InteractiveQECViewer:
    def __init__(self):
        # Create full screen / large bright white figure
        self.fig = plt.figure(figsize=(13, 7.5), facecolor='white')
        self.fig.canvas.manager.set_window_title("Quantum Error Correction (QEC) Interactive Controller")

        self.current_target = 0

        # Scenario metadata
        self.meta = {
            0: {
                "title": "SCENARIO: Error Injected on Data Qubit 0 (X Gate)",
                "syndrome": "s1 s0 = '01'",
                "syndrome_detail": "Ancilla a0 triggered (Parity mismatch at q0-q1)",
                "action": "Dynamic X(q0) applied automatically!",
                "color": "#dc2626"
            },
            1: {
                "title": "SCENARIO: Error Injected on Data Qubit 1 (X Gate)",
                "syndrome": "s1 s0 = '11'",
                "syndrome_detail": "Both Ancillas a0 and a1 triggered (Parity mismatch at both)",
                "action": "Dynamic X(q1) applied automatically!",
                "color": "#dc2626"
            },
            2: {
                "title": "SCENARIO: Error Injected on Data Qubit 2 (X Gate)",
                "syndrome": "s1 s0 = '10'",
                "syndrome_detail": "Ancilla a1 triggered (Parity mismatch at q1-q2)",
                "action": "Dynamic X(q2) applied automatically!",
                "color": "#dc2626"
            },
            None: {
                "title": "SCENARIO: Clean Quantum State (No Error Injected)",
                "syndrome": "s1 s0 = '00'",
                "syndrome_detail": "Neither ancilla triggered (Both parities match)",
                "action": "No correction required (Pure quantum state preserved)",
                "color": "#16a34a"
            }
        }

        # Setup buttons layout
        self.create_buttons()

        # Circuit draw axis
        self.ax_circ = self.fig.add_axes([0.05, 0.16, 0.90, 0.68])
        self.ax_circ.set_facecolor('white')

        # Status text axis at bottom
        self.ax_status = self.fig.add_axes([0.05, 0.02, 0.90, 0.11])
        self.ax_status.axis('off')

        # Draw default scenario (Qubit 0)
        self.draw_scenario(0)

    def create_buttons(self):
        # 4 big buttons at the top
        btn_y = 0.88
        btn_h = 0.07
        btn_w = 0.18

        # Header Title
        self.fig.text(0.5, 0.96, "Quantum Error Correction (QEC) - Interactive Scenario Explorer",
                      ha='center', va='center', fontsize=14, fontweight='bold', color='#0f172a')

        # Button axes
        self.ax_b0 = self.fig.add_axes([0.08, btn_y, btn_w, btn_h])
        self.ax_b1 = self.fig.add_axes([0.28, btn_y, btn_w, btn_h])
        self.ax_b2 = self.fig.add_axes([0.48, btn_y, btn_w, btn_h])
        self.ax_bn = self.fig.add_axes([0.68, btn_y, btn_w, btn_h])

        self.btn0 = Button(self.ax_b0, '💥 Qubit 0 Error', color='#fee2e2', hovercolor='#fca5a5')
        self.btn1 = Button(self.ax_b1, '💥 Qubit 1 Error', color='#fee2e2', hovercolor='#fca5a5')
        self.btn2 = Button(self.ax_b2, '💥 Qubit 2 Error', color='#fee2e2', hovercolor='#fca5a5')
        self.btnn = Button(self.ax_bn, '✨ Clean (No Error)', color='#dcfce7', hovercolor='#86efac')

        self.btn0.label.set_fontsize(10)
        self.btn0.label.set_fontweight('bold')
        self.btn0.label.set_color('#991b1b')

        self.btn1.label.set_fontsize(10)
        self.btn1.label.set_fontweight('bold')
        self.btn1.label.set_color('#991b1b')

        self.btn2.label.set_fontsize(10)
        self.btn2.label.set_fontweight('bold')
        self.btn2.label.set_color('#991b1b')

        self.btnn.label.set_fontsize(10)
        self.btnn.label.set_fontweight('bold')
        self.btnn.label.set_color('#166534')

        # Connect callbacks
        self.btn0.on_clicked(lambda event: self.draw_scenario(0))
        self.btn1.on_clicked(lambda event: self.draw_scenario(1))
        self.btn2.on_clicked(lambda event: self.draw_scenario(2))
        self.btnn.on_clicked(lambda event: self.draw_scenario(None))

    def draw_scenario(self, target):
        self.current_target = target
        m = self.meta[target]

        # Highlight active button
        self.btn0.color = '#dc2626' if target == 0 else '#fee2e2'
        self.btn0.label.set_color('white' if target == 0 else '#991b1b')

        self.btn1.color = '#dc2626' if target == 1 else '#fee2e2'
        self.btn1.label.set_color('white' if target == 1 else '#991b1b')

        self.btn2.color = '#dc2626' if target == 2 else '#fee2e2'
        self.btn2.label.set_color('white' if target == 2 else '#991b1b')

        self.btnn.color = '#16a34a' if target is None else '#dcfce7'
        self.btnn.label.set_color('white' if target is None else '#166534')

        # Clear and redraw circuit axis
        self.ax_circ.clear()
        self.ax_circ.set_facecolor('white')

        # Generate fresh Qiskit circuit
        qc = build_qec_circuit(target)
        
        # Draw circuit into our axis using Qiskit's matplotlib drawer
        qc.draw(output='mpl', ax=self.ax_circ, style='iqp')

        # Update bottom status text
        self.ax_status.clear()
        self.ax_status.axis('off')

        # Status text boxes
        status_box = dict(boxstyle='round,pad=0.5', facecolor='#f8fafc', edgecolor='#cbd5e1', lw=1.5)
        text_str = (
            f"{m['title']}\n"
            f"• Parity Syndrome Extracted: {m['syndrome']}  ({m['syndrome_detail']})\n"
            f"• Recovery Action: {m['action']}  |  State Recovery Success: 100.0% FIDELITY!"
        )
        self.ax_status.text(0.01, 0.5, text_str, fontsize=10.5, fontweight='bold',
                            va='center', color='#0f172a', bbox=status_box)

        self.fig.canvas.draw_idle()

def main():
    viewer = InteractiveQECViewer()
    plt.show()

if __name__ == "__main__":
    main()
