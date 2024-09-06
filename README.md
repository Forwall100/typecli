# Typecli

A customizable, multi-language typing speed test application with a command-line interface.

## Description

This Typing Simulator is a Python-based application that allows users to practice and measure their typing speed in various languages. It features a curses-based interface for real-time feedback, supports multiple dictionaries, and provides detailed results including words per minute (WPM) and accuracy.

## Features

- Multi-language support (thanks [monkeytype](https://github.com/monkeytypegame/monkeytype))
- Customizable test duration
- Real-time WPM and time remaining display
- Color-coded feedback for correct and incorrect typing
- Final results showing WPM and accuracy
- Command-line interface for easy management of dictionaries

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/typing-simulator.git
   cd typing-simulator
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

The application provides several commands through its command-line interface:

### List available dictionaries

To see all available language dictionaries:

```
python main.py list-dictionaries
```

### Search for dictionaries

To search for a specific dictionary:

```
python main.py search-dictionaries <query>
```

Replace `<query>` with your search term.

### Run a typing test

To start a typing test:

```
python main.py run <test_duration> <dictionary>
```

- `<test_duration>`: The duration of the test in seconds
- `<dictionary>`: The name of the dictionary to use (e.g., "english", "spanish")

Example:
```
python main.py run 60 english
```

This will start a 60-second typing test using the English dictionary.

## During the Test

- Type the words shown on the screen.
- Green text indicates correct typing, red indicates mistakes.
- The cursor position is highlighted.
- Current WPM and time remaining are displayed at the top.
- Press Backspace to correct mistakes.
- The test ends automatically when the time is up.

## After the Test

- Your final WPM and accuracy will be displayed.
- Press 'r' to restart with the same settings or 'q' to quit.

## Customization

You can add new dictionaries by creating JSON files in the `./languages` directory. Each file should contain a "words" array with the words for that language.
