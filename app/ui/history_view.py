import tkinter as tk
import customtkinter as ctk

class HistoryView(ctk.CTkFrame):
    """
    UI component for displaying recent transcripts history with pagination.
    """
    def __init__(self, master, items_per_page, on_item_click):
        """
        :param master: Parent widget
        :param items_per_page: Number of items to show per page
        :param on_item_click: Callback function when a history item is clicked.
                              Should accept the transcript file path as argument.
        """
        super().__init__(master, fg_color="#1f2937", corner_radius=12)

        self.items_per_page = items_per_page
        self.on_item_click = on_item_click
        self.page = 0
        self.videos = []

        # Frame for list buttons (top area)
        self.list_frame = ctk.CTkFrame(self, fg_color="#1f2937")
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.history_buttons = []
        for _ in range(items_per_page):
            btn = tk.Button(
                self.list_frame,
                text="",
                font=("Segoe UI", 10),
                anchor="w",
                state="disabled",
                relief="flat",
                bd=0,
                padx=10,
                bg="#374151",
                fg="#D1D5DB",
                activebackground="#4B5563",
                command=lambda: None  # placeholder, updated dynamically
            )
            btn.pack(pady=5, fill="x")
            self.history_buttons.append(btn)

        # Frame for pagination controls (bottom area)
        self.pagination_frame = ctk.CTkFrame(self, fg_color="#1f2937")
        self.pagination_frame.pack(side="bottom", fill="x", pady=(0, 10), padx=10)

        self.btn_prev = ctk.CTkButton(
            self.pagination_frame,
            text="⬅️ Prev",
            width=80,
            command=self.prev_page
        )
        self.btn_prev.pack(side="left", padx=10, pady=5)

        self.label_page_info = ctk.CTkLabel(
            self.pagination_frame,
            text="",
            font=ctk.CTkFont(size=14)
        )
        self.label_page_info.pack(side="left", expand=True, pady=5)

        self.btn_next = ctk.CTkButton(
            self.pagination_frame,
            text="Next ➡️",
            width=80,
            command=self.next_page
        )
        self.btn_next.pack(side="right", padx=10, pady=5)

    def update_videos(self, videos):
        """
        Update the history list and reset pagination.
        """
        self.videos = videos
        self.page = 0
        self.update_view()

    def update_view(self):
        """
        Update the UI buttons and page info for the current page.
        """
        total_pages = max(1, (len(self.videos) + self.items_per_page - 1) // self.items_per_page)

        # Clamp page number
        if self.page < 0:
            self.page = 0
        if self.page >= total_pages:
            self.page = total_pages - 1

        start = self.page * self.items_per_page
        end = start + self.items_per_page
        page_items = self.videos[start:end]

        for i, btn in enumerate(self.history_buttons):
            if i < len(page_items):
                video = page_items[i]
                btn.configure(
                    text=video['title'],
                    state="normal",
                    command=lambda fp=video['filepath']: self.on_item_click(fp),
                    bg="#374151",
                    fg="#D1D5DB",
                    activebackground="#4B5563"
                )
            else:
                btn.configure(text="", state="disabled", command=lambda: None)

        self.label_page_info.configure(text=f"Page {self.page + 1} / {total_pages}")
        self.btn_prev.configure(state="normal" if self.page > 0 else "disabled")
        self.btn_next.configure(state="normal" if self.page < total_pages - 1 else "disabled")

    def next_page(self):
        """
        Move to the next page and update view.
        """
        self.page += 1
        self.update_view()

    def prev_page(self):
        """
        Move to the previous page and update view.
        """
        self.page -= 1
        self.update_view()
