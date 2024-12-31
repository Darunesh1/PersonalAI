# Personal AI Assistant

## Overview

The **Personal AI Assistant** is a versatile, voice-controlled program designed to perform a wide range of tasks including searching the web, providing weather updates, managing emails, playing music, retrieving news, solving calculations, and even fetching movie details. The assistant interacts with users through voice commands, making it highly user-friendly and accessible.

## Features

- **Voice Recognition**: Recognizes and processes voice commands.
- **Task Automation**: Opens applications like Notepad, Command Prompt, Camera, and more.
- **Web Search**: Searches on Google, Wikipedia, and YouTube.
- **Weather Updates**: Provides weather forecasts for any city.
- **News Retrieval**: Fetches the latest news headlines.
- **Movie Information**: Retrieves movie ratings, cast, and plot summaries.
- **Calculations and Queries**: Uses WolframAlpha to solve mathematical problems and answer general queries.
- **Email Functionality**: Sends emails directly from the assistant.
- **IP Address Retrieval**: Fetches the system's public IP address.
- **Custom Hotkeys**: Pause/resume and exit the assistant with keyboard shortcuts.

## Installation

***Note**: It has been observed that the `siap5` sound module doesn't work well on Linux systems. For better performance and compatibility, it's recommended to use alternative sound modules like **`pyaudio`** or **`sounddevice`** for voice recognition and audio tasks.

### Recommended Alternatives:

1. **[pyaudio](https://pypi.org/project/PyAudio/)** - A popular Python library for working with audio, ideal for voice recognition tasks. You can install it using `pip install pyaudio`.

2. **[sounddevice](https://python-sounddevice.readthedocs.io/)** - A simple and easy-to-use library for playing and recording sound, compatible with Linux. Install it with `pip install sounddevice`.

Additionally, for fetching news and weather data, here are some useful APIs:

1. **[Newsdata.io](https://newsdata.io/documentation)** - A reliable API for fetching news from various sources. You can find more details and create an API key [here](https://newsdata.io/documentation).
   
2. **[OpenWeatherMap](https://openweathermap.org/api)** - Provides accurate weather data. You can create an API key [here](https://openweathermap.org/api).

By using these alternatives and APIs, you can seamlessly integrate voice recognition and data fetching tasks into your application with better support across different platforms.



1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and configure it with your credentials:
   ```env
   USER="<Your Name>"
   BOT="<Bot Name>"
   EMAIL="<Your Email Address>"
   PASSWORD="<Your Email passkey !!>"
   NEWS="<Your News API Key>"
   WEATHER="<Your WEATHER API Key>"
   APP_ID="<Your WolframAlpha App ID>"
   ```

## Usage

1. Run the assistant:
   ```bash
   python main.py
   ```

2. Interact with the assistant using voice commands such as:
   - "Open Notepad"
   - "Search on Google"
   - "What's the weather in Chennai?"
   - "What is the plot of Inception?"

3. Use the following hotkeys:
   - **Ctrl + Alt + K**: Pause/Resume listening.
   - **Ctrl + Alt + E**: Exit the assistant.

## Contributing

Contributions are welcome! Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-branch-name
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add a descriptive commit message"
   ```
4. Push your changes:
   ```bash
   git push origin feature-branch-name
   ```
5. Open a pull request on GitHub.

## Acknowledgments

- **Python**: The core programming language for the assistant.
- **Pyttsx3**: For text-to-speech functionality.
- **SpeechRecognition**: For voice recognition.
- **WolframAlpha**: For calculations and knowledge queries.
- **IMDbPy**: For fetching movie details.
- **Requests**: For handling API requests.
- **Decouple**: For managing environment variables.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.


**Note**: An experimental version with a GUI is available in the development branch. Please use it at your own discretion, as it may not be fully stable.








