import random
import time
import curses
from curses import wrapper
import sys
import json
import os
import click

LANGUAGES_DIR = "./languages"


def load_word_list(language_name):
    file_path = os.path.join(LANGUAGES_DIR, f"{language_name}.json")
    if not os.path.exists(file_path):
        raise ValueError(f"Language file {language_name}.json not found.")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "words" not in data:
        raise ValueError(
            f"Invalid format in {language_name}.json, 'words' field not found."
        )

    return data["words"]


def load_groups():
    groups_file = os.path.join(LANGUAGES_DIR, "_groups.json")
    with open(groups_file, "r", encoding="utf-8") as f:
        return json.load(f)


def get_random_words(word_list, num_words):
    return " ".join(random.choices(word_list, k=num_words))


def draw_centered_text(stdscr, y, text, color_pair=0):
    screen_height, screen_width = stdscr.getmaxyx()
    start_x = max(0, (screen_width - len(text)) // 2)
    stdscr.addstr(y, start_x, text, color_pair)


def draw_text(stdscr, target, current, current_pos, wpm=0, time_left=0):
    screen_height, screen_width = stdscr.getmaxyx()
    lines = [target[i : i + 60] for i in range(0, len(target), 60)]

    draw_centered_text(
        stdscr, screen_height // 2 - 5, f"WPM: {wpm} | Time left: {time_left:.1f}s"
    )

    for i, line in enumerate(lines[current_pos : current_pos + 3]):
        y = screen_height // 2 - 2 + i
        x = (screen_width - 60) // 2
        for j, char in enumerate(line):
            current_idx = current_pos * 60 + i * 60 + j
            if current_idx >= len(current):
                stdscr.addstr(y, x + j, char, curses.color_pair(3))
            elif char == current[current_idx]:
                stdscr.addstr(y, x + j, char, curses.color_pair(1))
            else:
                stdscr.addstr(y, x + j, char, curses.color_pair(2))

            if current_idx == len(current):
                stdscr.addstr(y, x + j, char, curses.color_pair(4) | curses.A_REVERSE)


def wpm_test(stdscr, word_list, test_duration):
    target_text = get_random_words(word_list, 100)
    current_text = []
    wpm = 0
    start_time = None
    stdscr.nodelay(True)
    current_pos = 0

    while True:
        if start_time:
            time_elapsed = time.time() - start_time
        else:
            time_elapsed = 0

        time_left = max(test_duration - time_elapsed, 0)
        if time_elapsed > 0:
            wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.erase()
        draw_text(stdscr, target_text, current_text, current_pos, wpm, time_left)
        stdscr.refresh()

        if time_left <= 0:
            break

        if len(current_text) >= (current_pos + 3) * 60:
            current_pos += 3

        if len(current_text) == len(target_text):
            target_text = get_random_words(word_list, 100)
            current_text = []
            current_pos = 0

        try:
            key = stdscr.get_wch()
        except curses.error:
            continue

        if key == curses.KEY_BACKSPACE or key in ("\b", "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif isinstance(key, str) and len(current_text) < len(target_text):
            current_text.append(key)
            if start_time is None:
                start_time = time.time()

    return wpm, current_text, target_text


def show_results(stdscr, wpm, accuracy):
    stdscr.clear()
    screen_height, screen_width = stdscr.getmaxyx()

    draw_centered_text(stdscr, screen_height // 2 - 2, "Test completed!")
    draw_centered_text(stdscr, screen_height // 2, f"WPM: {wpm}")
    draw_centered_text(stdscr, screen_height // 2 + 2, f"Accuracy: {accuracy:.2f}%")
    draw_centered_text(
        stdscr, screen_height // 2 + 4, "Press 'r' to restart or 'q' to quit"
    )

    while True:
        key = stdscr.getch()
        if key == ord("r"):
            return True
        elif key == ord("q"):
            return False


@click.group()
def cli():
    pass


@cli.command()
def list_dictionaries():
    groups = load_groups()
    click.echo("Available dictionaries:")
    for group in groups:
        click.echo(f"- {group['name']}: {', '.join(group['languages'])}")


@cli.command()
@click.argument("query", type=str)
def search_dictionaries(query):
    groups = load_groups()
    found = []
    for group in groups:
        for lang in group["languages"]:
            if query.lower() in lang.lower():
                found.append(lang)

    if found:
        click.echo(f"Dictionaries matching '{query}':")
        for lang in found:
            click.echo(f"- {lang}")
    else:
        click.echo(f"No dictionaries found for query: {query}")


@cli.command()
@click.argument("test_duration", type=int)
@click.argument("dictionary", type=str)
def run(test_duration, dictionary):
    word_list = load_word_list(dictionary)

    wrapper(lambda stdscr: run_wpm_test(stdscr, word_list, test_duration))


def run_wpm_test(stdscr, word_list, test_duration):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_RED, -1)
    curses.init_pair(3, curses.COLOR_WHITE, -1)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.curs_set(0)

    while True:
        wpm, current_text, target_text = wpm_test(stdscr, word_list, test_duration)
        accuracy = (
            sum(1 for c, t in zip(current_text, target_text) if c == t)
            / len(current_text)
            * 100
            if current_text
            else 0
        )

        if not show_results(stdscr, wpm, accuracy):
            break


if __name__ == "__main__":
    cli()
