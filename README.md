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

