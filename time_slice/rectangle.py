import glob
from PIL import Image, ImageDraw


def rectangle_slice(path: str, mode: str=None) -> None:
    image_files = glob.glob(path)
    number_images = len(image_files)
    base_image = Image.open(image_files[0]).convert('RGB')

    h, w = base_image.height, base_image.width

    # Used to adjust whether centre 'slice' dimensions are equal to spacing
    # or are 1/4 of total image dimensions i.e. how large  centre slice will be
    if mode == 'big_centre':
        centre_space = 0.75
    else:
        centre_space = 1

    spacing_x = (w * centre_space) / number_images/2
    spacing_y = (h * centre_space) / number_images/2
    top, left = 0, 0
    bottom = h
    right = w

    base_image = Image.new("RGB", base_image.size, 0)

    for image_file in image_files:
        mask_im = Image.new("L", base_image.size, 0)
        draw = ImageDraw.Draw(mask_im)
        draw.polygon([(left, top), (right, top), (right, bottom), (left, bottom)], fill=255)

        selected_image = Image.open(image_file).convert('RGB')
        base_image.paste(selected_image, (0, 0), mask_im)

        top += spacing_y 
        left += spacing_x
        bottom -= spacing_y
        right -= spacing_x

    base_image.save("rectangle.jpeg")
    print("Done")


if __name__ == "__main__":
    path = "images/*.jpg"
    
    rectangle_slice(path, 'big_centre')
