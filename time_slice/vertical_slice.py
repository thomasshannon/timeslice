import glob
from PIL import Image


def vertical_slice():
    path = "images/*.jpg"
    image_files = glob.glob(path)


    # get dimensions of image
    img = Image.open(image_files[0])
    width, height = img.size
    # how wide each slice will be
    spacing = width // len(image_files)
    # top left coords of each slice for cropping
    left, top = 0, 0

    base_img = Image.new('RGB',(width, height), 'white')

    for image_file in image_files:
        current_img = Image.open(image_file)
        slice = current_img.crop((left, top, left + spacing, height))
        base_img.paste(slice, (left, top))
        left += spacing

    
    # save image
    base_img.save("time_slice_result.jpeg")
    print('Done...')

if __name__ == "__main__":
    vertical_slice()