import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog, messagebox
from ui.theme import Theme
from ui.widgets import FileListRow, DropZone
from converters.image import ImageConverter
from converters.audio import AudioConverter
from converters.video import VideoConverter
from converters.document import DocumentConverter
import os
import threading
from pathlib import Path

class FileCon(ctk.CTk, TkinterDnD.DnDWrapper):
    """Main application class for FileCon."""
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._retrieve(self)
        
        self.title("FileCon - The Ultimate File Converter")
        self.geometry("1100x800")
        self.minsize(900, 700)
        
        # Initialize Converters
        self.converters = {
            "Images": ImageConverter(),
            "Audio": AudioConverter(),
            "Video": VideoConverter(),
            "Documents": DocumentConverter()
        }
        
        # Application State
        self.output_dir = str(Path.home() / "FileCon_Conversions")
        
        # UI Setup
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="FileCon", font=Theme.FONTS['title'], text_color=Theme.COLORS['accent'])
        self.logo_label.pack(pady=40, padx=20)
        
        self.nav_buttons = {}
        for tab in ["Images", "Audio", "Video", "Documents"]:
            btn = ctk.CTkButton(self.sidebar, text=tab, height=40, corner_radius=8,
                               command=lambda t=tab: self.show_tab(t))
            btn.pack(pady=10, padx=20, fill="x")
            self.nav_buttons[tab] = btn
        
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar, values=["Light", "Dark", "System"],
                                                               command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.pack(side="bottom", padx=20, pady=(10, 30))
        self.appearance_mode_optionemenu.set("Dark")

        # Main Content
        self.main_content = ctk.CTkFrame(self, corner_radius=15, fg_color="transparent")
        self.main_content.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        self.tabview = ctk.CTkTabview(self.main_content)
        self.tabview.pack(fill="both", expand=True)
        
        self.tab_data = {}
        for tab in ["Images", "Audio", "Video", "Documents"]:
            self.setup_tab(tab)

        # Bottom Bar (Progress & Global Actions)
        self.bottom_bar = ctk.CTkFrame(self.main_content, height=100, fg_color="transparent")
        self.bottom_bar.pack(fill="x", side="bottom", pady=(20, 0))
        
        self.progress_bar = ctk.CTkProgressBar(self.bottom_bar, width=600)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)
        
        self.convert_btn = ctk.CTkButton(self.bottom_bar, text="CONVERT ALL", font=Theme.FONTS['header'],
                                        fg_color=Theme.COLORS['success'], hover_color="#00aa55",
                                        height=50, command=self.start_conversion)
        self.convert_btn.pack(pady=10)

    def setup_tab(self, tab_name):
        tab = self.tabview.add(tab_name)
        
        # Left side: Drop zone & List
        left_frame = ctk.CTkFrame(tab, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        drop_zone = DropZone(left_frame, tab_name, lambda: self.browse_files(tab_name), height=150)
        drop_zone.pack(fill="x", pady=(0, 10))
        drop_zone.drop_target_register(DND_FILES)
        drop_zone.dnd_bind('<<Drop>>', lambda e: self.handle_drop(e, tab_name))
        
        scroll_frame = ctk.CTkScrollableFrame(left_frame, label_text="Selected Files")
        scroll_frame.pack(fill="both", expand=True)
        
        # Right side: Options
        right_frame = ctk.CTkFrame(tab, width=250)
        right_frame.pack(side="right", fill="y", padx=10, pady=10)
        
        ctk.CTkLabel(right_frame, text="Conversion Options", font=Theme.FONTS['header']).pack(pady=20, padx=10)
        
        # Format selection
        formats = {
            "Images": ["PNG", "JPEG", "WEBP", "ICO", "BMP"],
            "Audio": ["MP3", "WAV", "FLAC", "OGG", "AAC"],
            "Video": ["MP4", "MKV", "MOV", "AVI", "WEBM", "MP3 (Audio)"],
            "Documents": ["PDF"]
        }
        
        ctk.CTkLabel(right_frame, text="Output Format:").pack(anchor="w", padx=20)
        format_menu = ctk.CTkOptionMenu(right_frame, values=formats[tab_name])
        format_menu.pack(pady=10, padx=20, fill="x")
        
        # Save data
        self.tab_data[tab_name] = {
            "scroll_frame": scroll_frame,
            "format_menu": format_menu,
            "files": []
        }

    def browse_files(self, tab_name):
        file_types = {
            "Images": [("Image files", "*.png *.jpg *.jpeg *.webp *.bmp *.gif")],
            "Audio": [("Audio files", "*.mp3 *.wav *.flac *.ogg *.m4a *.aac")],
            "Video": [("Video files", "*.mp4 *.mkv *.mov *.avi *.webm")],
            "Documents": [("Document files", "*.docx *.txt *.md")]
        }
        paths = filedialog.askopenfilenames(filetypes=file_types[tab_name])
        if paths:
            self.add_files(paths, tab_name)

    def handle_drop(self, event, tab_name):
        files = self.tk.splitlist(event.data)
        self.add_files(files, tab_name)

    def add_files(self, paths, tab_name):
        for path in paths:
            if path not in self.tab_data[tab_name]["files"]:
                self.tab_data[tab_name]["files"].append(path)
                row = FileListRow(self.tab_data[tab_name]["scroll_frame"], path, 
                                 lambda r: self.remove_file(r, tab_name))
                row.pack(fill="x", pady=2, padx=5)

    def remove_file(self, row, tab_name):
        self.tab_data[tab_name]["files"].remove(row.file_path)
        row.destroy()

    def show_tab(self, tab_name):
        self.tabview.set(tab_name)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def start_conversion(self):
        tab_name = self.tabview.get()
        files = self.tab_data[tab_name]["files"]
        if not files:
            messagebox.showwarning("No Files", "Please add some files to convert first!")
            return
            
        target_format = self.tab_data[tab_name]["format_menu"].get()
        if " (Audio)" in target_format:
            target_format = target_format.replace(" (Audio)", "")
            
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
        self.convert_btn.configure(state="disabled", text="CONVERTING...")
        threading.Thread(target=self.run_conversion, args=(tab_name, files, target_format), daemon=True).start()

    def run_conversion(self, tab_name, files, target_format):
        converter = self.converters[tab_name]
        options = {"format": target_format}
        
        def update_progress(val):
            self.after(0, lambda: self.progress_bar.set(val / 100))
            
        results = converter.batch_convert(files, self.output_dir, options, update_progress)
        
        success_count = sum(1 for r in results if r['success'])
        self.after(0, lambda: self.finish_conversion(success_count, len(files)))

    def finish_conversion(self, success, total):
        self.convert_btn.configure(state="normal", text="CONVERT ALL")
        self.progress_bar.set(0)
        messagebox.showinfo("Done", f"Converted {success} of {total} files successfully!\nFiles saved to: {self.output_dir}")

if __name__ == "__main__":
    app = FileCon()
    print("FileCon Application Ready.")
    # app.mainloop()
