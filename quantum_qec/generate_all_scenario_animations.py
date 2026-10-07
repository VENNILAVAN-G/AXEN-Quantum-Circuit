"""
Generate Separate Animations and High-Res Circuit Diagrams for Each Error Scenario:
- Qubit 0 Error (anim_error_q0.gif & circuit_error_q0.png)
- Qubit 1 Error (anim_error_q1.gif & circuit_error_q1.png)
- Qubit 2 Error (anim_error_q2.gif & circuit_error_q2.png)
- No Error Clean (anim_clean.gif & circuit_clean.png)
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import FancyBboxPatch
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "visualizations")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. EXPORT INDIVIDUAL QISKIT CIRCUIT PNGs FOR EACH SCENARIO
# -----------------------------------------------------------------------------
def export_scenario_circuit_images():
    print("[1/2] Generating Specific Qiskit Circuit PNGs for Each Error Scenario...")
    scenarios = [
        (None, "circuit_clean.png", "Clean Circuit (No Error)"),
        (0,    "circuit_error_q0.png", "Error on Data Qubit 0"),
        (1,    "circuit_error_q1.png", "Error on Data Qubit 1"),
        (2,    "circuit_error_q2.png", "Error on Data Qubit 2"),
    ]

    for err_q, fname, label in scenarios:
        qr = QuantumRegister(3, 'data')
        ar = QuantumRegister(2, 'ancilla')
        cr_syn = ClassicalRegister(2, 'syn')
        cr_out = ClassicalRegister(1, 'out')
        qc = QuantumCircuit(qr, ar, cr_syn, cr_out, name=label)

        qc.x(qr[0])
        qc.barrier(label="Prep")

        qc.cx(qr[0], qr[1])
        qc.cx(qr[0], qr[2])
        qc.barrier(label="Encode")

        if err_q is not None:
            qc.x(qr[err_q])
        qc.barrier(label=f"Err_Q{err_q}" if err_q is not None else "No_Err")

        qc.cx(qr[0], ar[0])
        qc.cx(qr[1], ar[0])
        qc.cx(qr[1], ar[1])
        qc.cx(qr[2], ar[1])
        qc.measure(ar[0], cr_syn[0])
        qc.measure(ar[1], cr_syn[1])
        qc.barrier(label="Syndrome")

        with qc.if_test((cr_syn, 1)):
            qc.x(qr[0])
        with qc.if_test((cr_syn, 2)):
            qc.x(qr[2])
        with qc.if_test((cr_syn, 3)):
            qc.x(qr[1])
        qc.barrier(label="Correct")

        qc.cx(qr[0], qr[2])
        qc.cx(qr[0], qr[1])
        qc.measure(qr[0], cr_out[0])

        fig = qc.draw(output='mpl', style='iqp')
        fig.savefig(os.path.join(OUTPUT_DIR, fname), bbox_inches='tight', dpi=300)
        plt.close(fig)
        print(f"      -> Exported: {fname}")

# -----------------------------------------------------------------------------
# 2. GENERATE DEDICATED ANIMATED GIF FOR A GIVEN ERROR SCENARIO
# -----------------------------------------------------------------------------
def generate_scenario_gif(err_target, out_filename, title_text):
    print(f"[2/2] Generating Animated GIF for: {title_text} -> {out_filename}...")
    num_frames = 60
    fig, ax = plt.subplots(figsize=(10, 5.5), facecolor='#0d1117')

    qubits = ['data 0', 'data 1', 'data 2', 'ancilla 0', 'ancilla 1']
    y_coords = [4.0, 3.0, 2.0, 1.0, 0.0]

    def draw_wires():
        ax.clear()
        ax.set_facecolor('#0d1117')
        ax.set_xlim(-0.5, 9.5)
        ax.set_ylim(-0.8, 5.2)
        ax.axis('off')

        for i, (name, y) in enumerate(zip(qubits, y_coords)):
            color = '#30363d' if 'ancilla' in name else '#21262d'
            ax.plot([-0.2, 9.2], [y, y], color='#484f58', linewidth=2, zorder=1)
            label_color = '#58a6ff' if 'data' in name else '#d29922'
            ax.text(-0.4, y, f"|{name}⟩", color=label_color, fontsize=11, fontweight='bold', ha='right', va='center')

        stages = [(0.8, "1. Prep"), (2.2, "2. Encode"), (3.8, "3. Error"), (5.5, "4. Syndrome"), (7.2, "5. Correct"), (8.8, "6. Restored")]
        for x, label in stages:
            ax.axvline(x=x, color='#21262d', linestyle='--', linewidth=1)
            ax.text(x, 4.9, label, color='#8b949e', fontsize=9, ha='center', fontweight='bold')

    def animate(frame):
        draw_wires()
        q_colors = ['#58a6ff', '#58a6ff', '#58a6ff', '#8b949e', '#8b949e']
        status_text = ""
        status_color = '#58a6ff'
        fidelity = 100

        # Phase 1: Prep (0 - 10)
        if frame <= 10:
            x_cursor = 0.8
            ax.add_patch(FancyBboxPatch((0.5, 3.75), 0.6, 0.5, boxstyle="round,pad=0.05", fc='#1f6feb', ec='#58a6ff'))
            ax.text(0.8, 4.0, "X", color='white', fontweight='bold', ha='center', va='center')
            status_text = "Stage 1: State Preparation (|1⟩ prepared on Data 0)"

        # Phase 2: Encode (11 - 20)
        elif 10 < frame <= 20:
            x_cursor = 2.2
            ax.add_patch(FancyBboxPatch((0.5, 3.75), 0.6, 0.5, boxstyle="round,pad=0.05", fc='#1f6feb', ec='#58a6ff'))
            ax.text(0.8, 4.0, "X", color='white', fontweight='bold', ha='center', va='center')
            ax.plot([1.8, 1.8], [4.0, 3.0], color='#58a6ff', lw=2)
            ax.plot([2.2, 2.2], [4.0, 2.0], color='#58a6ff', lw=2)
            ax.plot(1.8, 4.0, 'o', color='#58a6ff', markersize=7)
            ax.plot(2.2, 4.0, 'o', color='#58a6ff', markersize=7)
            status_text = "Stage 2: Encoding 3-Qubit Repetition Code (|111⟩)"

        # Phase 3: Error Strike (21 - 32)
        elif 20 < frame <= 32:
            x_cursor = 3.8
            if err_target is not None:
                err_y = y_coords[err_target]
                pulse = np.sin((frame - 20) * 0.6) * 0.05
                ax.add_patch(FancyBboxPatch((3.5 - pulse, err_y - 0.25 - pulse), 0.6 + 2*pulse, 0.5 + 2*pulse,
                                            boxstyle="round,pad=0.05", fc='#da3633', ec='#f85149', lw=2))
                ax.text(3.8, err_y, "X_err", color='white', fontweight='bold', ha='center', va='center', fontsize=9)
                q_colors[err_target] = '#f85149'
                status_text = f"Stage 3: [ERROR STRIKE!] Bit-Flip Injected on Data Qubit {err_target}!"
                status_color = '#f85149'
                fidelity = 0
            else:
                status_text = "Stage 3: No Error Injected (Clean quantum state)."

        # Phase 4: Syndrome Parity Extraction (33 - 44)
        elif 32 < frame <= 44:
            x_cursor = 5.5
            if err_target is not None:
                err_y = y_coords[err_target]
                ax.add_patch(FancyBboxPatch((3.5, err_y - 0.25), 0.6, 0.5, boxstyle="round,pad=0.05", fc='#da3633', ec='#f85149'))
                ax.text(3.8, err_y, "X_err", color='white', fontweight='bold', ha='center', va='center', fontsize=9)
                q_colors[err_target] = '#f85149'

            # Ancilla parity CNOTs
            ax.plot([5.0, 5.0], [4.0, 1.0], color='#d29922', lw=2)
            ax.plot([5.3, 5.3], [3.0, 1.0], color='#d29922', lw=2)
            ax.plot([5.6, 5.6], [3.0, 0.0], color='#d29922', lw=2)
            ax.plot([5.9, 5.9], [2.0, 0.0], color='#d29922', lw=2)

            syn_str = "00"
            if err_target == 0: syn_str = "01"
            elif err_target == 1: syn_str = "11"
            elif err_target == 2: syn_str = "10"

            q_colors[3] = '#e3b341'
            q_colors[4] = '#e3b341'
            status_text = f"Stage 4: Parity Measured Syndrome s1 s0 = '{syn_str}' (Identified Q{err_target if err_target is not None else 'None'})"
            status_color = '#d29922'
            fidelity = 50 if err_target is not None else 100

        # Phase 5: Dynamic Correction (45 - 52)
        elif 44 < frame <= 52:
            x_cursor = 7.2
            if err_target is not None:
                err_y = y_coords[err_target]
                # Feedforward arrow
                ax.annotate("", xy=(7.2, err_y), xytext=(6.2, 0.5),
                            arrowprops=dict(arrowstyle="->", color='#2ea043', lw=2, linestyle='-.'))

                pulse = np.sin((frame - 44) * 0.7) * 0.06
                ax.add_patch(FancyBboxPatch((6.9 - pulse, err_y - 0.25 - pulse), 0.6 + 2*pulse, 0.5 + 2*pulse,
                                            boxstyle="round,pad=0.05", fc='#238636', ec='#3fb950', lw=2))
                ax.text(7.2, err_y, "X_corr", color='white', fontweight='bold', ha='center', va='center', fontsize=9)
                q_colors[err_target] = '#3fb950'
                status_text = f"Stage 5: Dynamic Feedforward Applies Conditional X on Data Qubit {err_target}!"
                status_color = '#3fb950'
            else:
                status_text = "Stage 5: No correction needed (Syndrome = 00)."
            fidelity = 100

        # Phase 6: Restored (53 - 59)
        else:
            x_cursor = 8.8
            q_colors[0] = '#2ea043'
            q_colors[1] = '#2ea043'
            q_colors[2] = '#2ea043'
            ax.plot([8.2, 8.2], [4.0, 2.0], color='#2ea043', lw=2)
            ax.plot([8.5, 8.5], [4.0, 3.0], color='#2ea043', lw=2)
            ax.add_patch(FancyBboxPatch((8.8, 3.75), 0.5, 0.5, boxstyle="square,pad=0", fc='#238636', ec='#3fb950'))
            ax.text(9.05, 4.0, "M", color='white', fontweight='bold', ha='center', va='center')
            status_text = "Stage 6: [HEALED] Logical State |1⟩ Fully Restored (Fidelity: 100%)!"
            status_color = '#3fb950'
            fidelity = 100

        for i, (name, y, color) in enumerate(zip(qubits, y_coords, q_colors)):
            ax.plot(x_cursor, y, 'o', color=color, markersize=12, markeredgecolor='white', markeredgewidth=1.5, zorder=5)

        ax.add_patch(FancyBboxPatch((0.0, -0.7), 9.0, 0.45, boxstyle="round,pad=0.05", fc='#161b22', ec='#30363d', lw=1.5))
        ax.text(0.2, -0.48, status_text, color=status_color, fontsize=10.5, fontweight='bold', va='center')
        ax.text(8.8, -0.48, f"Fidelity: {fidelity}%", color=status_color, fontsize=10.5, fontweight='bold', ha='right', va='center')

        return []

    ani = animation.FuncAnimation(fig, animate, frames=num_frames, interval=110, blit=False)
    out_path = os.path.join(OUTPUT_DIR, out_filename)
    ani.save(out_path, writer='pillow', dpi=100)
    plt.close(fig)
    print(f"      -> Successfully saved: {out_filename}")

def main():
    export_scenario_circuit_images()
    generate_scenario_gif(0,    "anim_error_q0.gif", "Error on Qubit 0")
    generate_scenario_gif(1,    "anim_error_q1.gif", "Error on Qubit 1")
    generate_scenario_gif(2,    "anim_error_q2.gif", "Error on Qubit 2")
    generate_scenario_gif(None, "anim_clean.gif",    "Clean Run (No Error)")
    print("\nAll scenario animations and images successfully generated!")

if __name__ == "__main__":
    main()
