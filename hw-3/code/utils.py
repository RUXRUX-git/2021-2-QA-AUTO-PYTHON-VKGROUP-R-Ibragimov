import os
import numpy
from PIL import Image
from uuid import uuid4

from api_client import ApiClient
from constants import URLS, EMAIL, PASSWORD


def create_random_image(tmpdir, width, height):
    imarray = numpy.random.rand(height, width, 3) * 255  # First parameter should be height
    im = Image.fromarray(imarray.astype('uint8')).convert('RGBA')
    image_path = os.path.join(os.path.abspath(tmpdir), 'image.png')
    im.save(image_path, 'PNG')

    return image_path


def create_api_client():
    return ApiClient(URLS.BASE, EMAIL, PASSWORD)


def create_random_name():
    return str(uuid4())
