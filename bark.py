from src import commands as c
from src import presentation as p


def loop():
    options = {
        "A": p.Option(
            name="Add a bookmark",
            command=c.AddBookmarkCommand()
        ),
        "B": p.Option(
            name="List bookmarks by date",
            command=c.ListBookmarksCommand()
        ),
        "T": p.Option(
            name="List bookmarks by title",
            command=c.ListBookmarksCommand(order_by="title")
        ),
        "D": p.Option(
            name="Delete bookmark",
            command=c.DeleteBookmarkCommand()
        ),
        "Q": p.Option(
            name="Quit",
            command=c.QuitCommand()
        )
    }

    p.clear_screen()
    p.print_options(options)
    chosen_option = p.get_option_choice(options)
    p.clear_screen()
    chosen_option.choose()

    _ = input("Press ENTER to return to menu")

if __name__ == "__main__":
    c.CreateBookmarksTableCommand().execute()
    print("Welcome to Bark!")

    while True:
        loop()
