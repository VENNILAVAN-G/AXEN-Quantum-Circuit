"""
generate_laptop_comparison_media.py
===================================
Generates high-resolution Image (PNG) and Animated GIF
for the exact 4 Dataset Experiments compared between
Laptop A (Friend's Unprotected Circuit) and Laptop B (Our QEC Protected Circuit).

Values:
- Exp_001: Minor Thermal Fluctuation (Laptop A: 59.9% vs Laptop B: 100.0%)
- Exp_002: Moderate Cosmic Ray Impact (Laptop A: 36.8% vs Laptop B: 100.0%)
- Exp_003: Severe Cross-Talk Noise (Laptop A: 6.8% vs Laptop B: 100.0%)
- Exp_004: Extreme Magnetic Disturbance (Laptop A: 0.8% vs Laptop B: 100.0%)

Outputs:
1. visualizations/laptop_a_vs_laptop_b_comparison.png (Publication-ready Static Graphic)
2. visualizations/laptop_a_vs_b_live_animation.gif (Dynamic Looping Presentation GIF)
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Arrow
from PIL import Image

# Windows console UTF-8 safety
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIS_DIR = os.path.join(BASE_DIR, "visualizations")
os.makedirs(VIS_DIR, exist_ok=True)

PNG_PATH = os.path.join(VIS_DIR, "laptop_a_vs_laptop_b_comparison.png")
GIF_PATH = os.path.join(VIS_DIR, "laptop_a_vs_b_live_animation.gif")

EXPERIMENTS = [
    {
        "id": "Exp_001",
        "name": "Minor Thermal Fluctuation",
        "desc": "Thermal energy dissipation across idle qubits",
        "lap_a_acc": 59.9,
        "lap_a_counts": "{'0': 401, '1': 599}",
        "lap_b_acc": 100.0,
        "lap_b_counts": "{'111': 1000}",
        "syndrome": "01",
        "target_qubit": "Qubit 0",
        "gain": "+40.1%"
    },
    {
        "id": "Exp_002",
        "name": "Moderate Cosmic Ray Impact",
        "desc": "Substrate ionizing radiation causing burst bit-flip",
        "lap_a_acc": 36.8,
        "lap_a_counts": "{'0': 632, '1': 368}",
        "lap_b_acc": 100.0,
        "lap_b_counts": "{'111': 1000}",
        "syndrome": "11",
        "target_qubit": "Qubit 1",
        "gain": "+63.2%"
    },
    {
        "id": "Exp_003",
        "name": "Severe Cross-Talk Noise",
        "desc": "Parasitic ZZ coupling from neighboring drive lines",
        "lap_a_acc": 6.8,
        "lap_a_counts": "{'0': 932, '1': 68}",
        "lap_b_acc": 100.0,
        "lap_b_counts": "{'111': 1000}",
        "syndrome": "10",
        "target_qubit": "Qubit 2",
        "gain": "+93.2%"
    },
    {
        "id": "Exp_004",
        "name": "Extreme Magnetic Disturbance",
        "desc": "Flux bias fluctuation destroying quantum state",
        "lap_a_acc": 0.8,
        "lap_a_counts": "{'0': 992, '1': 8}",
        "lap_b_acc": 100.0,
        "lap_b_counts": "{'111': 1000}",
        "syndrome": "01",
        "target_qubit": "Qubit 0",
        "gain": "+99.2%"
    }
]

# ==============================================================================
# 1. GENERATE STATIC PUBLICATION-QUALITY COMPARISON IMAGE
# ==============================================================================
def generate_static_comparison_image():
    print("[*] Generating static high-res comparison figure...")
    fig, axes = plt.subplots(2, 2, figsize=(16, 11), dpi=200)
    fig.patch.set_facecolor('#F8FAFC')

    # Panel 1: Direct Accuracy Comparison Bar Chart
    ax1 = axes[0, 0]
    ax1.set_facecolor('#FFFFFF')
    exp_labels = [f"{e['id']}\n{e['name']}" for e in EXPERIMENTS]
    lap_a_vals = [e['lap_a_acc'] for e in EXPERIMENTS]
    lap_b_vals = [e['lap_b_acc'] for e in EXPERIMENTS]
    
    x = np.arange(len(exp_labels))
    width = 0.35

    rects1 = ax1.bar(x - width/2, lap_a_vals, width, label="Normal Quantum Circuit (Laptop A)", 
                     color='#EF4444', edgecolor='#B91C1C', linewidth=1.5, alpha=0.9)
    rects2 = ax1.bar(x + width/2, lap_b_vals, width, label="AXEN Quantum Circuit (Laptop B)", 
                     color='#10B981', edgecolor='#047857', linewidth=1.5, alpha=0.95)

    ax1.set_title("Hardware Disturbance Accuracy: Normal vs. AXEN Quantum Circuit", fontsize=13, fontweight='bold', pad=12, color='#0F172A')
    ax1.set_xticks(x)
    ax1.set_xticklabels(exp_labels, fontsize=8.5, fontweight='bold', color='#334155', rotation=8, ha='right')
    ax1.set_ylabel("Fidelity / Output Accuracy (%)", fontsize=11, fontweight='semibold', color='#0F172A')
    ax1.set_ylim(0, 126)
    ax1.grid(axis='y', linestyle='--', alpha=0.4, color='#CBD5E1')
    ax1.legend(loc='upper left', fontsize=9.5, framealpha=0.95)

    # Add data labels & gain badges
    for i, (r1, r2) in enumerate(zip(rects1, rects2)):
        h1 = r1.get_height()
        h2 = r2.get_height()
        ax1.annotate(f"{h1:.1f}%", (r1.get_x() + r1.get_width()/2, h1 + 1.5),
                     ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#B91C1C')
        ax1.annotate(f"{h2:.1f}%", (r2.get_x() + r2.get_width()/2, h2 + 1.5),
                     ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#047857')
        # Gain badge
        gain_text = EXPERIMENTS[i]['gain']
        ax1.text(x[i], 114, gain_text, ha='center', va='center', fontsize=9, fontweight='bold',
                 color='#0F766E', bbox=dict(boxstyle="round,pad=0.25", facecolor='#CCFBF1', edgecolor='#14B8A6', linewidth=1))

    # Panel 2: State Decay vs Perfect Coherence Preservation
    ax2 = axes[0, 1]
    ax2.set_facecolor('#FFFFFF')
    
    categories = ['|0> (Decayed/Wrong)', '|1> / |111> (Target Correct)']
    y_pos = np.arange(len(categories))
    
    ax2.barh(y_pos - 0.18, [992, 8], 0.35, label="Normal Quantum Circuit (Exp_004)", color='#F87171', edgecolor='#DC2626')
    ax2.barh(y_pos + 0.18, [0, 1000], 0.35, label="AXEN Quantum Circuit (Exp_004)", color='#34D399', edgecolor='#059669')
    
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(categories, fontsize=10.5, fontweight='bold')
    ax2.set_xlabel("Measurement Shots (Out of 1000 Total)", fontsize=11, fontweight='semibold')
    ax2.set_title("Extreme Disturbance (Exp_004) Shot Distribution", fontsize=13, fontweight='bold', pad=12)
    ax2.set_xlim(0, 1150)
    ax2.grid(axis='x', linestyle='--', alpha=0.4)
    ax2.legend(loc='lower right', fontsize=10)
    
    ax2.annotate("99.2% Failure\n(Raw Hardware)", xy=(992, 0 - 0.18), xytext=(830, 0.4),
                 arrowprops=dict(arrowstyle="->", color='#DC2626', lw=1.5),
                 fontsize=9.5, fontweight='bold', color='#DC2626')
    ax2.annotate("100% Pristine\n(AXEN QEC)", xy=(1000, 1 + 0.18), xytext=(780, 1.4),
                 arrowprops=dict(arrowstyle="->", color='#059669', lw=1.5),
                 fontsize=9.5, fontweight='bold', color='#059669')

    # Panel 3: Ancilla Syndrome Localization Matrix
    ax3 = axes[1, 0]
    ax3.set_facecolor('#FFFFFF')
    ax3.axis('off')
    
    table_data = [
        ["Experiment", "Dataset Disturbance", "Syndrome", "Detected Error", "Correction Gate", "Accuracy"],
        ["Exp_001", "Minor Thermal", "01", "Bit-Flip on Q0", "Dynamic X(q0)", "100.0%"],
        ["Exp_002", "Cosmic Ray", "11", "Bit-Flip on Q1", "Dynamic X(q1)", "100.0%"],
        ["Exp_003", "Cross-Talk Noise", "10", "Bit-Flip on Q2", "Dynamic X(q2)", "100.0%"],
        ["Exp_004", "Extreme Magnetic", "01", "Bit-Flip on Q0", "Dynamic X(q0)", "100.0%"]
    ]
    
    table = ax3.table(cellText=table_data, loc='center', cellLoc='center',
                      colWidths=[0.14, 0.22, 0.12, 0.20, 0.18, 0.14])
    table.auto_set_font_size(False)
    table.set_fontsize(9.5)
    table.scale(1.05, 2.1)
    
    for (row_idx, col_idx), cell in table.get_celld().items():
        if row_idx == 0:
            cell.set_facecolor('#1E293B')
            cell.set_text_props(color='#FFFFFF', fontweight='bold')
        else:
            cell.set_facecolor('#F1F5F9' if row_idx % 2 == 0 else '#FFFFFF')
            if col_idx == 5:
                cell.set_text_props(color='#047857', fontweight='bold')
            elif col_idx == 2:
                cell.set_text_props(color='#2563EB', fontweight='bold')
                
    ax3.set_title("AXEN Quantum Circuit: Autonomous Diagnosis & Feedforward Matrix", fontsize=13, fontweight='bold', pad=25)

    # Panel 4: Architectural Triad Comparison (The Quantum Solution Block)
    ax4 = axes[1, 1]
    ax4.set_facecolor('#FFFFFF')
    ax4.axis('off')
    
    rect_a = FancyBboxPatch((0.03, 0.53), 0.94, 0.42, boxstyle="round,pad=0.03", 
                            facecolor="#FEE2E2", edgecolor="#EF4444", linewidth=1.5)
    ax4.add_patch(rect_a)
    ax4.text(0.06, 0.88, "LAPTOP A: NORMAL QUANTUM CIRCUIT", fontsize=10.5, fontweight='bold', color='#991B1B')
    ax4.text(0.06, 0.78, "Status: FAILED (Accuracy collapsed to 0.8% - 59.9%)", fontsize=9.5, fontweight='bold', color='#DC2626')
    ax4.text(0.06, 0.68, "• Single physical qubit q[0] directly exposed to environment.", fontsize=9, color='#7F1D1D')
    ax4.text(0.06, 0.58, "• No parity measurement. No syndromes. Disturbance destroys state permanently.", fontsize=9, color='#7F1D1D')

    rect_b = FancyBboxPatch((0.03, 0.04), 0.94, 0.44, boxstyle="round,pad=0.03", 
                            facecolor="#D1FAE5", edgecolor="#10B981", linewidth=1.5)
    ax4.add_patch(rect_b)
    ax4.text(0.06, 0.42, "LAPTOP B: AXEN QUANTUM CIRCUIT", fontsize=10.5, fontweight='bold', color='#065F46')
    ax4.text(0.06, 0.33, "Status: PASSED (100.0% Solid Accuracy Restored)", fontsize=9.5, fontweight='bold', color='#047857')
    ax4.text(0.06, 0.24, "• 3 Physical Data Qubits: Redundant logical encoding |1_L> = |111>.", fontsize=9, color='#047857')
    ax4.text(0.06, 0.16, "• 2 Ancilla Qubits: Continuous non-destructive parity checks (Z0Z1, Z1Z2).", fontsize=9, color='#047857')
    ax4.text(0.06, 0.08, "• Real-time FPGA Dynamic Feedforward: Automatic single-shot X-gate correction.", fontsize=9, color='#047857')
    
    ax4.set_title("Architectural Comparison: Normal vs. AXEN Architecture", fontsize=13, fontweight='bold', pad=15)

    plt.suptitle("KAGGLE QUANTUM CIRCUIT STABILITY BENCHMARK: NORMAL vs. AXEN QUANTUM CIRCUIT", 
                 fontsize=14.5, fontweight='bold', color='#0F172A', y=0.98)
    
    plt.tight_layout(rect=[0, 0.02, 1, 0.96])
    plt.savefig(PNG_PATH, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"✅ High-resolution comparison image saved to: {PNG_PATH}")



# ==============================================================================
# 2. GENERATE DYNAMIC ANIMATED GIF (EXP_001 TO EXP_004 IN ACTION)
# ==============================================================================
def generate_animated_comparison_gif():
    print("[*] Generating dynamic looping presentation GIF...")
    
    frames = []
    # Total 4 experiments, 18 frames each = 72 frames (~7.2 seconds at 10 fps)
    frames_per_exp = 16
    
    for exp_idx, exp in enumerate(EXPERIMENTS):
        for f in range(frames_per_exp):
            # Progress inside this experiment (0.0 to 1.0)
            progress = f / (frames_per_exp - 1)
            
            fig, ax = plt.subplots(figsize=(10, 6.2), dpi=100)
            fig.patch.set_facecolor('#0F172A') # Dark modern presentation theme
            ax.set_facecolor('#0F172A')
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.axis('off')
            
            # 1. Header Banner
            ax.text(5.0, 9.4, f"DATASET BENCHMARK: {exp['id']} - {exp['name'].upper()}", 
                    ha='center', va='center', fontsize=13, fontweight='bold', color='#38BDF8')
            ax.text(5.0, 8.8, f"Disturbance: {exp['desc']}", 
                    ha='center', va='center', fontsize=9.5, color='#94A3B8')
            
            # Divider line
            ax.plot([0.5, 9.5], [8.4, 8.4], color='#334155', lw=1.5)
            
            # 2. LAPTOP A SECTION (Top Card)
            card_a = FancyBboxPatch((0.5, 4.6), 9.0, 3.5, boxstyle="round,pad=0.2",
                                    facecolor="#1E293B", edgecolor="#EF4444" if progress > 0.4 else "#475569", 
                                    linewidth=2.0)
            ax.add_patch(card_a)
            ax.text(0.9, 7.7, "LAPTOP A: NORMAL QUANTUM CIRCUIT (UNPROTECTED)", 
                    fontsize=10.5, fontweight='bold', color='#F87171')

            
            # Noise strike indicator on Laptop A
            if progress < 0.3:
                stage_a = ">> Disturbance injected from dataset..."
                color_a = '#FCD34D'
                cur_acc_a = 100.0 - (100.0 - exp['lap_a_acc']) * (progress / 0.3)
            else:
                stage_a = f"[FAILED] Qubit decohered | Target state destroyed"
                color_a = '#EF4444'
                cur_acc_a = exp['lap_a_acc']
                
            ax.text(0.9, 7.1, stage_a, fontsize=9.5, fontweight='semibold', color=color_a)
            ax.text(0.9, 6.4, f"Output Counts : {exp['lap_a_counts']} | No Error Identification", fontsize=9, color='#CBD5E1')
            
            # Progress bar for Laptop A
            ax.text(0.9, 5.5, f"Fidelity: {cur_acc_a:.1f}%", fontsize=11, fontweight='bold', color='#EF4444')
            bar_w_a = (cur_acc_a / 100.0) * 5.0
            # Background bar
            ax.add_patch(Rectangle((2.8, 5.25), 5.0, 0.45, facecolor="#334155", edgecolor="none"))
            # Filled bar
            ax.add_patch(Rectangle((2.8, 5.25), bar_w_a, 0.45, facecolor="#EF4444", edgecolor="none"))
            
            # Status Badge A
            if progress > 0.35:
                ax.text(8.8, 5.48, "FAILED", ha='center', va='center', fontsize=9.5, fontweight='bold',
                        color='#FFFFFF', bbox=dict(boxstyle="round,pad=0.3", facecolor='#DC2626', edgecolor='none'))

            # 3. LAPTOP B SECTION (Bottom Card)
            card_b = FancyBboxPatch((0.5, 0.6), 9.0, 3.6, boxstyle="round,pad=0.2",
                                    facecolor="#1E293B", edgecolor="#10B981" if progress > 0.5 else "#475569", 
                                    linewidth=2.0)
            ax.add_patch(card_b)
            ax.text(0.9, 3.8, "LAPTOP B: AXEN QUANTUM CIRCUIT (3 DATA + 2 ANCILLA QEC)", 
                    fontsize=10.5, fontweight='bold', color='#34D399')

            
            # Dynamic stages on Laptop B
            if progress < 0.3:
                stage_b = ">> Ingesting disturbance through redundant 3-qubit channel..."
                color_b = '#FCD34D'
            elif progress < 0.6:
                stage_b = f"[DETECT] Parity Check: Syndrome '{exp['syndrome']}' -> Identified {exp['target_qubit']}!"
                color_b = '#38BDF8'
            else:
                stage_b = f"[PASS] Dynamic FPGA Feedforward: Corrective X-gate applied -> 100% RESTORED!"
                color_b = '#10B981'
                
            ax.text(0.9, 3.2, stage_b, fontsize=9.5, fontweight='semibold', color=color_b)
            ax.text(0.9, 2.5, f"Output Counts : {exp['lap_b_counts']} | All 3 data qubits in |111>", fontsize=9, color='#CBD5E1')

            
            # Progress bar for Laptop B (Always stays at 100%)
            ax.text(0.9, 1.6, "Fidelity: 100.0%", fontsize=11, fontweight='bold', color='#10B981')
            # Background bar
            ax.add_patch(Rectangle((2.8, 1.35), 5.0, 0.45, facecolor="#334155", edgecolor="none"))
            # Filled bar
            ax.add_patch(Rectangle((2.8, 1.35), 5.0, 0.45, facecolor="#10B981", edgecolor="none"))
            
            # Status Badge B
            ax.text(8.8, 1.58, "RESTORED", ha='center', va='center', fontsize=9.5, fontweight='bold',
                    color='#FFFFFF', bbox=dict(boxstyle="round,pad=0.3", facecolor='#059669', edgecolor='none'))

            # Footer step indicator
            dots = ""
            for i in range(len(EXPERIMENTS)):
                dots += " ●" if i == exp_idx else " ○"
            ax.text(5.0, 0.25, f"Experiment {exp_idx+1} of 4 {dots}", ha='center', va='center', fontsize=9, color='#64748B')

            plt.tight_layout()
            
            # Render to PIL Image safely using numpy array
            fig.canvas.draw()
            rgba_array = np.asarray(fig.canvas.buffer_rgba())
            img = Image.fromarray(rgba_array).convert("RGB")
            frames.append(img)
            plt.close()

            
    # Save as animated GIF
    if frames:
        frames[0].save(
            GIF_PATH,
            save_all=True,
            append_images=frames[1:],
            optimize=False,
            duration=120, # 120ms per frame
            loop=0
        )
        print(f"✅ Dynamic presentation GIF saved to: {GIF_PATH}")

def main():
    print("=" * 80)
    print("  GENERATING MEDIA ASSETS FOR LAPTOP A vs. LAPTOP B COMPARISON")
    print("=" * 80)
    generate_static_comparison_image()
    generate_animated_comparison_gif()
    print("=" * 80)
    print("🎉 ALL MEDIA ASSETS SUCCESSFULLY GENERATED!")
    print(f"1. Image:     {PNG_PATH}")
    print(f"2. Animation: {GIF_PATH}")
    print("=" * 80)

if __name__ == "__main__":
    main()
