# import tkinter as tk

# root = tk.Tk()
# root.title("Scrollable Root Window")
# root.geometry("500x400")

# # Create canvas and scrollbar
# canvas = tk.Canvas(root)
# scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
# scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
# canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# # Configure canvas to work with scrollbar
# canvas.configure(yscrollcommand=scrollbar.set)
# canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# # Create a frame inside the canvas
# scrollable_frame = tk.Frame(canvas)
# canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# # Add sample widgets to the scrollable frame
# for i in range(50):
#     tk.Label(scrollable_frame, text=f"Item {i+1}", font=("Arial", 12)).pack(pady=2)

# root.mainloop()

import tkinter as tk
from tkinter import ttk

def create_scrollable_root():
    root = tk.Tk()
    root.title("Scrollable Root Window")
    
    # Create main container frame
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Create canvas with scrollbar
    canvas = tk.Canvas(main_frame)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    # Configure scroll region
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    
    # Set up canvas
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Pack widgets
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Add mouse wheel scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    # For Linux mouse wheel
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
    
    # Add some sample content to demonstrate scrolling
    for i in range(50):
        ttk.Label(scrollable_frame, text=f"Label {i}").pack(pady=5)
    
    return root, scrollable_frame

# Usage
root, content_frame = create_scrollable_root()
root.mainloop()