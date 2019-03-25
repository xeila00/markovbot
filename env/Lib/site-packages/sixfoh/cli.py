'''
Generates base sixfoh-encoded images for yer websites.
'''

import os
import sys
import getopt
import mimetypes


options = {
    'files': None,
    'mimetypes': ['image/jpeg', 'image/png', 'image/gif'],
    'encoding': 'base64',
    'output_format': 'image/png',
    'scheme': "data:{output_format};{encoding},{content}"
}

css_formats = {
    "less": "@{filename}: \"{content}\";\n",
    "scss": "${filename}: \"{content}\";\n"
}

NO_IMAGES_MESSAGE = "No valid images found"
IMAGE_NOT_FOUND_MESSAGE = "'{0}' not found\n"
FILE_SIZE_WARNING = """Warning: {0} is larger than 32KB and will not display \
in IE 8.

Press Enter to continue. Use --force to stifle this warning."""


def print_usage(exit_code=0):
    print '''
Usage: %(cmd)s [-LSf] files
    %(cmd)s [-h]

Options
    --less  Writes images into a group of LessCSS variables, to included in a \
stylesheet
            or written to a .less file to be imported. See README.md for \
examples.
    --scss  Writes images into a group of Sass variables, to included in a \
stylesheet
            or written to a .scss file to be imported. See README.md for \
examples.
    -f      Force output and ignore warnings.
    ''' % {'cmd': os.path.basename(sys.argv[0])}
    sys.exit(exit_code)

'''
TODO: -m "mime/type, mime/type"  Pass custom mimetypes. By default sixfoh only
accepts
    image/jpeg, image/png and image/gif
'''


def parse_opts(args):
    try:
        opts, args = getopt.getopt(
            args,
            'hfLS',
            ['help', 'files', 'less', 'scss', 'force']
        )
    except getopt.GetoptError:
        print_usage(1)

    if args:
        options['files'] = args

    for opt, optarg in opts:
        if opt in ('-h', '--help'):
            print_usage()
        elif opt in ('-L', '--less'):
            options['less'] = True
        elif opt in ('-S', '--scss'):
            options['scss'] = True
        elif opt in ('-f', '--force'):
            options['force'] = True


def parse_file_mimetypes(images):
    file_list = []
    for file in images:
        if not os.path.isfile(file):
            print IMAGE_NOT_FOUND_MESSAGE.format(file)
            continue

        mimetype = mimetypes.guess_type(file)[0]
        if mimetype in options['mimetypes']:
            file_list.append([file, mimetype])

    if file_list:
        return file_list
    else:
        print NO_IMAGES_MESSAGE
        sys.exit()


def encode_image(image, mimetype):
    image_size = os.path.getsize(image)
    content = open(image, 'r').read().encode(options['encoding'])\
        .replace("\n", "")

    output = options['scheme'].format(
        output_format=mimetype,
        encoding=options['encoding'],
        content=content
    )

    if image_size > 32000:
        if not options.get('force'):
            raw_input(FILE_SIZE_WARNING.format(image))
            return output
        else:
            return output
    else:
        return output


def output_css(image, mimetype, format):
    print css_formats[format].format(
        filename=os.path.splitext(image)[0].replace(" ", "_"),
        content=encode_image(image, mimetype)
    )


def main():
    parse_opts(sys.argv[1:])

    if options.get('files'):
        files = options['files']
    else:
        files = sorted([f for f in os.listdir('.') if os.path.isfile(f)])

    images = parse_file_mimetypes(files)

    for image, mimetype in images:
        if options.get('less'):
            output_css(image, mimetype, 'less')
        elif options.get('scss'):
            output_css(image, mimetype, 'scss')
        else:
            print encode_image(image, mimetype) + "\n"
