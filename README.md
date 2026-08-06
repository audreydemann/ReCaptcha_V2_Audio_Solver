# ReCaptcha V2 Audio Solver

A Python-based solution to solve Google ReCaptcha V2 using audio challenges and local AI speech recognition.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen)

## Features

*   **Local Processing**: Uses `faster-whisper` (OpenAI Whisper) locally on CPU. No external API keys required.
*   **Selenium Integration**: Built for `selenium` and `undetected-chromedriver`.
*   **Smart Logic**: Handles "Multiple correct solutions required" and retry loops automatically.

## Installation

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2.  Ensure you have `ffmpeg` installed on your system (required for audio processing).

## Usage

```python
from driver.chrome_driver import create_driver
from solver import AudioCaptchaSolver

driver = create_driver()
driver.get("https://www.google.com/recaptcha/api2/demo")

solver = AudioCaptchaSolver(driver)
result = solver.solve()

print(f"Solved: {result}")
```

## Structure

*   `solver.py`: Core logic for captcha solving.
*   `driver/chrome_driver.py`: Helper to create undetected chrome instance.
*   `models/`: Directory where AI models are stored (downloaded automatically if missing).

## Disclaimer

This project is for educational purposes only.
