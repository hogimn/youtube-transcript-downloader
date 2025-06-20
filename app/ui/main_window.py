import os
import re
import sys
import subprocess
import customtkinter as ctk
from tkinter import filedialog, messagebox

from app.config.settings_manager import SettingsManager
from app.services.transcript_service import TranscriptService
from app.services.history_manager import HistoryManager
from app.services.video_utils import extract_video_id, fetch_video_title
from app.ui.history_view import HistoryView


class MainWindow(ctk.CTk):
    """
    Main application window integrating UI components
    and business logic for transcript downloading.
    """

    ITEMS_PER_PAGE = 5

    def __init__(self):
        super().__init__()

        # Window config
        self.title("🎬 YouTube Transcript Downloader")
        self.geometry("600x500")
        self.minsize(550, 700)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.custom_font = ctk.CTkFont(family="Segoe UI", size=14)
        self.title_font = ctk.CTkFont(family="Segoe UI Semibold", size=24)

        # Load settings and services
        self.settings = SettingsManager().load()
        self.transcript_service = TranscriptService(self.settings)
        self.history_manager = HistoryManager(self.settings.get("save_path"))

        self._setup_ui()

        # Load history and update UI
        self.history_manager.load_recent_history()
        self.history_view.update_videos(self.history_manager.recent_videos)

    def _setup_ui(self):
        """
        Setup all UI components for the main window.
        """
        self.configure(fg_color="#121212")

        # Title label
        self.label_title = ctk.CTkLabel(self, text="YouTube Transcript Downloader", font=self.title_font, text_color="#F0F0F0")
        self.label_title.pack(pady=(20, 5))

        # Input frame with entry and download button
        input_frame = ctk.CTkFrame(self, fg_color="#1f2937", corner_radius=12)
        input_frame.pack(pady=10, padx=30, fill="x")

        self.entry_video = ctk.CTkEntry(input_frame, placeholder_text="Enter YouTube Video URL or ID", font=self.custom_font, height=40, corner_radius=12)
        self.entry_video.pack(side="left", fill="x", expand=True, padx=(12, 8), pady=12)

        self.btn_fetch = ctk.CTkButton(input_frame, text="⬇️ Download", font=self.custom_font, width=130, height=40, corner_radius=12, fg_color="#2563EB", hover_color="#1D4ED8", command=self.fetch_transcript)
        self.btn_fetch.pack(side="right", padx=(0, 12), pady=12)

        # Status label for download feedback
        self.status_label = ctk.CTkLabel(self, text="", font=self.custom_font, text_color="#9CA3AF", wraplength=550, justify="left", height=0)
        self.status_label.pack(pady=(0, 3))

        # Path frame with path display and control buttons
        path_frame = ctk.CTkFrame(self, fg_color="#1f2937", corner_radius=12)
        path_frame.pack(pady=5, padx=30, fill="x")

        self.label_path = ctk.CTkLabel(path_frame, text=f"📁 {self.settings['save_path']}", font=self.custom_font, text_color="#A1A1AA", anchor="w")
        self.label_path.pack(fill="x", padx=15, pady=(10, 5))

        buttons_frame = ctk.CTkFrame(path_frame, fg_color="#1f2937", corner_radius=0)
        buttons_frame.pack(fill="x", padx=15, pady=(0, 10))

        self.btn_choose_folder = ctk.CTkButton(buttons_frame, text="Change Folder", width=140, height=30, corner_radius=12, fg_color="#F59E0B", hover_color="#B45309", command=self.choose_folder)
        self.btn_choose_folder.pack(side="left", padx=(0, 10))

        self.btn_open_folder = ctk.CTkButton(buttons_frame, text="Open Folder", width=120, height=30, corner_radius=12, fg_color="#10B981", hover_color="#059669", command=self.open_save_folder)
        self.btn_open_folder.pack(side="left", padx=(0, 10))

        self.btn_copy_path = ctk.CTkButton(buttons_frame, text="Copy Path", width=110, height=30, corner_radius=12, fg_color="#3B82F6", hover_color="#2563EB", command=self.copy_save_path)
        self.btn_copy_path.pack(side="left")

        # Recent downloads section
        self.label_history_title = ctk.CTkLabel(self, text="Recent Downloads:", font=ctk.CTkFont(size=16, weight="bold"), text_color="#E5E7EB", anchor="w")
        self.label_history_title.pack(pady=(10, 5), padx=30, fill="x")

        # History view component handles display & pagination of recent items
        self.history_view = HistoryView(self, self.ITEMS_PER_PAGE, self.open_transcript_in_notepad)
        self.history_view.pack(pady=5, padx=30, fill="x")

    def choose_folder(self):
        """
        Open directory selection dialog and update save path and UI accordingly.
        """
        folder = filedialog.askdirectory(initialdir=self.settings.get("save_path"))
        if folder:
            self.settings["save_path"] = folder
            SettingsManager().save(self.settings)
            self.label_path.configure(text=f"📁 {folder}")

            # Reload history manager and update history view
            self.history_manager.save_folder = folder
            self.history_manager.load_recent_history()
            self.history_view.update_videos(self.history_manager.recent_videos)

    def copy_save_path(self):
        """
        Copy the current save path to clipboard and update status message.
        """
        self.clipboard_clear()
        self.clipboard_append(self.settings["save_path"])
        self.status_label.configure(text="📋 Save path copied to clipboard!")

    def open_save_folder(self):
        """
        Open the save folder in the OS file explorer.
        """
        folder = self.settings.get("save_path")
        if os.path.exists(folder):
            if os.name == "nt":
                os.startfile(folder)
            elif os.name == "posix":
                if sys.platform == "darwin":
                    subprocess.run(["open", folder])
                else:
                    subprocess.run(["xdg-open", folder])
            else:
                messagebox.showwarning("Warning", "Opening folder is not supported on this OS.")
        else:
            messagebox.showerror("Error", "Save folder does not exist.")

    def open_transcript_in_notepad(self, filepath):
        """
        Open a transcript text file in Notepad (Windows only).
        """
        if os.path.exists(filepath):
            if os.name == "nt":
                subprocess.Popen(['notepad.exe', filepath])
            else:
                messagebox.showwarning("Warning", "Open in Notepad is supported only on Windows.")
        else:
            messagebox.showerror("Error", f"File not found:\n{filepath}")

    def fetch_transcript(self, video_id=None):
        """
        Download transcript given a video ID or input field value,
        save it, update UI and recent downloads list.
        """
        if video_id is None:
            input_text = self.entry_video.get()
            video_id = extract_video_id(input_text)
            if not video_id:
                messagebox.showerror("Error", "Invalid YouTube video URL or ID.")
                return

        title = fetch_video_title(video_id)

        self.status_label.configure(text="⏳ Downloading transcript...")
        self.update()

        try:
            # Clean filename from invalid chars
            safe_title = re.sub(r'[\\/:*?"<>|]', '_', title or video_id)
            filename = f"[YTTrans]_{video_id}_{safe_title}.txt"
            save_path = os.path.join(self.settings['save_path'], filename)

            self.transcript_service.fetch_and_save_custom_path(video_id, title, save_path)
        except Exception as e:
            self.status_label.configure(text="")
            messagebox.showerror("Error", str(e))
            return

        self.status_label.configure(text=f"✅ Transcript saved:\n{save_path}")

        # Update history with new transcript info (remove duplicates, insert at front)
        self.history_manager.load_recent_history()  # Reload to sync with disk
        self.history_view.update_videos(self.history_manager.recent_videos)

        self.open_transcript_in_notepad(save_path)
