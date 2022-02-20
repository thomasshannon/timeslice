import os
from PIL import Image, ImageDraw
from math import sqrt, pi, sin, acos, cos
import numpy as np
from typing import Optional


class TimeSlice:
    def __init__(self, input_path: str, slice_mode: Optional[str] = 'vertical') -> None:
        """
        Combines all images into a single sliced image that is saved in output directory
        Parameters:-
        input_put: Path to directory containing image set to create slices from
        slice_mode: Pattern to create the slice, defaults to vertical
        """
        # initialise - open image, get params width, height
        self.img_files = self._get_dir_image_files(input_path)
        self.num_images = len(self.img_files)
        self.slice_mode = slice_mode

        self.input_path = os.path.split(os.path.abspath(__file__))[0]
        self.output_path = os.path.join(self.input_path, 'time_slice_output')

        with Image.open(self.img_files[0]) as reference_image:
            self.img_height, self.img_width = reference_image.height, reference_image.width

        match self.slice_mode:
            case 'circle':
                sliced_img = self.slice_circle()
            case 'sectorcentre':
                sliced_img = self.slice_sector_centre()
            case 'sectorbottom':
                sliced_img = self.slice_sector_bottom()
            case 'rectangle':
                sliced_img = self.slice_rectangle()
            case 'diagonal':
                sliced_img = self.slice_diagonal()
            case _:
                sliced_img = self.slice_vertical()

        self._export_slice(sliced_img)

    def _open_image(self, img_path: str) -> Image.Image:
        """
         Opens image file and returns image object
        """
        # if png convert to RGBA else convert to RGB
        if img_path.endswith('.png'):
            return Image.open(img_path).convert('RGBA')
        else:
            return Image.open(img_path).convert('RGB')

    def _get_dir_image_files(self, path: str) -> list[str]:
        """
            Returns all filenames of images in specified directory
        """
        files = os.listdir(path)
        img_files = []
        for file in files:
            if file.endswith(('.jpg', '.jpeg', '.png')):
                img_files.append(os.path.join(path, file))

        if len(img_files) == 0:
            raise FileNotFoundError(
                f'No images found at given path: {path}')

        return img_files

    def slice_vertical(self) -> Image.Image:
        spacing_x = self.img_width / self.num_images
        offset = 0

        base_image = Image.new("RGB", (self.img_width, self.img_height), 0)
        for image_file in self.img_files:
            mask_im = Image.new("L", base_image.size, 0)
            draw = ImageDraw.Draw(mask_im)
            draw.polygon([(offset, 0), (self.img_width, 0), (self.img_width,
                         self.img_height), (offset, self.img_height)], fill=255)
            selected_image = Image.open(image_file).convert('RGB')
            base_image.paste(selected_image, (0, 0), mask_im)
            offset += spacing_x

        return base_image

    def slice_circle(self) -> Image.Image:
        centre_x, centre_y = self.img_width / 2, self.img_height / 2    # centre of image
        # make radius equal to half the diagonal of the image size
        radius = sqrt((centre_x ** 2) + (centre_y ** 2))
        spacing = radius / self.num_images    # 'thickness' of each circular slice

        base_image = Image.new("RGB", (self.img_width, self.img_height), 0)
        for image_file in self.img_files:
            mask_im = Image.new("L", base_image.size, 0)
            draw = ImageDraw.Draw(mask_im)

            x0, y0 = centre_x - radius, centre_y - radius
            x1, y1 = centre_x + radius, centre_y + radius
            draw.ellipse([(x0, y0), (x1, y1)], fill=255)

            selected_image = Image.open(image_file).convert('RGB')
            base_image.paste(selected_image, (0, 0), mask_im)

            radius -= spacing

        return base_image

    def slice_diagonal(self) -> Image.Image:
        diagonal_length = sqrt((self.img_height ** 2) + (self.img_width ** 2))
        spacing = diagonal_length / self.num_images
        theta = acos(self.img_height / diagonal_length)
        offset = 0
        x_start, y_start = 0, 0

        base_image = Image.new(
            "RGB", (self.img_width, self.img_height), 255)   # white image
        for image_file in self.img_files:
            mask_im = Image.new("L", base_image.size, 0)
            draw = ImageDraw.Draw(mask_im)
            x_end = offset / sin(theta)
            y_end = offset / sin(pi / 2 - theta)
            draw.polygon([(x_start, y_start), (x_end, y_start),
                         (x_start, y_end), (x_start, y_start)], fill=0)  # fill black
            selected_image = Image.open(image_file).convert('RGB')
            base_image.paste(selected_image, (0, 0), mask_im)

            offset += spacing

        return base_image

    def slice_sector_centre(self) -> Image.Image:
        centre_x, centre_y = self.img_width / 2, self.img_height / 2    # centre of image
        diagonal_length = sqrt((self.img_height ** 2) + (self.img_width ** 2))
        # angle refers to sector size of each image
        angle = 360 / self.num_images
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

        base_image = Image.new("RGB", (self.img_width, self.img_height), 255)
        for image_file in self.img_files:
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

        return base_image

    def slice_sector_bottom(self) -> Image.Image:
        # using diagonal for triangle side length to ensure mask coverage to corners of image
        diagonal_length = sqrt((self.img_height ** 2) + (self.img_width ** 2))
        # "origin" where slices start from: bottom centre of image
        origin_x, origin_y = self.img_width / 2, self.img_height
        # slices spacing equally around 180 degrees
        angle = 180 / self.num_images
        # converting angle degrees to radians - rounding to 5 dp
        base_angle_rad = np.around(np.radians(angle), decimals=5)
        # start at 270 degrees as (0,0) is top left, and we're pasting slices from left to right in image
        # image is situated in top right of plane (+x, +y)
        # _________________
        # |    \  |  /    |
        # |_____\_|_/_____|
        angle_rad = np.radians(270)

        pt1_x = origin_x + diagonal_length * \
            np.around(sin(angle_rad), decimals=5)
        pt1_y = origin_y + diagonal_length * \
            np.around(cos(angle_rad), decimals=5)

        angle_rad -= base_angle_rad
        pt2_x = origin_x + diagonal_length * \
            np.around(sin(angle_rad), decimals=5)
        pt2_y = origin_y + diagonal_length * \
            np.around(cos(angle_rad), decimals=5)

        pt_0 = origin_x, origin_y
        pt_1 = pt1_x, pt1_y
        pt_2 = pt2_x, pt2_y

        base_image = Image.new("RGB", (self.img_width, self.img_height), 255)
        for image_file in self.img_files:
            mask_im = Image.new("L", base_image.size, 0)
            draw = ImageDraw.Draw(mask_im)
            draw.polygon([(pt_0), (pt_1), (pt_2), (pt_0)], fill=255)

            selected_image = Image.open(image_file).convert('RGB')
            base_image.paste(selected_image, (0, 0), mask_im)

            pt_1 = pt2_x, pt2_y
            # moving left to right, so minus base angle to get spacing
            angle_rad -= base_angle_rad
            pt2_x = origin_x + diagonal_length * \
                np.around(sin(angle_rad), decimals=5)
            pt2_y = origin_y + diagonal_length * \
                np.around(cos(angle_rad), decimals=5)
            pt_2 = pt2_x, pt2_y

        return base_image

    def slice_rectangle(self, mode: str = None) -> Image.Image:

        # Used to adjust whether centre 'slice' dimensions are equal to spacing
        # or are 1/4 of total image dimensions i.e. how large  centre slice will be
        if mode == 'big_centre':
            centre_space = 0.75
        else:
            centre_space = 1

        spacing_x = (self.img_width * centre_space) / self.num_images / 2
        spacing_y = (self.img_height * centre_space) / self.num_images / 2
        top, left = 0, 0
        bottom = self.img_height
        right = self.img_width

        base_image = Image.new("RGB", (self.img_width, self.img_height), 0)
        for image_file in self.img_files:
            mask_im = Image.new("L", base_image.size, 0)
            draw = ImageDraw.Draw(mask_im)
            draw.polygon([(left, top), (right, top),
                         (right, bottom), (left, bottom)], fill=255)

            selected_image = Image.open(image_file).convert('RGB')
            base_image.paste(selected_image, (0, 0), mask_im)

            top += spacing_y
            left += spacing_x
            bottom -= spacing_y
            right -= spacing_x

        return base_image

    def _export_slice(self, image: Image.Image) -> None:
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        path = os.path.join(self.output_path,
                            f'time_slice_{self.slice_mode}_{self.num_images}_images.jpeg')
        try:
            image.save(path, format='JPEG')
        except OSError: 
            print('Image could not be written')
        else:
            print(f'Time slice image written to {path}')
