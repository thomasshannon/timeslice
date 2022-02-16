import glob
from PIL import Image, ImageDraw
from math import sqrt, sin, cos
import numpy as np


def sector_centre(path: str) -> None:
    image_files = glob.glob(path)
    number_images = len(image_files)

    base_image = Image.open(image_files[0]).convert('RGB')

    h, w = base_image.height, base_image.width
    diagonal_length = sqrt((h ** 2) + (w ** 2))
    centre_x, centre_y = w//2, h//2
    # angle refers to sector size of each image
    angle = 360 / number_images
    base_angle_rad = np.radians(angle)
    angle_rad = 0

    # 3 points to make a triangle polygon for masking each sector
    # apex of triangle located at centre of image (width / 2, height / 2)
    # altitude of triangle is the diagonal length of the image dimensions
    # so that mask will cover to very edge of image.
    
    # calculate in radians
    pt1_x = centre_x + diagonal_length * sin(angle_rad)
    pt1_y = centre_y + diagonal_length * cos(angle_rad)

    angle_rad += base_angle_rad
    pt2_x = centre_x + diagonal_length * sin(angle_rad)
    pt2_y = centre_y + diagonal_length * cos(angle_rad)

    pt_0 = centre_x, centre_y
    pt_1 = pt1_x, pt1_y
    pt_2 = pt2_x, pt2_y

    for image_file in image_files:
        mask_im = Image.new("L", base_image.size, 0)
        draw = ImageDraw.Draw(mask_im)
        draw.polygon([(pt_0), (pt_1), (pt_2), (pt_0)], fill=255)

        selected_image = Image.open(image_file).convert('RGB')
        base_image.paste(selected_image, (0, 0), mask_im)

        pt_1 = pt2_x, pt2_y
        angle_rad += base_angle_rad
        pt2_x = centre_x + diagonal_length * sin(angle_rad)
        pt2_y = centre_y + diagonal_length * cos(angle_rad)
        pt_2 = pt2_x, pt2_y

    base_image.save("sectors_centre.jpeg")
    print("Done...")


if __name__ == "__main__":
    path = "images/*.jpg"
    sector_centre(path)