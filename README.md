# YouTube Transcript Downloader

A lightweight desktop app for downloading and managing YouTube video transcripts.  
Built with Python and [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter), featuring a clean dark-mode UI.

---

## Features

- 🎥 Extract transcripts from any public YouTube video  
- 📝 Save transcripts as plain text  
- 🧠 View transcript history  
- 🌓 Dark mode–only modern interface  
- ⚙️ Auto-saves user settings (e.g., last used save path)  

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/youtube-transcript-downloader.git
cd youtube-transcript-downloader
```

(Optional) Create a virtual environment:

```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
Install dependencies:
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the app:
```bash
python main.py
```

## Requirements
Python 3.9 or higher
Internet connection (required to fetch transcripts)

## Notes
- Supports only videos with available english subtitles (manual or auto-generated)
- Videos with disabled captions are not supported
- Interface is designed for dark mode only

## License
MIT License. See the LICENSE file.

## Credits
- YouTube Transcript API
- CustomTkinter
