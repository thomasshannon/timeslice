from math import sqrt, pi, sin, acos, cos
from pathlib import Path, PurePath

import numpy as np
from PIL import Image, ImageDraw


class TimeSlice:
    def __init__(self, input_path: str) -> None:
        """
        Initialise TimeSlice class, passing directory of input images in which is checked to contain valid images,
        instance variables of image files and image dimensions are set
        :param input_path: Path to directory containing timelapse images
        :type input_path: str
        """
        self.img_files = self._get_dir_image_files(input_path)
        self.num_images = len(self.img_files)
        self.num_slices = self.num_images
        self.slice_mode = ''
        with Image.open(self.img_files[0]) as reference_image:
            self.img_height = reference_image.height
            self.img_width = reference_image.width

    def create_time_slice(self, slice_mode: str = 'vertical', slices_number: int = 0) -> Image.Image:
        """
        Combines all images into a single time slice image with pattern specified by slice_mode and returns the
        image. If slice_mode is not specified, default it vertical
        :param slice_mode: Pattern to create the slice, defaults to vertical
        :type slice_mode: str
        :param slices_number:  Number of images to use in the photo slice, defaults to 0. If slices_number is 0, this
        argument is ignored and all input images are used
        :type slices_number: int
        :return: The time slice image combined from the images :rtype: Image.Image
        """
        self.slice_mode = slice_mode
        self.num_slices = slices_number if 0 < slices_number < self.num_images else self.num_images
        # Use np.linspace to select equally spaced subset of image files if number of slices < number images        
        self.img_files = [self.img_files[int(i)] for i in np.linspace(0, self.num_images - 1, self.num_slices)]

        if self.slice_mode == 'circle':
            sliced_img = self._slice_circle()
        elif self.slice_mode == 'sectorcentre':
            sliced_img = self._slice_sector_centre()
        elif self.slice_mode == 'sectorbottom':
            sliced_img = self._slice_sector_bottom()
        elif self.slice_mode == 'rectangle':
            sliced_img = self._slice_rectangle()
        elif self.slice_mode == 'diagonal':
            sliced_img = self._slice_diagonal()
        else:
            sliced_img = self._slice_vertical()
        return sliced_img

    @staticmethod
    def _get_dir_image_files(path: str) -> list[Path]:
        """
        Returns list of image filenames images in specified directory. Iterates over files in specified directory and
        adds to list if they are of type jpg or png
        :param path: path to directory
        :type path: str
        :return: list of filenames of images contained in the directory
        :rtype: list[Path]
        """
        file_path = Path(path)
        if not file_path.is_dir():
            raise NotADirectoryError(f'Invalid directory specified: {path}')
        img_files = []
        for file in file_path.iterdir():
            if file.is_file() and file.suffix.lower() in {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}:
                img_files.append(file)
        if len(img_files) == 0:
            raise FileNotFoundError(f'No images found at given path: {path}')

        return img_files

    def _slice_vertical(self) -> Image.Image:
        """
        Creates a single image of horizontal slices from the set of images.
        Creates horizontal slices of the set of images combined into a single image. Width of each slice is image width
        divided by number of images.
        :return: PIL Image of combined horizontally sliced images
        :rtype: Image.Image
        """
        spacing_x = self.img_width / self.num_slices
        offset = 0
        base_image = Image.new("RGB", (self.img_width, self.img_height), 0)
        for image_file in self.img_files:
            mask_im = Image.new("L", base_image.size, 0)
            draw = ImageDraw.Draw(mask_im)
            draw.polygon(
                [(offset, 0), (self.img_width, 0), (self.img_width, self.img_height), (offset, self.img_height)],
                fill=255)
            selected_image = Image.open(image_file).convert('RGB')
            base_image.paste(selected_image, (0, 0), mask_im)
            offset += spacing_x
        return base_image

    def _slice_circle(self) -> Image.Image:
        """
        Creates a single image of circular slices from the set of images
        Creates annulus or pattern from set of images. Width of each donut equal to half the diagonal of the image
        divided by the number of images.
        :return: PIL Image of combined circular/donut sliced images
        :rtype: Image.Image
        """
        # centre of image
        centre_x, centre_y = self.img_width / 2, self.img_height / 2
        radius = sqrt((centre_x ** 2) + (centre_y ** 2))
        # width or 'thickness' of each donut shaped slice
        spacing = radius / self.num_slices
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

    def _slice_diagonal(self) -> Image.Image:
        """
        Creates a single image of diagonal slices from the set of images. Combines the images into singular image of
        diagonal slices. Width is the image's diagonal length divided by the number of images. Angle of diagonals
        determined by the angle made between the diagonal length and the image height.
        :return: PIL Image of combined diagonally sliced images
        :rtype: Image.Image
        """
        diagonal_length = sqrt((self.img_height ** 2) + (self.img_width ** 2))
        spacing = diagonal_length / self.num_slices
        theta = acos(self.img_height / diagonal_length)
        offset = 0
        x_start, y_start = 0, 0
        # white base image
        base_image = Image.new("RGB", (self.img_width, self.img_height), 0)
        for image_file in self.img_files:
            mask_im = Image.new("L", base_image.size, 255)
            draw = ImageDraw.Draw(mask_im)
            x_end = offset / sin(theta)
            y_end = offset / sin(pi / 2 - theta)
            draw.polygon([(x_start, y_start), (x_end, y_start), (x_start, y_end), (x_start, y_start)], fill=0)
            selected_image = Image.open(image_file).convert('RGB')
            base_image.paste(selected_image, (0, 0), mask_im)
            offset += spacing
        return base_image

    def _slice_sector_centre(self) -> Image.Image:
        """
        Creates single image of a circle sector pattern from set of images.
        Sector pattern originates in centre of image. Angle of each sector calculated by 360 degrees divided by the
        number of images. Pattern made by creating mask of a triangle polygon with apex at centre of image
        (width / 2, height / 2). Altitude of triangle set as diagonal length of image dimensions to ensure the mask
        covers to edge of image.
        :return: PIL Image of combined sector sliced images
        :rtype: Image.Image
        """
        centre_x, centre_y = self.img_width / 2, self.img_height / 2
        diagonal_length = sqrt((self.img_height ** 2) + (self.img_width ** 2))
        # angle refers to sector size of each image
        angle = 360 / self.num_slices
        base_angle_rad = np.radians(angle)
        angle_rad = np.radians(360)
        # calculate in radians pt_1 and pt_2 triangle vertices
        pt1_x = centre_x + diagonal_length * sin(angle_rad)
        pt1_y = centre_y + diagonal_length * cos(angle_rad)
        angle_rad -= base_angle_rad
        pt2_x = centre_x + diagonal_length * sin(angle_rad)
        pt2_y = centre_y + diagonal_length * cos(angle_rad)
        pt_0 = centre_x, centre_y
        pt_1 = pt1_x, pt1_y
        pt_2 = pt2_x, pt2_y
        base_image = Image.new("RGB", (self.img_width, self.img_height), 255)
        for image_file in self.img_files:
            mask_im = Image.new("L", base_image.size, 0)
            draw = ImageDraw.Draw(mask_im)
            draw.polygon([pt_0, pt_1, pt_2, pt_0], fill=255)
            selected_image = Image.open(image_file).convert('RGB')
            base_image.paste(selected_image, (0, 0), mask_im)
            pt_1 = pt2_x, pt2_y
            angle_rad -= base_angle_rad
            pt2_x = centre_x + diagonal_length * sin(angle_rad)
            pt2_y = centre_y + diagonal_length * cos(angle_rad)
            pt_2 = pt2_x, pt2_y
        return base_image

    def _slice_sector_bottom(self) -> Image.Image:
        """
        Creates single image of a circle sector pattern with origin at bottom of image from set of images. Sector
        pattern originates at bottom centre of image. Angle of each sector calculated by 180 degrees divided by the
        number of images. Pattern made by creating mask of a triangle polygon with apex at bottom, middle of image
        (width / 2, height). Altitude of triangle set as diagonal length of image dimensions to ensure the mask covers
        to edge of image.
        :return: PIL Image of combined sector sliced images
        :rtype: Image.Image
        """
        diagonal_length = sqrt((self.img_height ** 2) + (self.img_width ** 2))
        # origin referring to bottom centre of image where slice apexes are
        origin_x, origin_y = self.img_width / 2, self.img_height
        angle = 180 / self.num_slices
        base_angle_rad = np.around(np.radians(angle), decimals=5)
        # start at 270 deg - (0,0) is top left, pasting slices left to right
        # image is situated in top right of plane (+x, +y)
        angle_rad = np.radians(270)
        pt1_x = origin_x + diagonal_length * np.around(sin(angle_rad), decimals=5)
        pt1_y = origin_y + diagonal_length * np.around(cos(angle_rad), decimals=5)
        angle_rad -= base_angle_rad
        pt2_x = origin_x + diagonal_length * np.around(sin(angle_rad), decimals=5)
        pt2_y = origin_y + diagonal_length * np.around(cos(angle_rad), decimals=5)
        pt_0 = origin_x, origin_y
        pt_1 = pt1_x, pt1_y
        pt_2 = pt2_x, pt2_y
        base_image = Image.new("RGB", (self.img_width, self.img_height), 255)
        for image_file in self.img_files:
            mask_im = Image.new("L", base_image.size, 0)
            draw = ImageDraw.Draw(mask_im)
            draw.polygon([pt_0, pt_1, pt_2, pt_0], fill=255)
            selected_image = Image.open(image_file).convert('RGB')
            base_image.paste(selected_image, (0, 0), mask_im)
            pt_1 = pt2_x, pt2_y
            # moving left to right, so minus base angle to get spacing
            angle_rad -= base_angle_rad
            pt2_x = origin_x + diagonal_length * np.around(sin(angle_rad), decimals=5)
            pt2_y = origin_y + diagonal_length * np.around(cos(angle_rad), decimals=5)
            pt_2 = pt2_x, pt2_y
        return base_image

    def _slice_rectangle(self) -> Image.Image:
        """
        Creates single image of rectangle pattern combining set of images.
        Images are combined in a rectangle frame-like pattern with same aspect ratio as dimensions of image dimensions
        equal to be image width/number images/2 and image height/number images/2. Rectangle frames are centred at the
        centre of the image.
        :return: PIL Image of combined rectangular pattern of sliced images
        :rtype: Image.Image
        """
        spacing_x = self.img_width / self.num_slices / 2
        spacing_y = self.img_height / self.num_slices / 2
        top, left = 0, 0
        bottom = self.img_height
        right = self.img_width
        base_image = Image.new("RGB", (self.img_width, self.img_height), 0)
        for image_file in self.img_files:
            mask_im = Image.new("L", base_image.size, 0)
            draw = ImageDraw.Draw(mask_im)
            draw.polygon([(left, top), (right, top), (right, bottom), (left, bottom)], fill=255)
            selected_image = Image.open(image_file).convert('RGB')
            base_image.paste(selected_image, (0, 0), mask_im)
            top += spacing_y
            left += spacing_x
            bottom -= spacing_y
            right -= spacing_x
        return base_image

    def export_slice(self, image: Image.Image, output_directory: str) -> None:
        """
        Exports PIL image to a jpeg
        Creates directory specified by self.output_path if not exists and saves the PIL image as a jpeg with filename
        based on the slice pattern and number of images inputted
        :param image: PIL image to save
        :type image: Image.Image
        :param output_directory: directory to save the image
        :type output_directory: str
        """
        Path(output_directory).mkdir(parents=True, exist_ok=True)
        full_path = str(PurePath(output_directory, f'timeslice_{self.slice_mode}_{self.num_slices}_images.jpg'))
        try:
            image.save(full_path, format='JPEG')
        except OSError:
            print('Image could not be written')
        else:
            print(f'Time slice image written to {full_path}')
