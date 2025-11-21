import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import threading
import os
import pyautogui
from settings import load_config, save_config
from automation import run_automation


class CaffeinatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Computer Caffeinator")
        self.root.geometry("550x480")
        self.root.resizable(True, False)
        self.config = load_config()

        self.create_widgets()
        self.update_mouse_position()

    def create_widgets(self):
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Section 1: Application Setup ---
        setup_frame = ttk.LabelFrame(main_frame, text="Application Setup", padding="10")
        setup_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(setup_frame, text="MS Word Path:").grid(row=0, column=0, sticky="w")
        self.word_path_var = tk.StringVar(value=self.config["ms_word_path"])
        ttk.Entry(setup_frame, textvariable=self.word_path_var, width=50).grid(
            row=0, column=1, padx=5, sticky="ew"
        )
        ttk.Button(setup_frame, text="Browse", command=self.browse_word_path).grid(
            row=0, column=2, padx=5
        )
        setup_frame.columnconfigure(1, weight=1)

        # --- Section 2: Target Coordinates ---
        coord_frame = ttk.LabelFrame(
            main_frame, text="Target Coordinates", padding="10"
        )
        coord_frame.pack(fill=tk.X, pady=(0, 10))

        # Row 0: Inputs
        ttk.Label(coord_frame, text="Click Location (X, Y):").grid(
            row=0, column=0, sticky="w"
        )

        input_subframe = ttk.Frame(coord_frame)
        input_subframe.grid(row=0, column=1, sticky="w", padx=5)

        self.coord_x_var = tk.IntVar(
            value=self.config["coordinates"]["blank_document"]["x"]
        )
        self.coord_y_var = tk.IntVar(
            value=self.config["coordinates"]["blank_document"]["y"]
        )

        ttk.Label(input_subframe, text="X:").pack(side=tk.LEFT)
        ttk.Entry(input_subframe, textvariable=self.coord_x_var, width=6).pack(
            side=tk.LEFT, padx=(0, 10)
        )
        ttk.Label(input_subframe, text="Y:").pack(side=tk.LEFT)
        ttk.Entry(input_subframe, textvariable=self.coord_y_var, width=6).pack(
            side=tk.LEFT
        )

        # Row 1: Tracker
        self.tracking_var = tk.BooleanVar()
        ttk.Checkbutton(
            coord_frame, text="Show Realtime Mouse Position", variable=self.tracking_var
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(10, 0))

        self.mouse_pos_label = ttk.Label(
            coord_frame, text="Current Mouse Position: -", foreground="blue"
        )
        self.mouse_pos_label.grid(row=1, column=1, sticky="w", pady=(10, 0), padx=5)

        # --- Section 3: Automation Details ---
        auto_frame = ttk.LabelFrame(main_frame, text="Automation Details", padding="10")
        auto_frame.pack(fill=tk.X, pady=(0, 10))

        # Grid layout for automation
        ttk.Label(auto_frame, text="Text to Type:").grid(
            row=0, column=0, sticky="w", pady=2
        )
        self.text_var = tk.StringVar(value=self.config["automation"]["text"])
        ttk.Entry(auto_frame, textvariable=self.text_var).grid(
            row=0, column=1, sticky="ew", padx=5, pady=2
        )

        ttk.Label(auto_frame, text="Typing Interval (sec):").grid(
            row=1, column=0, sticky="w", pady=2
        )
        self.interval_var = tk.DoubleVar(value=self.config["automation"]["interval"])
        ttk.Entry(auto_frame, textvariable=self.interval_var, width=10).grid(
            row=1, column=1, sticky="w", padx=5, pady=2
        )

        ttk.Label(auto_frame, text="Loop Count:").grid(
            row=2, column=0, sticky="w", pady=2
        )
        self.loop_count_var = tk.IntVar(value=self.config["automation"]["loop_count"])
        ttk.Entry(auto_frame, textvariable=self.loop_count_var, width=10).grid(
            row=2, column=1, sticky="w", padx=5, pady=2
        )

        auto_frame.columnconfigure(1, weight=1)

        # --- Section 4: Delays ---
        delay_frame = ttk.LabelFrame(
            main_frame, text="Timing & Delays (seconds)", padding="10"
        )
        delay_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(delay_frame, text="App Start Wait:").grid(
            row=0, column=0, sticky="w", padx=(0, 10)
        )
        self.delay_app_start_var = tk.IntVar(value=self.config["delays"]["app_start"])
        ttk.Entry(delay_frame, textvariable=self.delay_app_start_var, width=8).grid(
            row=0, column=1, sticky="w"
        )

        ttk.Label(delay_frame, text="Doc Ready Wait:").grid(
            row=0, column=2, sticky="w", padx=(20, 10)
        )
        self.delay_doc_ready_var = tk.IntVar(value=self.config["delays"]["doc_ready"])
        ttk.Entry(delay_frame, textvariable=self.delay_doc_ready_var, width=8).grid(
            row=0, column=3, sticky="w"
        )

        ttk.Label(delay_frame, text="Line Pause:").grid(
            row=0, column=4, sticky="w", padx=(20, 10)
        )
        self.delay_line_pause_var = tk.IntVar(value=self.config["delays"]["line_pause"])
        ttk.Entry(delay_frame, textvariable=self.delay_line_pause_var, width=8).grid(
            row=0, column=5, sticky="w"
        )

        # --- Buttons ---
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        ttk.Button(
            btn_frame, text="Save Configuration", command=self.save_settings
        ).pack(side=tk.RIGHT, padx=5)

        tk.Button(
            btn_frame,
            text="Start Automation",
            command=self.start_automation,
            bg="#4CAF50",
            fg="white",
            font=("Helvetica", 10, "bold"),
            padx=20,
            pady=5,
        ).pack(side=tk.RIGHT, padx=5)

    def update_mouse_position(self):
        if self.tracking_var.get():
            x, y = pyautogui.position()
            self.mouse_pos_label.config(text=f"Current Mouse Position: X={x}, Y={y}")
        else:
            self.mouse_pos_label.config(text="Current Mouse Position: -")
        self.root.after(100, self.update_mouse_position)

    def browse_word_path(self):
        filename = filedialog.askopenfilename(
            title="Select MS Word Executable",
            filetypes=[("Executables", "*.exe"), ("All Files", "*.*")],
        )
        if filename:
            self.word_path_var.set(filename)

    def validate_inputs(self):
        # Validate MS Word Path
        if not os.path.exists(self.word_path_var.get()):
            raise ValueError("The MS Word executable path does not exist.")

        # Validate Coordinates
        try:
            x = self.coord_x_var.get()
            y = self.coord_y_var.get()
            if x < 0 or y < 0:
                raise ValueError("Coordinates must be positive integers.")
        except tk.TclError:
            raise ValueError("Coordinates must be valid integers.")

        # Validate Automation Settings
        try:
            if self.interval_var.get() < 0:
                raise ValueError("Interval must be a non-negative number.")
            if self.loop_count_var.get() <= 0:
                raise ValueError("Loop count must be a positive integer.")
        except tk.TclError:
            raise ValueError("Interval and Loop Count must be valid numbers.")

        # Validate Delays
        try:
            if (
                self.delay_app_start_var.get() < 0
                or self.delay_doc_ready_var.get() < 0
                or self.delay_line_pause_var.get() < 0
            ):
                raise ValueError("Delays must be non-negative numbers.")
        except tk.TclError:
            raise ValueError("Delays must be valid numbers.")

    def save_settings(self):
        try:
            self.validate_inputs()

            self.config["ms_word_path"] = self.word_path_var.get()
            self.config["coordinates"]["blank_document"]["x"] = self.coord_x_var.get()
            self.config["coordinates"]["blank_document"]["y"] = self.coord_y_var.get()
            self.config["automation"]["text"] = self.text_var.get()
            self.config["automation"]["interval"] = self.interval_var.get()
            self.config["automation"]["loop_count"] = self.loop_count_var.get()
            self.config["delays"]["app_start"] = self.delay_app_start_var.get()
            self.config["delays"]["doc_ready"] = self.delay_doc_ready_var.get()
            self.config["delays"]["line_pause"] = self.delay_line_pause_var.get()

            save_config(self.config)
            messagebox.showinfo("Success", "Configuration saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {e}")

    def start_automation(self):
        # Save before starting to ensure we use latest values
        self.save_settings()

        # Run in a separate thread to keep UI responsive
        threading.Thread(target=self._run_automation_thread, daemon=True).start()

    def _run_automation_thread(self):
        try:
            run_automation(self.config)
            messagebox.showinfo("Completed", "Automation finished successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Automation failed: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CaffeinatorApp(root)
    root.mainloop()
