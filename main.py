import tkinter as tk
from tkinter import messagebox, filedialog
import threading
from settings import load_config, save_config
from automation import run_automation


class CaffeinatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Computer Caffeinator")
        self.config = load_config()

        self.create_widgets()

    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # MS Word Path
        tk.Label(main_frame, text="MS Word Path:").grid(row=0, column=0, sticky="w")
        self.word_path_var = tk.StringVar(value=self.config["ms_word_path"])
        tk.Entry(main_frame, textvariable=self.word_path_var, width=40).grid(
            row=0, column=1, padx=5
        )
        tk.Button(main_frame, text="Browse", command=self.browse_word_path).grid(
            row=0, column=2
        )

        # Coordinates
        tk.Label(main_frame, text="Coordinates (X, Y):").grid(
            row=1, column=0, sticky="w", pady=(10, 0)
        )
        coord_frame = tk.Frame(main_frame)
        coord_frame.grid(row=1, column=1, sticky="w", pady=(10, 0))

        self.coord_x_var = tk.IntVar(
            value=self.config["coordinates"]["blank_document"]["x"]
        )
        self.coord_y_var = tk.IntVar(
            value=self.config["coordinates"]["blank_document"]["y"]
        )

        tk.Label(coord_frame, text="X:").pack(side=tk.LEFT)
        tk.Entry(coord_frame, textvariable=self.coord_x_var, width=5).pack(
            side=tk.LEFT, padx=5
        )
        tk.Label(coord_frame, text="Y:").pack(side=tk.LEFT)
        tk.Entry(coord_frame, textvariable=self.coord_y_var, width=5).pack(
            side=tk.LEFT, padx=5
        )

        # Automation Settings
        tk.Label(main_frame, text="Automation Settings:").grid(
            row=2, column=0, sticky="w", pady=(10, 0)
        )

        tk.Label(main_frame, text="Text to Type:").grid(
            row=3, column=0, sticky="w", padx=10
        )
        self.text_var = tk.StringVar(value=self.config["automation"]["text"])
        tk.Entry(main_frame, textvariable=self.text_var, width=40).grid(
            row=3, column=1, padx=5
        )

        tk.Label(main_frame, text="Interval (sec):").grid(
            row=4, column=0, sticky="w", padx=10
        )
        self.interval_var = tk.DoubleVar(value=self.config["automation"]["interval"])
        tk.Entry(main_frame, textvariable=self.interval_var, width=10).grid(
            row=4, column=1, sticky="w", padx=5
        )

        tk.Label(main_frame, text="Loop Count:").grid(
            row=5, column=0, sticky="w", padx=10
        )
        self.loop_count_var = tk.IntVar(value=self.config["automation"]["loop_count"])
        tk.Entry(main_frame, textvariable=self.loop_count_var, width=10).grid(
            row=5, column=1, sticky="w", padx=5
        )

        # Delays
        tk.Label(main_frame, text="Delays (seconds):").grid(
            row=6, column=0, sticky="w", pady=(10, 0)
        )

        tk.Label(main_frame, text="App Start:").grid(
            row=7, column=0, sticky="w", padx=10
        )
        self.delay_app_start_var = tk.IntVar(value=self.config["delays"]["app_start"])
        tk.Entry(main_frame, textvariable=self.delay_app_start_var, width=10).grid(
            row=7, column=1, sticky="w", padx=5
        )

        tk.Label(main_frame, text="Doc Ready:").grid(
            row=8, column=0, sticky="w", padx=10
        )
        self.delay_doc_ready_var = tk.IntVar(value=self.config["delays"]["doc_ready"])
        tk.Entry(main_frame, textvariable=self.delay_doc_ready_var, width=10).grid(
            row=8, column=1, sticky="w", padx=5
        )

        tk.Label(main_frame, text="Line Pause:").grid(
            row=9, column=0, sticky="w", padx=10
        )
        self.delay_line_pause_var = tk.IntVar(value=self.config["delays"]["line_pause"])
        tk.Entry(main_frame, textvariable=self.delay_line_pause_var, width=10).grid(
            row=9, column=1, sticky="w", padx=5
        )

        # Buttons
        btn_frame = tk.Frame(main_frame, pady=20)
        btn_frame.grid(row=10, column=0, columnspan=3)

        tk.Button(btn_frame, text="Save Config", command=self.save_settings).pack(
            side=tk.LEFT, padx=10
        )
        tk.Button(
            btn_frame,
            text="Start Automation",
            command=self.start_automation,
            bg="green",
            fg="white",
        ).pack(side=tk.LEFT, padx=10)

    def browse_word_path(self):
        filename = filedialog.askopenfilename(
            title="Select MS Word Executable",
            filetypes=[("Executables", "*.exe"), ("All Files", "*.*")],
        )
        if filename:
            self.word_path_var.set(filename)

    def save_settings(self):
        try:
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
