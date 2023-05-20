from unittest import TestCase
from unittest.mock import patch
from textwrap import dedent

from src.database import DatabaseManager


class CreateDatabaseTableTest(TestCase):
    def setUp(self):
        self.db = DatabaseManager(" :memory: ")

    def test_create_table(self):
        with patch("src.database.DatabaseManager._execute") as mocked_execute:
            self.db.create_table(
                table_name="test_table",
                columns={
                "id": "integer primary key autoincrement",
                "test_column_one": "text not null",
                "test_column_two": "text not null"
                }
            )

            mocked_execute.assert_called_with(
                dedent("""
                    CREATE TABLE IF NOT EXISTS test_table(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        test_column_one TEXT NOT NULL,
                        test_column_two TEXT NOT NULL
                    );
                """
                )
            )