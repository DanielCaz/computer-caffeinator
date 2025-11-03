import tkinter as tk


def main():
    root = tk.Tk()
    root.title("Computer Caffeinator")

    entry = tk.Entry(root, width=40)
    entry.pack(padx=20, pady=20)
    entry.focus_set()

    running = {"flag": False, "after_id": None}

    def typewriter(text, idx=0):
        if not running["flag"]:
            return
        if idx <= len(text):
            entry.delete(0, tk.END)
            entry.insert(0, text[:idx])
            running["after_id"] = root.after(80, typewriter, text, idx + 1)
        else:
            # Restart typewriting indefinitely
            running["after_id"] = root.after(500, typewriter, text, 0)

    def start_typewriting():
        if not running["flag"]:
            running["flag"] = True
            typewriter("hello world")

    def stop_typewriting():
        running["flag"] = False
        if running["after_id"]:
            root.after_cancel(running["after_id"])
            running["after_id"] = None

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)
    start_btn = tk.Button(btn_frame, text="Start", command=start_typewriting)
    start_btn.pack(side=tk.LEFT, padx=5)
    stop_btn = tk.Button(btn_frame, text="Stop", command=stop_typewriting)
    stop_btn.pack(side=tk.LEFT, padx=5)

    root.mainloop()


if __name__ == "__main__":
    main()
