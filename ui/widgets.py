import customtkinter as ctk
import os
from .theme import Theme

class FileListRow(ctk.CTkFrame):
    """A row in the file list showing file name and a remove button."""
    def __init__(self, master, file_path, remove_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.file_path = file_path
        
        self.name_label = ctk.CTkLabel(self, text=os.path.basename(file_path), anchor="w")
        self.name_label.pack(side="left", padx=10, fill="x", expand=True)
        
        self.remove_btn = ctk.CTkButton(self, text="×", width=30, fg_color="transparent", 
                                       hover_color=Theme.COLORS['error'], command=lambda: remove_callback(self))
        self.remove_btn.pack(side="right", padx=5)

class DropZone(ctk.CTkFrame):
    """A specialized frame for drag & drop file input."""
    def __init__(self, master, title, callback, **kwargs):
        super().__init__(master, border_width=2, border_color=Theme.COLORS['accent'], **kwargs)
        
        self.label = ctk.CTkLabel(self, text=f"Drag & Drop {title} Here\nor Click to Browse", 
                                 font=Theme.FONTS['header'])
        self.label.place(relx=0.5, rely=0.5, anchor="center")
        
        self.bind("<Button-1>", lambda e: callback())
        self.label.bind("<Button-1>", lambda e: callback())
