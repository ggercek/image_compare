# -*- coding: utf-8 -*-
"""This module contains the wrapper classes for scikit-image library methods"""

import time
from functools import wraps
from collections import defaultdict
from skimage import io, img_as_float
from skimage.measure import compare_ssim as ssim
from skimage.measure import compare_nrmse as nrmse
from skimage.measure import compare_mse as mse

from image_compare.exceptions import FileError, ArgumentError


MEASUREMENTS = defaultdict(None)


def get_supported_similarity_methods():
    """Returns the supported similarity measurement methods as a list

    :return: supported_methods: list
    """
    return MEASUREMENTS.keys() if MEASUREMENTS is not None else []


def get_similarity_measurement(name):
    """ Returns similarity measurement method
    :param name: name of the method ["ssim", "nrmse", "mse"]
    :return: similarity method if the name is valid
    :raises:
        ArgumentError: if name is a not a valid implemented method
    """
    method = MEASUREMENTS.get(name)
    if method is None:
        raise ArgumentError(f"{name} is a not a supported similarity method")

    return method


def register(name=""):
    """Registers the similarity method with given name to MEASUREMENTS dictionary

    :param name: name of the method e.g ssim, nrmse, mse, etc.
    :return: decorated method
    """
    def decorator_register(func):
        """Decorator to register similarity measurments"""
        MEASUREMENTS[name] = func
    return decorator_register


def time_similarity_calculation_and_update_pair(method, timing_method=time.process_time):
    """Measures the time of the execution of decorated function and
    update the pair parameter pass to that function.

    :param method: similarity method to decorate
    :param timing_method: timing method to use, default value is time.process_time
    Process_time excludes time elapsed during sleep, if sleep time is important time.perf_counter() can be used.
     See the documentation;
      * process_time: https://docs.python.org/3/library/time.html#time.process_time
      * perf_counter: https://docs.python.org/3/library/time.html#time.perf_counter
    :return: the result of decorated function
    """
    @wraps(method)
    def timed(*args, **kw):
        ts = timing_method()
        result = method(*args, **kw)
        te = timing_method()
        # Update pair's elapsed time
        args[0].elapsed = te - ts
        return result
    return timed


def __check_files_and_open(pair, same_size_enforce=True):
    """Private function that enforces common checks and returns the file handlers

    :param pair: `FilePair` object
    :param same_size_enforce: enables dimension check of image pairs
    :return:
        image1, image2 : ndarray, ndarray
        loaded images
    :raises:
        FileError: if an image is missing
        ArgumentError: if same_size_enforce=True and images have different dimensions
    """

    image1 = None
    image2 = None

    try:
        image1 = io.imread(pair.image1)
    except FileNotFoundError:
        pair.skipped = True
        raise FileError("File Not Found", pair.image1)
    try:
        image2 = io.imread(pair.image2)
    except FileNotFoundError:
        pair.skipped = True
        raise FileError("File Not Found", pair.image2)

    if same_size_enforce and image1.size != image2.size:
        pair.skipped = True
        raise ArgumentError(f"Images should be same size, "
                            f"[line:{pair.line_num}]:{pair.image1}[{image1.size}], {pair.image2}[image2.size)]")

    return image1, image2


@register(name="ssim")
@time_similarity_calculation_and_update_pair
def calculate_ssmi_similarity(pair):
    """Compute the mean structural similarity index between two images.

    :param pair: image pair to compare
    :return:
    """
    image1, image2 = __check_files_and_open(pair)
    img1f = img_as_float(image1)
    img2f = img_as_float(image2)
    similarity = ssim(img1f, img2f, multichannel=True)
    pair.similarity = round(1 - similarity, 3)


@register(name="nrmse")
@time_similarity_calculation_and_update_pair
def calculate_nrmse_similarity(pair):
    """Compute the normalized root mean-squared error (NRMSE) between two images.

    :param pair: image pair to compare
    :return:
    """
    image1, image2 = __check_files_and_open(pair)
    img1f = img_as_float(image1)
    img2f = img_as_float(image2)
    similarity = nrmse(img1f, img2f)
    pair.similarity = round(similarity, 3)


@register(name="mse")
@time_similarity_calculation_and_update_pair
def calculate_mse_similarity(pair):
    """Compute the mean-squared error between two images.

    :param pair: image pair to compare
    :return:
    """
    image1, image2 = __check_files_and_open(pair)
    similarity = mse(image1, image2)
    pair.similarity = round(similarity / float(image1.shape[0] * image1.shape[1]), 3)
