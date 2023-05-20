""" A module for the persistance layer """

import sys
import typing as t

from src.database import DatabaseManager
from datetime import datetime

db = DatabaseManager("bookmarks.db")

CommandInput = t.Optional[t.Union[t.Dict[str, str], int]]
CommandResult = t.Optional[t.Union[t.List[str], str]]

class Command(t.Protocol):
    """ A protocol class that will be an example for implementing Commands """

    def execute(self, data: CommandInput) -> CommandResult:
        """ The actual execution of the command """
        pass


class CreateBookmarksTableCommand:
    """ A Command class that creates the SQL table """

    def execute(self):
        """ The actual execution of the command """

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
    """ A Command class that inserts into the SQL table """
    def execute(self, data: t.Dict[str, str]):
        """ The actual execution of the command """

        date_added = datetime.utcnow().isoformat
        data.setdefault("date_added", date_added)
        db.add(table_name="bookmarks", data=data)
        return "Bookmark added"


class ListBookmarksCommand:
    """ A Command class that will list all the bookmarks in the SQL table """

    def __init__(self, order_by: str = "date_added"):
        self.order_by = order_by

    def execute(self):
        """ The actual execution of the command """
        
        cursor = db.select(
            table_name="bookmarks",
            order_by=self.order_by
        )
        results = cursor.fetchall()
        return results
    

class DeleteBookmarkCommand:
    """ A Command class that will delete a bookmark from the SQL table """ 

    def execute(self, data: int) -> str:
        db.delete(table_name="bookmarks", criteria={"id": data})
        return "Bookmark deleted"
    
class QuitCommand:
    """ A Command class that will quit the application """
    def execute(self):
        sys.exit()