""" A module for the persistence layer """

import sys
import typing as t
import requests 

from datetime import datetime
from pathlib import Path


from src.database import DatabaseManager


db = DatabaseManager("debtors.db")

CommandInput = t.Optional[t.Union[t.Dict[str, str], int]]
CommandResult = t.Optional[t.Union[t.List[str], str]]


class Command(t.Protocol):
    """A protocol class that will be and example for implementing Commands"""

    def execute(self, data: CommandInput) -> CommandResult:
        """The actual execution of the command"""

        pass


class CreateDebtorsTableCommand:
    """A Command class that creates the SQL table"""

    def execute(self):
        """The actual execution of the command"""

        db.create_table(
            table_name="debtors",
            columns={
                "id": "integer primary key autoincrement",
                "name": "text not null",
                "sum_owed": "integer not null",
                "date_due": "text not null",
                "notes": "text",
                "date_added": "text not null",
            },
        )


class AddDebtorCommand:
    """A Command class that inserts into the SQL table"""

    def execute(self, data: t.Dict[str, str], timestamp: t.Optional[str] = None) -> str:
        """The actual execution of the command"""

        date_added = timestamp or datetime.utcnow().isoformat()
        data.setdefault("date_added", date_added)
        db.add(table_name="debtors", data=data)
        return "Debtor added!"


class ListDebtorsCommand:
    """A Command class that will list all the Debtors in the SQL table"""

    def __init__(self, order_by: str = "date_added"):
        self.order_by = order_by

    def execute(self) -> t.List[str]:
        """The actual execution of the command"""

        cursor = db.select(table_name="debtors", order_by=self.order_by)
        results = cursor.fetchall()
        return results


class GetDebtorCommand:
    """A Command class that will return a single Debtor based on an ID"""

    def execute(self, data: int) -> t.Optional[tuple]:
        result = db.select(table_name="debtors", criteria={"id": data}).fetchone()
        return result


class EditDebtorCommand:
    """A Command class that will edit a Debtor identified with an ID"""

    def execute(self, data: t.Dict[str, str]) -> str:
        db.update(
            table_name="debtors", criteria={"id": data["id"]}, data=data["update"]
        )
        return "Debtor information updated!"


class DeleteDebtorCommand:
    """A Command class that will delete a Debtor from the SQL table"""

    def execute(self, data: int) -> str:
        db.delete(table_name="debtors", criteria={"id": data})
        return "Debtor deleted!"


class QuitCommand:
    """A Command class that will quit the application"""

    def execute(self):
        sys.exit()