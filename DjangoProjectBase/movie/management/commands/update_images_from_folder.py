import os
from django.core.management.base import BaseCommand
from movie.models import Movie


class Command(BaseCommand):
    help = "Update all movie images from local folder"

    def handle(self, *args, **kwargs):
        images_folder = "images"
        movies = Movie.objects.all()

        self.stdout.write(f"Found {movies.count()} movies")

        updated_count = 0

        for movie in movies:
            image_filename = f"m_{movie.title}.png"
            image_path = os.path.join(images_folder, image_filename)

            if os.path.exists(image_path):
                movie.image = os.path.join("movie/images", image_filename)
                movie.save()
                self.stdout.write(self.style.SUCCESS(f"Updated image for: {movie.title}"))
                updated_count += 1
            else:
                self.stdout.write(self.style.WARNING(f"Image not found for: {movie.title}"))

        self.stdout.write(self.style.SUCCESS(f"Finished. Updated {updated_count} images."))