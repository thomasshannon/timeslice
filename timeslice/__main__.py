import argparse
from typing import Dict
from time_slice import TimeSlice


def slice_modes() -> list[str]:
    return ['vertical', 'circle', 'sectorcentre', 'sectorbottom', 'rectangle', 'diagonal']


def get_help() -> Dict:
    help_text = dict()
    help_text['path'] = "Relative or absolute string path to source images directory"
    help_text['pattern'] = "Slicing pattern to use. Choose from values " + \
        ', '.join(slice_modes()) + ' (default: vertical)'
    help_text['outputDirectory'] = "Path where the resultant timeslice image is saved (default: current directory)"
    return help_text


def main():
    help_text = get_help()
    parser = argparse.ArgumentParser(
        description='time_slice: Create timeslice images from time lapse photo sets, with customimsable geometric patterns')

    parser.add_argument('directory',
                        type=str, help=help_text['path'])

    parser.add_argument('-p', '--pattern', metavar='PATTERN',
                        type=str,
                        default='vertical',
                        help=help_text['pattern'],
                        choices=slice_modes()
                        )
    parser.add_argument('-o', '--outputDirectory', metavar='OUTPUT_DIRECTORY',
                        type=str,
                        default='',
                        help=help_text['outputDirectory'],
                        )
    args = parser.parse_args()

    # Check inputs
    if args.pattern not in slice_modes():
        raise ValueError('Invalid pattern')

    t = TimeSlice(args.directory, args.pattern)
    sliced_image = t.create_time_slice()
    t.export_slice(sliced_image, args.outputDirectory)


if __name__ == '__main__':
    main()
