import os
import glob
import re

class HistoryManager:
    """
    Manages loading and paginating recent transcript files
    from the save folder.
    """
    def __init__(self, save_folder: str):
        self.save_folder = save_folder
        self.recent_videos = []  # List of dicts: {'id', 'title', 'filepath'}

    def load_recent_history(self):
        """
        Load transcript files matching pattern from save_folder,
        extract video ID and title from filename,
        and sort by last modified time descending.
        """
        if not os.path.isdir(self.save_folder):
            self.recent_videos = []
            return

        pattern = os.path.join(self.save_folder, "[[]YTTrans[]]_*.txt")
        files = glob.glob(pattern)

        videos = []
        for filepath in files:
            filename = os.path.basename(filepath)
            match = re.match(r"\[YTTrans\]_(.{11})_(.+)\.txt$", filename)
            if match:
                video_id = match.group(1)
                title = match.group(2).replace('_', ' ')
                videos.append({
                    "id": video_id,
                    "title": title,
                    "filepath": filepath
                })

        # Sort by modification time descending (most recent first)
        videos.sort(key=lambda x: os.path.getmtime(x['filepath']), reverse=True)
        self.recent_videos = videos

    def get_page(self, page_index: int, items_per_page: int):
        """
        Returns a slice of recent videos for the requested page.
        """
        start = page_index * items_per_page
        end = start + items_per_page
        return self.recent_videos[start:end]

    def get_total_pages(self, items_per_page: int) -> int:
        """
        Calculate total pages based on items per page.
        """
        if not self.recent_videos:
            return 1
        return (len(self.recent_videos) + items_per_page - 1) // items_per_page
