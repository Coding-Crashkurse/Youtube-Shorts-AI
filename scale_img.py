from PIL import Image
import os

class ImageResizer:
    def __init__(self, target_width: int, target_height: int, directory: str = "data"):
        self.target_width = target_width
        self.target_height = target_height
        self.directory = directory

    def process_dir(self) -> None:
        for filename in os.listdir(self.directory):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                image_path = os.path.join(self.directory, filename)
                scaled_image = self._resize_image(image_path)
                self._save_image(scaled_image, image_path)

    def _resize_image(self, image_path: str) -> Image:
        image = Image.open(image_path)
        original_width, original_height = image.size

        # Determine scale factor to maintain aspect ratio
        scale_factor = max(self.target_width / original_width, self.target_height / original_height)
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)

        # Scale the image
        scaled_image = image.resize((new_width, new_height), Image.LANCZOS)

        # Calculate the coordinates for center cropping
        left = int((new_width - self.target_width) / 2)
        top = int((new_height - self.target_height) / 2)
        right = int((new_width + self.target_width) / 2)
        bottom = int((new_height + self.target_height) / 2)

        # Crop and return the image
        return scaled_image.crop((left, top, right, bottom))

    def _save_image(self, image: Image, image_path: str) -> None:
        image.save(image_path)
