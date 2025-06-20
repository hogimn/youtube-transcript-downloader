import re
import html
import requests

YOUTUBE_ID_PATTERN = re.compile(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*")

def extract_video_id(input_text: str) -> str:
    """
    Extract YouTube video ID from a URL or plain video ID string.
    """
    input_text = input_text.strip()
    if len(input_text) == 11 and re.fullmatch(r"[0-9A-Za-z_-]{11}", input_text):
        return input_text
    match = YOUTUBE_ID_PATTERN.search(input_text)
    if match:
        return match.group(1)
    return ""

def fetch_video_title(video_id: str) -> str:
    """
    Fetch the video title by scraping YouTube video page meta tag.
    Returns empty string if fails.
    """
    url = f"https://www.youtube.com/watch?v={video_id}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        html_text = res.text
        match = re.search(r'<meta name="title" content="([^"]+)">', html_text)
        if match:
            raw_title = match.group(1)
            return html.unescape(raw_title)
    except Exception:
        pass
    return ""
