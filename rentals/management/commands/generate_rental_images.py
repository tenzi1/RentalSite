"""Command to create dummy rental images for rental instances"""

import os
import random
from pathlib import Path
from django.core.files import File
from django.core.management.base import BaseCommand, CommandParser
from rentals.models import Rental, RentalImage


class Command(BaseCommand):
    help = "Creates rental images and assign them to rentals"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--image_dir", type=str, required=True, help="Directory containing images"
        )

    def handle(self, *args, **options):
        image_dir = options["image_dir"]
        image_files = list(Path(image_dir).glob("*"))

        if not image_files:
            self.stdout.write(
                self.style.ERROR("No images found in specified directory")
            )
            return

        rentals = list(Rental.objects.all())
        if not rentals:
            self.stdout.write(self.style.ERROR("No rentals found in the database"))
            return

        random.shuffle(image_files)

        for rental in rentals:
            num_images = random.randint(1, 4)
            assigned_images = random.sample(
                image_files, min(num_images, len(image_files))
            )
            for image_path in assigned_images:
                with open(image_path, "rb") as image_file:
                    RentalImage.objects.create(
                        rental=rental,
                        image=File(image_file, name=os.path.basename(image_path)),
                    )
        self.stdout.write(self.style.SUCCESS("Successfully generated rental images"))
