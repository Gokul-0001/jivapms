from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Check if a database table exists (SQLite compatible)."

    def add_arguments(self, parser):
        """
        Define arguments for the management command.
        """
        parser.add_argument(
            "table_name",
            type=str,
            help="Name of the table to check"
        )

    def handle(self, *args, **options):
        """
        Handle the management command.
        """
        table_name = options.get("table_name")

        # Check if table exists
        if self.table_exists(table_name):
            self.stdout.write(self.style.SUCCESS(f"Table '{table_name}' exists in the database."))
        else:
            self.stdout.write(self.style.WARNING(f"Table '{table_name}' does not exist in the database."))

    @staticmethod
    def table_exists(table_name):
        """
        Check if a table exists in the SQLite database using raw SQL.
        """
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
            return cursor.fetchone() is not None
