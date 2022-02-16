import glob
from PIL import Image, ImageDraw
from math import sqrt, sin, cos
import numpy as np


def sector_bottom(path: str) -> None:
    image_files = glob.glob(path)
    number_images = len(image_files)

    base_image = Image.open(image_files[0]).convert('RGB')

    h, w = base_image.height, base_image.width
    # using diagonal for triangle side length to ensure mask coverage to corners of image
    diagonal_length = sqrt((h ** 2) + (w ** 2))
    # "origin" where slices start from: bottom centre of image
    origin_x, origin_y = w / 2, h
    # slices spacing equally around 180 degrees
    angle = 180 / number_images
    # converting angle degrees to radians - rounding to 5 dp
    base_angle_rad = np.around(np.radians(angle), decimals=5)
    # start at 270 degrees as (0,0) is top left, and we're pasting slices from left to right in image
    # image is situated in top right of plane (+x, +y)
    #________________
    #|    \  |  /   |
    #|_____\_|_/____|
    angle_rad = np.radians(270)

    pt1_x = origin_x + diagonal_length * np.around(sin(angle_rad), decimals=5)
    pt1_y = origin_y + diagonal_length * np.around(cos(angle_rad), decimals=5)

    angle_rad -= base_angle_rad
    pt2_x = origin_x + diagonal_length * np.around(sin(angle_rad), decimals=5)
    pt2_y = origin_y + diagonal_length * np.around(cos(angle_rad), decimals=5)

    pt_0 = origin_x, origin_y
    pt_1 = pt1_x, pt1_y
    pt_2 = pt2_x, pt2_y

    for image_file in image_files:
        mask_im = Image.new("L", base_image.size, 0)
        draw = ImageDraw.Draw(mask_im)
        draw.polygon([(pt_0), (pt_1), (pt_2), (pt_0)], fill=255)

        selected_image = Image.open(image_file).convert('RGB')
        base_image.paste(selected_image, (0, 0), mask_im)

        pt_1 = pt2_x, pt2_y
        # moving left to right, so minus base angle to get spacing
        angle_rad -= base_angle_rad
        pt2_x = origin_x + diagonal_length * np.around(sin(angle_rad), decimals=5)
        pt2_y = origin_y + diagonal_length * np.around(cos(angle_rad), decimals=5)
        pt_2 = pt2_x, pt2_y

    base_image.save("sectors_bottom.jpeg")
    print("Done...")


if __name__ == "__main__":
    path = "images/*.jpg"
    sector_bottom(path)