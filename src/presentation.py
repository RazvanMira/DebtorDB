""" A module for the presentation layer """

import os
import typing as t

from commands import Command


class Option:
    def __init__(
        self, name: str, command: Command, prep_call: t.Optional[t.Callable] = None
    ):
        self.name = name
        self.command = command
        self.prep_call = prep_call

    def choose(self):
        data = self.prep_call() if self.prep_call else None
        result = self.command.execute(data) if data else self.command.execute()
        if isinstance(result, list):
            for line in result:
                print(line)
        else:
            print(result)

    def __str__(self):
        return self.name


def print_options(options: t.Dict[str, Option]) -> None:
    for shortcut, option in options.items():
        print(f"({shortcut}) {option}")
    print()


def option_choice_is_valid(choice: str, options: t.Dict[str, Option]) -> bool:
    result = choice in options or choice.upper() in options
    return result


def get_option_choice(options: t.Dict[str, Option]) -> Option:
    choice = input("Choose an option: ")
    while not option_choice_is_valid(choice, options):
        print("Invalid choice")
        choice = input("Choose an option: ")
    return options[choice.upper()]


def get_user_input(label: str, required: bool = True) -> t.Optional[str]:
    value = input(f"{label}: ") or None
    while required and not value:
        value = input(f"{label}: ") or None
    return value


def get_new_bookmark_data() -> t.Dict[str, t.Optional[str]]:
    result = {
        "title": get_user_input("Title"),
        "url": get_user_input("URL"),
        "notes": get_user_input("Notes", required=False),
    }

    return result


def get_bookmark_id() -> int:
    result = int(get_user_input("Enter a bookmark ID"))  
    return result


def get_update_bookmark_data() -> t.Dict[str, t.Union[int, t.Dict[str, str]]]:
    bookmark_id = int(get_user_input("Enter a bookmark ID to edit"))
    field = get_user_input("Choose a value to edit (title, url, notes)")
    new_value = get_user_input(f"Enter a new value for {field}")
    return {"id": bookmark_id, "update": {field: new_value}}


def get_github_import_options() -> t.Dict[str, t.Union[str, bool]]:
    github_username = get_user_input("Please input the Github username")
    preserve_timestamps = get_user_input("Preserve timestamps? [Y/n]")

    if preserve_timestamps in ["Y", "y", ""]:
        preserve_timestamps = True
    else:
        preserve_timestamps = False

    return {
        "github_username": github_username,
        "preserve_timestamps": preserve_timestamps,
    }


def get_file_name() -> str:
    file_name = get_user_input(
        "Please type in the name of the Excel file where you want to save"
    )
    return file_name


def clear_screen():
    clear_command = "cls" if os.name == "nt" else "clear"
    os.system(clear_command)