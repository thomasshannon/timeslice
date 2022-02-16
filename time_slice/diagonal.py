import glob
from math import sqrt, sin, acos, pi
from PIL import Image, ImageDraw


def diagonal(path: str) -> None:
    """
    TODO: describe whats going on here
    """
    image_files = glob.glob(path)
    number_images = len(image_files)

    base_image = Image.open(image_files[0]).convert('RGB')

    h, w = base_image.height, base_image.width
    diagonal_length = sqrt((h ** 2) + (w ** 2))
    spacing = diagonal_length / number_images

    base_image = Image.new("RGB", base_image.size, 0)

    # calculate angle diagonal makes from image dimensions
    # use this angle for angle of diagonal slices
    theta = acos(h / diagonal_length)
    offset = 0
    
    # top left of image
    x_start, y_start = 0, 0
    

    for i, image_file in enumerate(image_files):
        mask_im = Image.new("L", base_image.size, 255)
        draw = ImageDraw.Draw(mask_im)
        x_end = offset / sin(theta)
        y_end = offset / sin(pi/2 - theta)

        # mask is a triangle with vertex at origin, with height/altitude a multiple of the offset
        draw.polygon([(x_start, y_start), (x_end, y_start), (x_start, y_end), (x_start, y_start)], fill=0)

        selected_image = Image.open(image_file).convert('RGB')
        base_image.paste(selected_image, (0, 0), mask_im)

        offset += spacing

    base_image.save("diagonal.jpeg")



if __name__  == "__main__":
    path = "images/*.jpg"
    diagonal(path)