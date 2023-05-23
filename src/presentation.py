""" A module for the presentation layer """

import os
import typing as t

from src.commands import Command


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


def get_new_debtor_data() -> t.Dict[str, t.Optional[str]]:
    result = {
        "name": get_user_input("Name"),
        "sum_owed": get_user_input("Sum owed"),
        "date_due": get_user_input("Date due"),
        "notes": get_user_input("Notes", required=False),
    }

    return result


def get_debtor_id() -> int:
    result = int(get_user_input("Enter a Debtor's ID"))  
    return result


def get_update_debtor_data() -> t.Dict[str, t.Union[int, t.Dict[str, str]]]:
    Debtor_id = int(get_user_input("Enter a Debtor ID to edit"))
    field = get_user_input("Choose a value to edit (name, sum_owed, date_due, notes)")
    new_value = get_user_input(f"Enter a new value for {field}")
    return {"id": Debtor_id, "update": {field: new_value}}


def clear_screen():
    clear_command = "cls" if os.name == "nt" else "clear"
    os.system(clear_command)