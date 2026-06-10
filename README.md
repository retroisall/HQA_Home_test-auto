# HQA Home Test — Twitch WAP Automation

End-to-end test suite for Twitch using **Python + pytest + Selenium** with desktop Chrome.

## Demo

![record](record.gif)

## Folder Structure

```
project/
├─ tests/
│  └─ test_stream_search.py   # E2E test cases
├─ pages/
│  ├─ base_page.py            # Base class (waits, scroll, screenshot)
│  ├─ home_page.py            # Twitch homepage — open & search icon
│  ├─ search_page.py          # Search input, scroll, streamer selection
│  └─ live_page.py            # Streamer page — popups & screenshot
├─ screenshots/               # Auto-generated screenshots (git-ignored)
├─ conftest.py                # pytest fixture — desktop Chrome WebDriver setup
├─ pytest.ini                 # pytest configuration
└─ requirements.txt           # Python dependencies
```

## Test Scenario

| Step | Action |
|------|--------|
| 1 | Navigate to [twitch.tv](https://www.twitch.tv) |
| 2 | Click the search icon |
| 3 | Type **StarCraft II** |
| 4 | Scroll down **2 times** |
| 5 | Select the first available streamer |
| 6 | Wait for the stream to load and **take a screenshot** |

> The test also handles optional modals (mature content gate, subscription popup) automatically.

## Setup

```bash
# 1. Clone the repository
git clone https://github.com/retroisall/HQA_Home_test-auto.git
cd HQA_Home_test-auto

# 2. Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

## Run

```bash
pytest
```

Screenshots are saved to `screenshots/starcraft2_streamer.png` after each run.

## Tech Stack

- **Python 3.10+**
- **pytest** — test runner
- **Selenium 4** — browser automation
- **webdriver-manager** — automatic ChromeDriver management
- **opencv-python** — template matching for UI element detection
- **numpy** — image array processing
- **Pillow** — image capture and preprocessing
