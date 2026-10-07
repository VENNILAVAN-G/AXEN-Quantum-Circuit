"""
Animated GIF Generator for Quantum Error Correction (QEC)
==========================================================
Generates a high-quality animated GIF (qec_recovery_animation.gif)
demonstrating the entire lifecycle of quantum error correction:
1. State Prep -> 2. Encoding -> 3. Error Strike (Red) ->
4. Ancilla Syndrome Parity -> 5. Active Correction (Green Flash) -> 6. 100% Healed!
Ideal for inserting into PowerPoint presentation slides!
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, Arrow

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "visualizations")
os.makedirs(OUTPUT_DIR, exist_ok=True)
GIF_PATH = os.path.join(OUTPUT_DIR, "qec_recovery_animation.gif")

def create_qec_animation():
    print("[*] Generating QEC Animated GIF for Presentation Slides...")
    
    # 70 frames total, 10 fps -> 7 seconds loop
    num_frames = 65
    
    fig, ax = plt.subplots(figsize=(10, 5.5), facecolor='#0d1117')
    
    qubits = ['data 0', 'data 1', 'data 2', 'ancilla 0', 'ancilla 1']
    y_coords = [4.0, 3.0, 2.0, 1.0, 0.0]
    
    def draw_base_circuit():
        ax.clear()
        ax.set_facecolor('#0d1117')
        ax.set_xlim(-0.5, 9.5)
        ax.set_ylim(-0.8, 5.2)
        ax.axis('off')

        # Draw wire rails
        for i, (name, y) in enumerate(zip(qubits, y_coords)):
            color = '#30363d' if 'ancilla' in name else '#21262d'
            ax.plot([-0.2, 9.2], [y, y], color='#484f58', linewidth=2, zorder=1)
            # Label
            label_color = '#58a6ff' if 'data' in name else '#d29922'
            ax.text(-0.4, y, f"|{name}⟩", color=label_color, fontsize=11, fontweight='bold', ha='right', va='center')

        # Stage boundary guides
        stages = [
            (0.8, "1. Prep"),
            (2.2, "2. Encode"),
            (3.8, "3. Error"),
            (5.5, "4. Syndrome"),
            (7.2, "5. Correct"),
            (8.8, "6. Restored")
        ]
        for x, label in stages:
            ax.axvline(x=x, color='#21262d', linestyle='--', linewidth=1)
            ax.text(x, 4.9, label, color='#8b949e', fontsize=9, ha='center', fontweight='bold')

    def animate(frame):
        draw_base_circuit()
        
        # State transitions based on frame:
        # Phase 1 (0-10): Prep
        # Phase 2 (11-20): Encode
        # Phase 3 (21-32): Error injection on Data 0
        # Phase 4 (33-46): Syndrome Extraction on Ancillas
        # Phase 5 (47-56): Dynamic Feedforward Correction
        # Phase 6 (57-64): Restored & Healed
        
        # Default qubit colors: normal blue
        q_colors = ['#58a6ff', '#58a6ff', '#58a6ff', '#8b949e', '#8b949e']
        status_text = "Stage 1: State Preparation (|1⟩ prepared on Data 0)"
        status_color = '#58a6ff'
        fidelity = 100

        # Phase 1: Prep
        if frame <= 10:
            x_cursor = 0.8
            # Draw X gate on data 0
            ax.add_patch(FancyBboxPatch((0.5, 3.75), 0.6, 0.5, boxstyle="round,pad=0.05", fc='#1f6feb', ec='#58a6ff', lw=1.5))
            ax.text(0.8, 4.0, "X", color='white', fontweight='bold', ha='center', va='center', fontsize=11)
            status_text = "Stage 1: Initializing Quantum State |1⟩"
            status_color = '#58a6ff'

        # Phase 2: Encode
        elif 10 < frame <= 22:
            x_cursor = 2.2
            # Draw Prep gate
            ax.add_patch(FancyBboxPatch((0.5, 3.75), 0.6, 0.5, boxstyle="round,pad=0.05", fc='#1f6feb', ec='#58a6ff', lw=1))
            ax.text(0.8, 4.0, "X", color='white', fontweight='bold', ha='center', va='center')
            
            # CNOTs
            ax.plot([1.8, 1.8], [4.0, 3.0], color='#58a6ff', lw=2)
            ax.plot([2.2, 2.2], [4.0, 2.0], color='#58a6ff', lw=2)
            ax.plot(1.8, 4.0, 'o', color='#58a6ff', markersize=7)
            ax.plot(2.2, 4.0, 'o', color='#58a6ff', markersize=7)
            ax.plot(1.8, 3.0, 'o', color='none', markeredgecolor='#58a6ff', markeredgewidth=2, markersize=10)
            ax.plot(2.2, 2.0, 'o', color='none', markeredgecolor='#58a6ff', markeredgewidth=2, markersize=10)
            
            status_text = "Stage 2: 3-Qubit Repetition Encoding (|0⟩_L → |000⟩, |1⟩_L → |111⟩)"
            status_color = '#388bfd'

        # Phase 3: Error Strike!
        elif 22 < frame <= 34:
            x_cursor = 3.8
            # Error gate in bright red
            pulse = np.sin((frame - 22) * 0.5) * 0.05
            ax.add_patch(FancyBboxPatch((3.5 - pulse, 3.7 - pulse), 0.6 + 2*pulse, 0.6 + 2*pulse,
                                        boxstyle="round,pad=0.05", fc='#da3633', ec='#f85149', lw=2))
            ax.text(3.8, 4.0, "X_err", color='white', fontweight='bold', ha='center', va='center', fontsize=9)
            
            q_colors[0] = '#f85149' # Corrupted
            status_text = "Stage 3: [ERROR STRIKE!] Random Bit-Flip flips Data Qubit 0!"
            status_color = '#f85149'
            fidelity = 0

        # Phase 4: Syndrome Parity Extraction
        elif 34 < frame <= 48:
            x_cursor = 5.5
            # Show error gate still on data 0
            ax.add_patch(FancyBboxPatch((3.5, 3.75), 0.6, 0.5, boxstyle="round,pad=0.05", fc='#da3633', ec='#f85149', lw=1.5))
            ax.text(3.8, 4.0, "X_err", color='white', fontweight='bold', ha='center', va='center', fontsize=9)
            q_colors[0] = '#f85149'
            
            # CNOTs to ancillas
            ax.plot([5.0, 5.0], [4.0, 1.0], color='#d29922', lw=2)
            ax.plot([5.3, 5.3], [3.0, 1.0], color='#d29922', lw=2)
            ax.plot([5.6, 5.6], [3.0, 0.0], color='#d29922', lw=2)
            ax.plot([5.9, 5.9], [2.0, 0.0], color='#d29922', lw=2)

            # Ancilla measurement boxes
            ax.add_patch(FancyBboxPatch((6.3, 0.75), 0.5, 0.5, boxstyle="square,pad=0", fc='#9e6a03', ec='#d29922'))
            ax.text(6.55, 1.0, "M", color='white', fontweight='bold', ha='center', va='center', fontsize=9)
            ax.add_patch(FancyBboxPatch((6.3, -0.25), 0.5, 0.5, boxstyle="square,pad=0", fc='#9e6a03', ec='#d29922'))
            ax.text(6.55, 0.0, "M", color='white', fontweight='bold', ha='center', va='center', fontsize=9)
            
            q_colors[3] = '#e3b341'
            q_colors[4] = '#e3b341'
            status_text = "Stage 4: Parity Checks Extracted Syndrome s1 s0 = '01' (Q0 Fault Pinpointed!)"
            status_color = '#d29922'
            fidelity = 50

        # Phase 5: Dynamic Correction (Green Flash)
        elif 48 < frame <= 58:
            x_cursor = 7.2
            # Feedforward arrow from ancilla to data 0
            ax.annotate("", xy=(7.2, 4.0), xytext=(6.6, 0.5),
                        arrowprops=dict(arrowstyle="->", color='#2ea043', lw=2, linestyle='-.'))
            
            # Correction gate glowing green
            pulse = np.sin((frame - 48) * 0.6) * 0.08
            ax.add_patch(FancyBboxPatch((6.9 - pulse, 3.7 - pulse), 0.6 + 2*pulse, 0.6 + 2*pulse,
                                        boxstyle="round,pad=0.05", fc='#238636', ec='#3fb950', lw=2.5))
            ax.text(7.2, 4.0, "X_corr", color='white', fontweight='bold', ha='center', va='center', fontsize=9)
            
            q_colors[0] = '#3fb950' # Healed green!
            status_text = "Stage 5: Dynamic Feedforward Applies Instantaneous X-Correction on Q0!"
            status_color = '#3fb950'
            fidelity = 100

        # Phase 6: Restored!
        else:
            x_cursor = 8.8
            # Data 0 restored
            q_colors[0] = '#2ea043'
            q_colors[1] = '#2ea043'
            q_colors[2] = '#2ea043'
            
            # Final decode CNOTs
            ax.plot([8.2, 8.2], [4.0, 2.0], color='#2ea043', lw=2)
            ax.plot([8.5, 8.5], [4.0, 3.0], color='#2ea043', lw=2)
            
            # Measurement
            ax.add_patch(FancyBboxPatch((8.8, 3.75), 0.5, 0.5, boxstyle="square,pad=0", fc='#238636', ec='#3fb950'))
            ax.text(9.05, 4.0, "M", color='white', fontweight='bold', ha='center', va='center')
            
            status_text = "Stage 6: [HEALED] Quantum State |1⟩ Fully Recovered with 100% Fidelity!"
            status_color = '#3fb950'
            fidelity = 100

        # Draw qubit state nodes at the cursor position
        for i, (name, y, color) in enumerate(zip(qubits, y_coords, q_colors)):
            ax.plot(x_cursor, y, 'o', color=color, markersize=12, markeredgecolor='white', markeredgewidth=1.5, zorder=5)

        # Status HUD Banner
        ax.add_patch(FancyBboxPatch((0.0, -0.7), 9.0, 0.45, boxstyle="round,pad=0.05", fc='#161b22', ec='#30363d', lw=1.5))
        ax.text(0.2, -0.48, status_text, color=status_color, fontsize=10.5, fontweight='bold', va='center')
        ax.text(8.8, -0.48, f"Fidelity: {fidelity}%", color=status_color, fontsize=10.5, fontweight='bold', ha='right', va='center')

        return []

    ani = animation.FuncAnimation(fig, animate, frames=num_frames, interval=110, blit=False)
    ani.save(GIF_PATH, writer='pillow', dpi=100)
    plt.close(fig)
    print(f"      -> Successfully saved animated GIF: {GIF_PATH}")

if __name__ == "__main__":
    create_qec_animation()
