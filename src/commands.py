""" A module for the persistence layer """

import sys
import typing as t

from datetime import datetime
from pathlib import Path


from src.database import DatabaseManager


db = DatabaseManager("bookmarks.db")

CommandInput = t.Optional[t.Union[t.Dict[str, str], int]]
CommandResult = t.Optional[t.Union[t.List[str], str]]


class Command(t.Protocol):
    """A protocol class that will be and example for implementing Commands"""

    def execute(self, data: CommandInput) -> CommandResult:
        """The actual execution of the command"""

        pass


class CreateBookmarksTableCommand:
    """A Command class that creates the SQL table"""

    def execute(self):
        """The actual execution of the command"""

        db.create_table(
            table_name="bookmarks",
            columns={
                "id": "integer primary key autoincrement",
                "title": "text not null",
                "url": "text not null",
                "notes": "text",
                "date_added": "text not null",
            },
        )


class AddBookmarkCommand:
    """A Command class that inserts into the SQL table"""

    def execute(self, data: t.Dict[str, str], timestamp: t.Optional[str] = None) -> str:
        """The actual execution of the command"""

        date_added = timestamp or datetime.utcnow().isoformat()
        data.setdefault("date_added", date_added)
        db.add(table_name="bookmarks", data=data)
        return "Bookmark added!"


class ListBookmarksCommand:
    """A Command class that will list all the bookmarks in the SQL table"""

    def __init__(self, order_by: str = "date_added"):
        self.order_by = order_by

    def execute(self) -> t.List[str]:
        """The actual execution of the command"""

        cursor = db.select(table_name="bookmarks", order_by=self.order_by)
        results = cursor.fetchall()
        return results


class GetBookmarkCommand:
    """A Command class that will return a single bookmark based on an ID"""

    def execute(self, data: int) -> t.Optional[tuple]:
        result = db.select(table_name="bookmarks", criteria={"id": data}).fetchone()
        return result


class EditBookmarkCommand:
    """A Command class that will edit a bookmark identified with an ID"""

    def execute(self, data: t.Dict[str, str]) -> str:
        db.update(
            table_name="bookmarks", criteria={"id": data["id"]}, data=data["update"]
        )
        return "Bookmark updated!"


class DeleteBookmarkCommand:
    """A Command class that will delete a bookmark from the SQL table"""

    def execute(self, data: int) -> str:
        db.delete(table_name="bookmarks", criteria={"id": data})
        return "Bookmark deleted!"


class ImportGithubStarsCommand:
    """A Command class that will take the stars from Github and save them into the DB"""

    def execute(self, data: t.Dict[str, str]) -> str:
        bookmarks_imported = 0

        github_username = data["github_username"]
        next_page_of_results = f"https://api.github.com/users/{github_username}/starred"

        while next_page_of_results:
            stars_response = requests.get(
                next_page_of_results,
                headers={"Accept": "application/vnd.github.v3.star+json"},
            )

            if "next" in stars_response.links.keys():
                next_page_of_results = stars_response.links["next"]["url"]
            else:
                next_page_of_results = None

            for repo_response in stars_response.json():
                repo = repo_response["repo"]
                starred_at = repo_response["starred_at"]

                if data["preserve_timestamps"]:
                    timestamp = datetime.strptime(
                        starred_at, "%Y-%m-%dT%H:%M:%SZ"
                    ).isoformat()
                else:
                    timestamp = None

                AddBookmarkCommand().execute(
                    data={
                        "title": repo["name"],
                        "url": repo["html_url"],
                        "notes": repo["description"],
                    },
                    timestamp=timestamp,
                )

                bookmarks_imported += 1

        return f"Imported {bookmarks_imported} bookmarks from starred repos!"


class QuitCommand:
    """A Command class that will quit the application"""

    def execute(self):
        sys.exit()