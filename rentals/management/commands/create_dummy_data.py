"""Command to generate dummy data for rental models"""

from typing import Any
from django.core.management.base import BaseCommand, CommandParser

from rentals.factories import (
    RentalFactory,
    UserFactory,
)


class Command(BaseCommand):
    help = "Generate dummy data for rental"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--users", type=int, default=10, help="Number of users to create"
        )
        parser.add_argument(
            "--rentals", type=int, default=20, help="Number of rentals to create"
        )

    def handle(self, *args: Any, **options: Any) -> str | None:
        num_users = options["users"]
        num_rentals = options["rentals"]

        UserFactory.create_batch(num_users)
        RentalFactory.create_batch(num_rentals)

        self.stdout.write(self.style.SUCCESS("Successfully generated dummy data"))
