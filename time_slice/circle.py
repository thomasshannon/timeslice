import glob
from PIL import Image, ImageDraw
from math import sqrt


def circle(path: str) -> None:
    image_files = glob.glob(path)
    number_images = len(image_files)

    base_image = Image.open(image_files[0]).convert('RGB')

    h, w = base_image.height, base_image.width
    centre_x, centre_y = w / 2, h / 2

    half_diagonal_length = sqrt((centre_x ** 2) + (centre_y ** 2))

    spacing = (half_diagonal_length / number_images)
    radius = half_diagonal_length
    base_image = Image.new("RGB", base_image.size, 0)

    for imageFile in image_files:
        mask_im = Image.new("L", base_image.size, 0)
        draw = ImageDraw.Draw(mask_im)

        x0, y0 = centre_x - radius, centre_y - radius
        x1, y1 = centre_x + radius, centre_y + radius
        draw.ellipse([(x0, y0), (x1, y1)], fill=255)

        selected_image = Image.open(imageFile).convert('RGB')
        base_image.paste(selected_image, (0, 0), mask_im)

        radius -= spacing

    base_image.save("time_slice_circle.jpeg")
    print("Done...")


if __name__ == "__main__":
    path = "images/*.jpg"
    circle(path)