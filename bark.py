from src import commands as c
from src import presentation as p


def loop():
    options = {
        "A": p.Option(
            name="Add a bookmark",
            command=c.AddBookmarkCommand(),
            prep_call=p.get_new_bookmark_data,
        ),
        "S": p.Option(
            name="Get bookmark by ID",
            command=c.GetBookmarkCommand(),
            prep_call=p.get_bookmark_id,
        ),
        "B": p.Option(name="List bookmarks by date", command=c.ListBookmarksCommand()),
        "T": p.Option(
            name="List bookmarks by title",
            command=c.ListBookmarksCommand(order_by="title"),
        ),
        "E": p.Option(
            name="Edit a bookmark",
            command=c.EditBookmarkCommand(),
            prep_call=p.get_update_bookmark_data,
        ),
        "G": p.Option(
            name="Import Github stars",
            command=c.ImportGithubStarsCommand(),
            prep_call=p.get_github_import_options,
        ),
        "D": p.Option(
            name="Delete a bookmark",
            command=c.DeleteBookmarkCommand(),
            prep_call=p.get_bookmark_id,
        ),
        "Q": p.Option(name="Quit", command=c.QuitCommand()),
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
