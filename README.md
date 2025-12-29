# Interviewer Helper

CV analysis and interview question generator powered by AI (Claude/Gemini).

## Download

### Pre-built Installers

Download the latest release for your platform:

| Platform | Download |
|----------|----------|
| Windows  | [InterviewerHelper.exe](../../releases/latest/download/InterviewerHelper.exe) |
| macOS    | [InterviewerHelper.dmg](../../releases/latest/download/InterviewerHelper.dmg) |

> **Note**: First release requires creating a GitHub Release to trigger the build workflow.

### Run from Source

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/InterviewerHelper.git
cd InterviewerHelper

# 2. Create virtual environment
python -m venv .venv

# 3. Activate
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Mac/Linux

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run app
python app.py
```

App will open at http://127.0.0.1:7860

## Features

- Upload CV (PDF) and analyze
- Input Job Description (free-text or structured)
- Generate interview questions with AI
- Score candidate fit (0-100)
- Save history with SQLite
- Bilingual support (EN/VI)
- Export to Markdown (bilingual)

## Configuration

1. Go to **Settings** tab
2. Enter your API keys:
   - **Gemini**: Get from https://aistudio.google.com/apikey
   - **Claude**: Get from https://console.anthropic.com/
3. Click **Save Settings**

## Build from Source

### Windows

```bash
pip install pyinstaller
pyinstaller --name "InterviewerHelper" --windowed --onefile --clean app.py
```

Output: `dist/InterviewerHelper.exe`

### macOS

```bash
pip install pyinstaller
pyinstaller --name "InterviewerHelper" --windowed --onefile --clean app.py
```

Output: `dist/InterviewerHelper`

## Creating a Release

1. Tag version: `git tag v1.0.0`
2. Push tag: `git push origin v1.0.0`
3. Create GitHub Release from tag
4. GitHub Actions will automatically build and attach installers

## License

MIT
