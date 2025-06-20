import os
import json
from typing import Dict


SETTINGS_FILE = "settings.json"
DEFAULT_SAVE_PATH = os.getcwd()


class SettingsManager:
    def __init__(self, file_path: str = SETTINGS_FILE):
        """
        Initialize the settings manager with the settings file path.
        """
        self.file_path = file_path

    def load(self) -> Dict[str, str]:
        """
        Load settings from the JSON file.

        Returns:
            dict: Settings dictionary. Defaults to {"save_path": DEFAULT_SAVE_PATH} if file missing or corrupted.
        """
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                # Could log the error here if needed
                pass

        # Return default settings if loading failed
        return {"save_path": DEFAULT_SAVE_PATH}

    def save(self, settings: Dict[str, str]) -> None:
        """
        Save the settings dictionary to the JSON file.

        Args:
            settings (dict): Settings to save.

        Raises:
            RuntimeError: If saving fails.
        """
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            raise RuntimeError(f"Failed to save settings: {e}")
