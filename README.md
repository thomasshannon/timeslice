# Time Slice

Time Slice is a command-line tool for creating a time slice photograph from a series of images taken from a timelapse. The program allows the user to specify the type of pattern to use in the time slice.

## What is a Time Slice Effect?

In photography, a time slice effect is the technique of compositing a series of images, taken from a time-lapse, into a single image. This technique can create stunning visual effects by combining changes in light and movement of things to show the passage of time.

## Why Use Time Slice

Traditionally, creating a time slice effect required manual editing of the images in photo editing software such as GIMP or Photoshop. This process can be time consuming and requires specific photo editing knowledge.

Time Slice was created to simplify and automate the process of creating this effect. Users are able to instantly create time slice photographs in a range of patterns with simple command-line arguments and without needing the skill of using an image editor.

## Installation

Install the package and its dependencies:

```bash
git clone https://github.com/thomasshannon/time-slice.git
cd time-slice
pip install .
```

## Usage

To use Time Slice, you'll need a directory of images taken of a timelapse. The images should be named in sequential order, e.g. `IMG_0001.jpg`, `IMG_0002.jpg`, etc...

Once you have your images, you can use Time Slice to create a time slice photograph with a specified pattern. For example:

```python
python timeslice path/to/images --pattern vertical --output path/to/output
```

### Patterns

Time Slice supports the following patterns:

- vertical
- circle
- sectorcentre
- sectorbottom
- rectangle
- diagonal

### Options

Time Slice supports the following options:

- `--pattern`: Specifies the pattern to use for the time slice. Defaults to `vertical`.
- `--output`: Specifies the file path for the output file. Defaults to the current working directory.
- `--numberSlices`: The number of images to combine into a single time slice image. By default, all images are used.

## Time Slice Output Samples

### Vertical Time Slice

![Vertical time slice](/images/timeslice_vertical_10_images_1.jpg)

### Circular Time Slice

![Circle time slice](/images/timeslice_circle_10_images.jpg)

### Sector (centre) Time Slice

![Sector centre time slice](/images/timeslice_sectorcentre_10_images.jpg)

### Sector (bottom) Time Slice

![Sector time slice](/images/timeslice_sectorbottom_10_images.jpg)

### Rectangle Time Slice

![Rectangle time slice](/images/timeslice_rectangle_10_images.jpg)

### Diagonal Time Slice

![Diagonal time slice](/images/timeslice_diagonal_10_images.jpg)

### Varying the number of input images

|10 Images|50 Images|
|:-:|:-:|
|![Vertical time slice of 10 images](/images/timeslice_vertical_10_images.jpg)|![Vertical time slice of 50 images](/images/timeslice_vertical_50_images.jpg)|

|100 Images|644 Images|
|:-:|:-:|
|![Vertical time slice of 100 images](/images/timeslice_vertical_100_images.jpg)|![Vertical time slice of 644 images](/images/timeslice_vertical_644_images.jpg)|
