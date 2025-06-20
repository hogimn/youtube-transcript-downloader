import os
import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound
from youtube_transcript_api.formatters import TextFormatter


class TranscriptService:
    def __init__(self, settings: dict):
        """
        Initialize with app settings dict.
        """
        self.settings = settings

    def fetch_and_save(self, video_id: str, title: str = None) -> str:
        """
        Fetch transcript and save to a generated path based on settings and title or video_id.

        Returns the full saved file path.

        Raises:
            ValueError: If no English transcript is found.
            RuntimeError: On fetching or saving failure.
        """
        transcript_text = self._fetch_transcript_text(video_id)

        # Clean filename from title or video_id
        filename_base = title if title else video_id
        filename_base = re.sub(r'[\\/*?:"<>|]', "", filename_base)

        save_path = os.path.join(self.settings["save_path"], f"{filename_base}.txt")

        self._save_text_to_file(transcript_text, save_path)

        return save_path

    def fetch_and_save_custom_path(self, video_id: str, title: str, save_path: str) -> str:
        """
        Fetch transcript and save to a custom file path provided externally.

        Returns the full saved file path.

        Raises:
            ValueError: If no English transcript is found.
            RuntimeError: On fetching or saving failure.
        """
        transcript_text = self._fetch_transcript_text(video_id)

        # Ensure directory exists and save file
        self._save_text_to_file(transcript_text, save_path)

        return save_path

    def _fetch_transcript_text(self, video_id: str) -> str:
        """
        Internal helper to fetch and format transcript text for given video ID.

        Raises:
            ValueError: If no English transcript is found.
            RuntimeError: On other fetching errors.
        """
        try:
            transcript = YouTubeTranscriptApi().fetch(video_id, languages=["en"])
            formatter = TextFormatter()
            text = formatter.format_transcript(transcript)
            return text
        except NoTranscriptFound:
            raise ValueError("No English transcript found for this video.")
        except Exception as e:
            raise RuntimeError(f"Failed to fetch transcript: {e}")

    def _save_text_to_file(self, text: str, file_path: str):
        """
        Internal helper to save text content to the specified file path.

        Ensures parent directories exist.

        Raises:
            RuntimeError: On file writing errors.
        """
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text)
        except Exception as e:
            raise RuntimeError(f"Failed to save transcript: {e}")
