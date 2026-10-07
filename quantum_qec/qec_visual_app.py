"""
Quantum Error Correction (QEC) - High-Visibility Live Visualizer
==================================================================
Displays crystal-clear, high-resolution circuit diagrams and animations
for each error scenario:
- Qubit 0 Error (X Gate on Q0) -> Syndrome '01' -> Auto-corrected with X(q0)
- Qubit 1 Error (X Gate on Q1) -> Syndrome '11' -> Auto-corrected with X(q1)
- Qubit 2 Error (X Gate on Q2) -> Syndrome '10' -> Auto-corrected with X(q2)
- Clean State  (No Error)      -> Syndrome '00' -> Preserved 100%
"""

import os
import sys
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIS_DIR = os.path.join(BASE_DIR, "visualizations")

SCENARIOS = {
    0: {
        "title": "💥 Error Injected on Data Qubit 0 (X Gate)",
        "gif": os.path.join(VIS_DIR, "anim_error_q0.gif"),
        "png": os.path.join(VIS_DIR, "circuit_error_q0.png"),
        "syndrome": "s1 s0 = '01'",
        "syndrome_desc": "Parity check flagged mismatch at q0-q1 -> Fault localized on Q0",
        "correction": "Applied dynamic X gate on Data Qubit 0",
        "fidelity": "100.0% (State Fully Restored!)",
        "color": "#e63946"
    },
    1: {
        "title": "💥 Error Injected on Data Qubit 1 (X Gate)",
        "gif": os.path.join(VIS_DIR, "anim_error_q1.gif"),
        "png": os.path.join(VIS_DIR, "circuit_error_q1.png"),
        "syndrome": "s1 s0 = '11'",
        "syndrome_desc": "Both parity checks flagged mismatch -> Fault localized on Q1",
        "correction": "Applied dynamic X gate on Data Qubit 1",
        "fidelity": "100.0% (State Fully Restored!)",
        "color": "#e63946"
    },
    2: {
        "title": "💥 Error Injected on Data Qubit 2 (X Gate)",
        "gif": os.path.join(VIS_DIR, "anim_error_q2.gif"),
        "png": os.path.join(VIS_DIR, "circuit_error_q2.png"),
        "syndrome": "s1 s0 = '10'",
        "syndrome_desc": "Parity check flagged mismatch at q1-q2 -> Fault localized on Q2",
        "correction": "Applied dynamic X gate on Data Qubit 2",
        "fidelity": "100.0% (State Fully Restored!)",
        "color": "#e63946"
    },
    None: {
        "title": "✨ Clean Quantum State (No Error Injected)",
        "gif": os.path.join(VIS_DIR, "anim_clean.gif"),
        "png": os.path.join(VIS_DIR, "circuit_clean.png"),
        "syndrome": "s1 s0 = '00'",
        "syndrome_desc": "Both parities match -> No error present",
        "correction": "No correction required (Pure state)",
        "fidelity": "100.0% (State Pure!)",
        "color": "#2a9d8f"
    }
}

class QECViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum Error Correction (QEC) Visual Controller")
        self.root.geometry("1100x820")
        self.root.configure(bg="#1e293b")

        self.current_scenario = 0
        self.view_mode = "circuit"  # "circuit" or "animation"
        self.frames = []
        self.frame_idx = 0
        self.anim_job = None
        self.static_img = None

        self.build_ui()
        self.switch_scenario(0)

        # Keyboard shortcuts
        self.root.bind("0", lambda e: self.switch_scenario(0))
        self.root.bind("1", lambda e: self.switch_scenario(1))
        self.root.bind("2", lambda e: self.switch_scenario(2))
        self.root.bind("c", lambda e: self.switch_scenario(None))
        self.root.bind("n", lambda e: self.switch_scenario(None))

    def build_ui(self):
        # Top Header
        header = tk.Frame(self.root, bg="#0f172a", pady=12, padx=20)
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="Quantum Error Correction (QEC) Interactive Visualizer",
            font=("Segoe UI", 16, "bold"),
            fg="#38bdf8",
            bg="#0f172a"
        )
        title.pack(anchor="w")

        sub = tk.Label(
            header,
            text="Select an error value below to instantly see the circuit diagram and auto-correction update!",
            font=("Segoe UI", 10),
            fg="#94a3b8",
            bg="#0f172a"
        )
        sub.pack(anchor="w", pady=(2, 0))

        # Control Toolbar
        toolbar = tk.Frame(self.root, bg="#334155", pady=10, padx=20)
        toolbar.pack(fill="x")

        tk.Label(
            toolbar,
            text="SELECT ERROR VALUE:",
            font=("Segoe UI", 10, "bold"),
            fg="#f8fafc",
            bg="#334155"
        ).pack(side="left", padx=(0, 15))

        self.btn_map = {}
        scenarios_btns = [
            (0, "💥 Qubit 0 Error (Key: 0)", "#ef4444"),
            (1, "💥 Qubit 1 Error (Key: 1)", "#ef4444"),
            (2, "💥 Qubit 2 Error (Key: 2)", "#ef4444"),
            (None, "✨ No Error (Key: C)", "#10b981")
        ]

        for key, text, color in scenarios_btns:
            btn = tk.Button(
                toolbar,
                text=text,
                font=("Segoe UI", 10, "bold"),
                bg="#1e293b",
                fg="#f8fafc",
                activebackground=color,
                activeforeground="white",
                relief="groove",
                bd=2,
                padx=12,
                pady=6,
                cursor="hand2",
                command=lambda k=key: self.switch_scenario(k)
            )
            btn.pack(side="left", padx=5)
            self.btn_map[key] = btn

        # Toggle Mode (Circuit vs Animation)
        mode_frame = tk.Frame(toolbar, bg="#334155")
        mode_frame.pack(side="right")

        self.btn_view_circ = tk.Button(
            mode_frame,
            text="📐 Circuit Diagram",
            font=("Segoe UI", 9, "bold"),
            bg="#0284c7",
            fg="white",
            relief="flat",
            padx=10,
            pady=5,
            command=lambda: self.set_view_mode("circuit")
        )
        self.btn_view_circ.pack(side="left", padx=4)

        self.btn_view_anim = tk.Button(
            mode_frame,
            text="🎬 Animated GIF",
            font=("Segoe UI", 9, "bold"),
            bg="#1e293b",
            fg="#cbd5e1",
            relief="flat",
            padx=10,
            pady=5,
            command=lambda: self.set_view_mode("animation")
        )
        self.btn_view_anim.pack(side="left", padx=4)

        # Status Banner
        self.banner = tk.Frame(self.root, bg="#0f172a", pady=10, padx=20)
        self.banner.pack(fill="x")

        self.lbl_title = tk.Label(
            self.banner,
            text="",
            font=("Segoe UI", 13, "bold"),
            fg="#f8fafc",
            bg="#0f172a"
        )
        self.lbl_title.pack(side="left")

        self.lbl_badge = tk.Label(
            self.banner,
            text="Fidelity: 100.0%",
            font=("Segoe UI", 11, "bold"),
            fg="#10b981",
            bg="#0f172a"
        )
        self.lbl_badge.pack(side="right")

        # Main Image Viewer Frame (White Card for maximum visibility)
        self.view_card = tk.Frame(self.root, bg="#ffffff", bd=3, relief="solid")
        self.view_card.pack(fill="both", expand=True, padx=20, pady=10)

        self.img_label = tk.Label(self.view_card, bg="#ffffff")
        self.img_label.pack(fill="both", expand=True, padx=6, pady=6)

        # Telemetry Footer
        telemetry = tk.Frame(self.root, bg="#0f172a", pady=12, padx=20)
        telemetry.pack(fill="x")

        c1 = tk.Frame(telemetry, bg="#0f172a")
        c1.pack(side="left", fill="both", expand=True)
        tk.Label(c1, text="ANCILLA SYNDROME EXTRACTED:", font=("Segoe UI", 9, "bold"), fg="#94a3b8", bg="#0f172a").pack(anchor="w")
        self.lbl_syn = tk.Label(c1, text="", font=("Segoe UI", 13, "bold"), fg="#fbbf24", bg="#0f172a")
        self.lbl_syn.pack(anchor="w")
        self.lbl_syn_desc = tk.Label(c1, text="", font=("Segoe UI", 9), fg="#cbd5e1", bg="#0f172a")
        self.lbl_syn_desc.pack(anchor="w")

        c2 = tk.Frame(telemetry, bg="#0f172a")
        c2.pack(side="left", fill="both", expand=True)
        tk.Label(c2, text="ACTIVE DYNAMIC RECOVERY:", font=("Segoe UI", 9, "bold"), fg="#94a3b8", bg="#0f172a").pack(anchor="w")
        self.lbl_corr = tk.Label(c2, text="", font=("Segoe UI", 13, "bold"), fg="#38bdf8", bg="#0f172a")
        self.lbl_corr.pack(anchor="w")
        self.lbl_res = tk.Label(c2, text="", font=("Segoe UI", 9, "bold"), fg="#10b981", bg="#0f172a")
        self.lbl_res.pack(anchor="w")

    def set_view_mode(self, mode):
        self.view_mode = mode
        if mode == "circuit":
            self.btn_view_circ.configure(bg="#0284c7", fg="white")
            self.btn_view_anim.configure(bg="#1e293b", fg="#cbd5e1")
            self.view_card.configure(bg="#ffffff")
            self.img_label.configure(bg="#ffffff")
        else:
            self.btn_view_circ.configure(bg="#1e293b", fg="#cbd5e1")
            self.btn_view_anim.configure(bg="#0284c7", fg="white")
            self.view_card.configure(bg="#0d1117")
            self.img_label.configure(bg="#0d1117")

        self.switch_scenario(self.current_scenario)

    def switch_scenario(self, q):
        self.current_scenario = q
        sc = SCENARIOS[q]

        # Button highlights
        for key, btn in self.btn_map.items():
            if key == q:
                btn.configure(bg=sc["color"], fg="white")
            else:
                btn.configure(bg="#1e293b", fg="#f8fafc")

        # Update text labels
        self.lbl_title.configure(text=sc["title"])
        self.lbl_syn.configure(text=sc["syndrome"])
        self.lbl_syn_desc.configure(text=sc["syndrome_desc"])
        self.lbl_corr.configure(text=sc["correction"])
        self.lbl_res.configure(text=f"Result: {sc['fidelity']}")

        # Cancel any ongoing animation timer
        if self.anim_job:
            self.root.after_cancel(self.anim_job)
            self.anim_job = None

        if self.view_mode == "circuit":
            self.show_circuit_png(sc["png"])
        else:
            self.show_animation_gif(sc["gif"])

    def show_circuit_png(self, png_path):
        if not os.path.exists(png_path):
            self.img_label.configure(text=f"Image not found: {png_path}", fg="red")
            return

        im = Image.open(png_path)
        # Resize to fit window nicely while maintaining aspect ratio
        max_w, max_h = 1040, 480
        im.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
        self.static_img = ImageTk.PhotoImage(im)
        self.img_label.configure(image=self.static_img)

    def show_animation_gif(self, gif_path):
        if not os.path.exists(gif_path):
            self.img_label.configure(text=f"GIF not found: {gif_path}", fg="red")
            return

        im = Image.open(gif_path)
        self.frames = []
        max_w, max_h = 1000, 480
        for f in ImageSequence.Iterator(im):
            # CRITICAL FIX: Convert to RGBA before resizing to prevent black palette bug!
            f_rgba = f.convert("RGBA")
            f_rgba.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
            self.frames.append(ImageTk.PhotoImage(f_rgba))

        self.frame_idx = 0
        self.play_gif_loop()

    def play_gif_loop(self):
        if not self.frames:
            return
        self.img_label.configure(image=self.frames[self.frame_idx])
        self.frame_idx = (self.frame_idx + 1) % len(self.frames)
        self.anim_job = self.root.after(110, self.play_gif_loop)

def main():
    root = tk.Tk()
    app = QECViewerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
