from src import commands as c
from src import presentation as p

if __name__ == "__main__":
    c.CreateBookmarksTableCommand().execute()
    print("Welcome to Bark!")

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

    p.print_options(options)

    chosen_option = p.get_option_choice(options)